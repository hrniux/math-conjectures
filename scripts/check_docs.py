#!/usr/bin/env python3
"""Offline checks for this repository's documented Markdown subset; see CONTRIBUTING."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Document:
    def __init__(self):
        self.links = []  # (destination, source line) for rendered link/image uses
        self.anchors = set()
        self.errors = []


class HTMLLinks(HTMLParser):
    def __init__(self, document):
        super().__init__(convert_charrefs=True)
        self.document = document

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("id", "name" if tag == "a" else "id"):
            if attrs.get(name):
                self.document.anchors.add(attrs[name])
        attribute = {"a": "href", "img": "src"}.get(tag)
        if attribute and attribute in attrs:
            self.document.links.append((attrs[attribute], self.getpos()[0]))

    handle_startendtag = handle_starttag


def visible_text(text):
    """Blank code and real comments in context, preserving offsets and lines."""
    visible = list(text)

    def hide(start, end):
        for position in range(start, end):
            if visible[position] != "\n":
                visible[position] = " "

    fence, i = None, 0
    while i < len(text):
        if i == 0 or text[i - 1] == "\n":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end + 1
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", text[i:end].rstrip("\n"))
            if fence:
                hide(i, end)
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
                i = end
                continue
            if marker:
                fence = marker[1]
                hide(i, end)
                i = end
                continue
        # Code spans are consumed as a unit: their comment markers stay inert.
        if text[i] == "`":
            end = i + 1
            while end < len(text) and text[end] == "`":
                end += 1
            marker, close = text[i:end], end
            while True:
                close = text.find(marker, close)
                if close < 0:
                    break
                after = close + len(marker)
                if text[close - 1] != "`" and (after == len(text) or text[after] != "`"):
                    hide(i, after)
                    end = after
                    break
                close = after
            i = end
            continue
        # Conversely, code markers within a real comment cannot start code.
        if text.startswith("<!--", i):
            close = text.find("-->", i + 4)
            end = len(text) if close < 0 else close + 3
            hide(i, end)
            i = end
            continue
        if text[i] == "\\":
            i += 2
        else:
            i += 1
    return "".join(visible)


def balanced_end(text, start, opening, closing):
    depth, i = 1, start + 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == opening:
            depth += 1
        elif text[i] == closing:
            depth -= 1
            if not depth:
                return i
        i += 1
    return None


def inline_link_end(text, start):
    """Find the outer close after a destination and an optional quoted title."""
    i = start + 1
    while i < len(text) and text[i].isspace():
        i += 1
    if i < len(text) and text[i] == "<":
        end = text.find(">", i + 1)
        if end < 0:
            return None
        i = end + 1
    else:
        depth = 0
        while i < len(text):
            if text[i] == "\\":
                i += 2
                continue
            if text[i].isspace() and depth == 0:
                break
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                if depth == 0:
                    break
                depth -= 1
            i += 1
        if depth:
            return None
    destination_end = i
    while i < len(text) and text[i].isspace():
        i += 1
    if i < len(text) and text[i] == ")":
        return i
    if i == destination_end or i == len(text) or text[i] not in "\"'(":
        return None
    closing = ")" if text[i] == "(" else text[i]
    i += 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == closing:
            i += 1
            break
        if closing == ")" and text[i] == "(":
            return None  # Unescaped nested parentheses are not a valid title.
        i += 1
    while i < len(text) and text[i].isspace():
        i += 1
    return i if i < len(text) and text[i] == ")" else None


def destination(text, start):
    """Read a destination token, angle delimited or with balanced parentheses."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start < len(text) and text[start] == "<":
        end = text.find(">", start + 1)
        return text[start + 1:end] if end >= 0 else None
    i, depth = start, 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            i += 2
            continue
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            if depth == 0:
                break
            depth -= 1
        if text[i].isspace() and depth == 0:
            break
        i += 1
    return re.sub(r"\\([() <>])", r"\1", text[start:i])


def reference_key(value):
    return " ".join(value.split()).casefold()


def parse_markdown(raw):
    text = visible_text(raw)
    document, references = Document(), {}
    heading_counts = Counter()
    lines = text.splitlines(keepends=True)
    for number, line in enumerate(lines, 1):
        definition = re.match(r"^ {0,3}\[([^\]]+)\]:\s*(.*)$", line)
        if definition:
            target = destination(definition[2], 0)
            references[reference_key(definition[1])] = target
            lines[number - 1] = "\n" if line.endswith("\n") else ""
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            # Plain ATX heading slugs only; rich heading rendering is out of scope.
            slug = "".join(c for c in heading[1].lower() if c in " -_" or unicodedata.category(c)[0] in "LN")
            slug = slug.replace(" ", "-")
            count = heading_counts[slug]
            heading_counts[slug] += 1
            document.anchors.add(slug + (f"-{count}" if count else ""))
    text = "".join(lines)
    HTMLLinks(document).feed(text)
    i = 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] != "[":
            i += 1
            continue
        end = balanced_end(text, i, "[", "]")
        if end is None:
            i += 1
            continue
        label, after, line = text[i + 1:end], end + 1, text.count("\n", 0, i) + 1
        if after < len(text) and text[after] == "(":
            close = inline_link_end(text, after)
            if close is not None:
                target = destination(text[after + 1:close], 0)
                document.links.append((target, line))
                i = close + 1
                continue
        elif after < len(text) and text[after] == "[":
            close = text.find("]", after + 1)
            if close >= 0:
                key = reference_key(text[after + 1:close] or label)
                if key not in references:
                    document.errors.append(f"line {line}: undefined reference [{key}]")
                else:
                    document.links.append((references[key], line))
                i = close + 1
                continue
        # Shortcut references only count when a definition exists; [plain prose] is valid.
        key = reference_key(label)
        if key in references:
            document.links.append((references[key], line))
        i = end + 1
    return document


def local_target(root, source, destination):
    if destination is None:
        raise ValueError("invalid link destination")
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    target = (source.parent / path).resolve() if path else source.resolve()
    if path.startswith("/") or not target.is_relative_to(root):
        raise ValueError(f"outside repository: {destination}")
    return target, unquote(parsed.fragment)


def target_key(root, target, fragment):
    return target.relative_to(root).as_posix() + (f"#{fragment}" if fragment else "")


def check_repository(root):
    root = Path(root).resolve()
    errors, documents, svg_anchors = [], {}, {}
    files = sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts)
    for path in files:
        if not path.resolve().is_relative_to(root):
            errors.append(f"{path.relative_to(root)}: outside repository symlink")
            continue
        if path.suffix.lower() == ".md":
            documents[path.resolve()] = parse_markdown(path.read_text(encoding="utf-8"))
        elif path.suffix.lower() == ".svg":
            try:
                tree = ET.parse(path)
                if tree.getroot().tag.rsplit("}", 1)[-1] != "svg":
                    raise ValueError("root element is not svg")
                svg_anchors[path.resolve()] = {e.attrib["id"] for e in tree.iter() if "id" in e.attrib}
            except (ET.ParseError, ValueError) as exc:
                errors.append(f"{path.relative_to(root)}: invalid SVG: {exc}")
    linked = {}
    for path, document in documents.items():
        source = path.relative_to(root).as_posix()
        errors.extend(f"{source}: {e}" for e in document.errors)
        linked[path] = set()
        for destination_value, line in document.links:
            try:
                resolved = local_target(root, path, destination_value)
                if resolved is None:
                    continue
                target, fragment = resolved
                linked[path].add(target_key(root, target, fragment))
                if not target.exists():
                    raise ValueError(f"missing target: {destination_value}")
                if fragment and (target in documents or target in svg_anchors):
                    anchors = documents[target].anchors if target in documents else svg_anchors[target]
                    if fragment not in anchors:
                        raise ValueError(f"missing fragment: {destination_value}")
            except ValueError as exc:
                errors.append(f"{source}:{line}: {exc}")
    try:
        config = json.loads((root / "docs-check.json").read_text(encoding="utf-8"))
        if not isinstance(config, dict) or not isinstance(config.get("inventories"), list):
            raise ValueError("expected an inventories list")
        for inventory in config["inventories"]:
            entries = inventory["entries"]
            if not isinstance(entries, list) or not all(isinstance(e, str) for e in entries):
                raise ValueError("inventory entries must be strings")
            expected = set(entries)
            if len(entries) != len(expected):
                errors.append("inventory contains duplicate entries")
            if "glob" in inventory:
                actual = {p.relative_to(root).as_posix() for p in root.glob(inventory["glob"]) if p.is_file()}
            else:
                anchor_file = (root / inventory["anchor_file"]).resolve()
                actual = {f'{inventory["anchor_file"]}#{anchor}' for anchor in documents.get(anchor_file, Document()).anchors if anchor.startswith(inventory["anchor_prefix"])}
            if actual != expected:
                errors.append(f"inventory differs: missing={sorted(expected - actual)}, unlisted={sorted(actual - expected)}")
            for entry in entries:
                resolved = local_target(root, root / "docs-check.json", entry)
                if resolved is None:
                    raise ValueError("inventory entries must be local")
                target, fragment = resolved
                if not target.is_file():
                    errors.append(f"inventory missing target: {entry}")
                elif fragment and fragment not in documents.get(target, Document()).anchors:
                    errors.append(f"inventory missing fragment: {entry}")
            for navigation in inventory["navigation"]:
                nav = (root / navigation).resolve()
                absent = expected - linked.get(nav, set())
                if absent:
                    errors.append(f"{navigation}: navigation missing: {sorted(absent)}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"docs-check.json: invalid manifest: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_repository(args.root)
    for error in errors:
        print(error)
    if not errors:
        print("Documentation links, SVG assets and declared inventories passed.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
