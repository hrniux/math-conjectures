# abc 猜想 · abc Conjecture

> **状态**：有争议（望月新一 2012 年声称证明，尚未获广泛认可） · **提出**：1985 年 · **提出者**：Joseph Oesterlé & David Masser

## 精确陈述

定义 $\mathrm{rad}(n)$ 为 $n$ 的互异质因子之积（如 $\mathrm{rad}(12) = 2 \times 3 = 6$）。

**猜想**：对任意 $\varepsilon > 0$，存在常数 $K_\varepsilon$，使得对所有互素的正整数 $a, b, c$（满足 $a + b = c$）都有

$$c < K_\varepsilon \cdot \mathrm{rad}(abc)^{1 + \varepsilon}$$

## 通俗解释

大整数可能由少数质数的高次幂组成，因而其质因子之积远小于整数本身。abc 猜想限制的是：在 $a+b=c$ 且三者互素时，$c$ 相对**三者全部不同质因子的乘积**能有多大。这里不能说 $c$ 会继承 $a,b$ 的质因子；互素条件恰好意味着三者没有共同的质因子。

## 为什么重要

它极其深刻——若成立，可一举推出费马大定理（对充分大的指数）、以及众多其他数论难题的简化证明。

## 具体例子

取 $a = 1, b = 8, c = 9$：$\mathrm{rad}(abc) = \mathrm{rad}(72) = 2 \times 3 = 6$，而 $c = 9 > 6$。它说明简单的不等式 $c\le\mathrm{rad}(abc)$ 并不成立，**不是 abc 猜想的反例**；猜想允许依赖于 $\varepsilon$ 的常数 $K_\varepsilon$ 和指数 $1+\varepsilon$。

## 进展

2012 年望月新一提出基于「宇宙际 Teichmüller 理论」的证明，篇幅极巨、高度原创，但数学界至今未能就其正确性达成共识。

---

← [返回目录](../README.md)
