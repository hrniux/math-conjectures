# 纳维-斯托克斯存在性与光滑性 · Navier–Stokes Existence and Smoothness

> **状态**：未解决（千禧年问题） · **提出**：2000 年 · **背景方程**：19 世纪（Navier & Stokes）

## 精确陈述

以三维全空间上的无外力情形为例，固定黏性系数 $\nu>0$，考虑

$$\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,\qquad \nabla\cdot u=0,\qquad u(x,0)=u_0(x).$$

给定任意光滑、无散度的初始速度场 $u_0$，要求它及各阶导数在无穷远处快速衰减。**问题**：是否总存在对所有 $t\ge 0$ 光滑的速度 $u$ 和压力 $p$，且动能 $\int_{\mathbb R^3}|u(x,t)|^2\,dx$ 在时间上一致有界？

这里要求的是空间上的**快速衰减**，不是流速「足够快」，也不是向过去延伸的整个时间轴。Clay 的正式问题还允许周期空间上的存在性版本，或满足规定条件、可带光滑外力的失效反例版本，具体要求见原始陈述。

## 通俗解释

纳维-斯托克斯方程描述水、空气等流体的运动，从天气到飞机设计都靠它。问题在于：给定光滑的初始状态，数学解能否一直保持光滑？湍流是复杂的流动现象，不能直接等同于数学解在有限时间失去光滑性。

## 为什么重要

它是流体力学与偏微分方程理论的核心，直接关系到湍流这一经典难题能否被数学严格刻画，千禧年七大难题之一。

## 进展

二维情形已知光滑解整体存在；三维一般情形是否存在光滑解（或能否证明 blow-up）仍是完全开放的问题。

## 原始资料

- [Clay Mathematics Institute：问题介绍](https://www.claymath.org/millennium/navier-stokes-equation/)
- [Charles L. Fefferman：正式问题陈述（PDF）](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

---

← [返回目录](../README.md)
