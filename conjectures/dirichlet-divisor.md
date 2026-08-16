# 迪利克雷除数问题 · Dirichlet Divisor Problem

> **状态**：未解决 · **提出**：1849 年 · **提出者**：Peter Gustav Lejeune Dirichlet

## 精确陈述

设 $d(n)$ 为 $n$ 的因子个数，$D(x) = \sum_{n \le x} d(n)$。已知

$$D(x) = x \ln x + (2\gamma - 1)x + O(x^{\theta})$$

**问题**：最优的 $\theta$ 是多少？**猜想**：$\theta = \frac{1}{4} + \varepsilon$。

## 通俗解释

前 $x$ 个数的因子个数之和，主项是 $x\ln x$，但「误差」能小到什么程度？这是除数函数求和的核心问题，与高斯圆问题、黎曼猜想都有联系。

## 为什么重要

它是解析数论「求和误差估计」的经典难题，与 $\zeta$ 函数的零点分布直接相关。

## 进展

目前已知 $\theta \le \frac{131}{416} \approx 0.315$；$\theta = \frac{1}{4}$ 仍是猜想。

---

← [返回目录](../README.md)
