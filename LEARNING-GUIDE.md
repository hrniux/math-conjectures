# 学习导航：先选问题，再看结论

[返回总目录](README.md) · [维护与离线检查](CONTRIBUTING.md)

本页把现有 64 个条目串成可执行的学习路线。主题归类是阅读建议，同一个问题可能跨多个领域；这里不提供猜想的证明，也不重新认证每篇条目的最新研究进展。涉及前沿状态时，先读条目的精确陈述和来源，再核查原论文。

## 先分清“解决”是什么意思

| 标记 | 阅读时应问的问题 | 本库例子 |
|---|---|---|
| 开放 | 原命题是否仍没有公认的证明或反例？有限计算不能替代全称证明。 | [哥德巴赫](conjectures/goldbach.md)、[P vs NP](conjectures/p-vs-np.md) |
| 已证明 | 哪些假设下结论成立？证明一个特例不等于证明原命题。 | [素数无穷多](conjectures/euclid-infinite-primes.md)、[庞加莱](conjectures/poincare.md) |
| 已否定 | 一个满足前提却违反结论的反例，就足以否定全称命题。 | [哥德巴赫另一猜想](conjectures/goldbach-other.md) |
| 不可能性已证 | “不能完成”本身是证明得到的结论，要注明允许的工具或算法模型。 | [倍立方](conjectures/doubling-cube.md)、[停机问题](conjectures/halting-problem.md) |
| 相对公理独立 | 这是对所选公理体系的结论；在 ZFC 一致的前提下，ZFC 既不能证明 CH，也不能证明其否定。不是一般意义上的“还没解出”。 | [连续统假设](conjectures/continuum-hypothesis.md) |
| 部分结论 / 证明有争议 | 要拆开“已证的子问题”和“仍需论证的原问题”；不能把声称的证明当成已获公认的定理。 | [华林问题](conjectures/warings-problem.md)、[abc](conjectures/abc.md) |
| 常数 / 恒等式 | 一个对象有已知性质，也可以附带未决问题；常数本身不是猜想。 | [π](conjectures/pi.md)与[π 的正规性](conjectures/normality-of-pi.md) |

千禧年问题的分类以 [Clay 官方清单](https://www.claymath.org/millennium-problems/)为起点：其页面分别列出活动问题和已解决的庞加莱问题。CH 的独立性可沿 [Cohen 原论文（1963）](https://pmc.ncbi.nlm.nih.gov/articles/PMC221287/)继续读；这里的相对一致性前提不能省略。算法不可能性可回到 [Turing 原论文（1936，DOI）](https://doi.org/10.1112/plms/s2-42.1.230)核对其计算模型。

## 按目标选一条起步路线

以下时间是编辑估计，只供短次学习安排，不是读完证明的承诺。

| 你的目标与前置知识 | 建议顺序 | 一次学习的交付物与停止点 |
|---|---|---|
| 想读懂一个证明；会整除、分数即可；约 45–60 分钟 | [√2 无理性](conjectures/sqrt2.md) → [素数无穷多](conjectures/euclid-infinite-primes.md) → [费马小定理](conjectures/fermats-little-theorem.md) | 写出前两个证明的反设与矛盾点；第三篇先验证模 7 的例子。若不熟悉模运算，停在例子并补基础。 |
| 喜欢编程实验；会循环、整数运算；约 60 分钟 | [考拉兹](conjectures/collatz.md) → [哥德巴赫另一猜想](conjectures/goldbach-other.md) → [π 的正规性](conjectures/normality-of-pi.md) | 记录实验范围、边界与结果；解释“找到反例”和“范围内未找到反例”为何不同。不要把有限位数统计称为正规性的证明。 |
| 想从图形进入抽象；会平面几何；约 45–60 分钟 | [毕达哥拉斯](conjectures/pythagorean.md) → [欧拉多面体](conjectures/euler-polyhedron.md) → [七桥](conjectures/seven-bridges.md) → [四色](conjectures/four-color.md) | 为一个多面体数 V、E、F，把一张桥图改写成顶点与边；写明公式/模型的适用条件。先理解陈述，不要求复现四色证明。 |
| 想区分“算不出”与“算得慢”；会算法与渐近记号；约 60–90 分钟 | [停机问题](conjectures/halting-problem.md) → [P vs NP](conjectures/p-vs-np.md) → [AKS](conjectures/aks-primality.md) | 各写一句输入、输出和模型；区分判定不可计算、复杂度未知、已知多项式算法。不要从停机不可判定推导 P≠NP。 |
| 想继续读研究陈述；已有复分析 / 微分几何 / PDE 基础 | 从下方主题选一组，再读条目的原始来源 | 列出陌生定义，选一个局部目标：能逐项解释假设。未掌握背景时先补课，不把通俗解释当研究级证明。 |

## 全部条目的主题地图

每个条目在此出现一次，便于按兴趣选读；问题状态请结合上方分类、总目录与条目说明阅读。

| 主题与建议背景 | 条目 |
|---|---|
| 整除、同余与素数形状；从初等数论开始 | [素数无穷多](conjectures/euclid-infinite-primes.md) · [费马小定理](conjectures/fermats-little-theorem.md) · [二次互反律](conjectures/quadratic-reciprocity.md) · [伯特兰公设](conjectures/bertrand.md) · [梅森素数](conjectures/mersenne-primes.md) · [费马数](conjectures/fermat-numbers.md) · [阿廷猜想](conjectures/artins-conjecture.md) · [奇完全数](conjectures/odd-perfect-numbers.md) · [Aliquot 序列](conjectures/aliquot-sequences.md) |
| 素数分布与间隔；先理解素数计数，再补复分析 | [素数定理](conjectures/prime-number-theorem.md) · [黎曼猜想](conjectures/riemann-hypothesis.md) · [广义黎曼猜想](conjectures/grh.md) · [孪生素数](conjectures/twin-prime.md) · [勒让德](conjectures/legendre.md) · [安德丽卡](conjectures/andrica.md) · [克拉梅尔](conjectures/cramer.md) · [布尼亚科夫斯基](conjectures/bunyakovsky.md) · [兰道第四问题](conjectures/landau-fourth-problem.md) · [哈代–利特尔伍德](conjectures/hardy-littlewood.md) · [西格尔零点](conjectures/siegel-zeros.md) · [林德洛夫](conjectures/lindelof.md) |
| 整数方程、表示与迭代；注意全称与存在量词 | [哥德巴赫](conjectures/goldbach.md) · [哥德巴赫另一猜想](conjectures/goldbach-other.md) · [费马大定理](conjectures/fermats-last-theorem.md) · [卡塔兰](conjectures/catalan.md) · [拉马努金–纳格尔](conjectures/ramanujan-nagell.md) · [华林问题](conjectures/warings-problem.md) · [埃尔德什–施特劳斯](conjectures/erdos-straus.md) · [比尔](conjectures/beal.md) · [abc](conjectures/abc.md) · [布罗卡尔](conjectures/brocard.md) · [埃尔德什–莫泽](conjectures/erdos-moser.md) · [考拉兹](conjectures/collatz.md) |
| 常数与计数误差；极限、级数及渐近记号 | [√2](conjectures/sqrt2.md) · [e](conjectures/e.md) · [π](conjectures/pi.md) · [黄金比例](conjectures/golden-ratio.md) · [欧拉恒等式](conjectures/euler-identity.md) · [γ 的无理性](conjectures/euler-mascheroni.md) · [π 的正规性](conjectures/normality-of-pi.md) · [高斯圆问题](conjectures/gauss-circle.md) · [迪利克雷除数问题](conjectures/dirichlet-divisor.md) |
| 几何、图论与尺规；先画图并注明规则 | [毕达哥拉斯](conjectures/pythagorean.md) · [欧拉多面体](conjectures/euler-polyhedron.md) · [七桥](conjectures/seven-bridges.md) · [四色](conjectures/four-color.md) · [三等分角](conjectures/angle-trisection.md) · [倍立方](conjectures/doubling-cube.md) · [化圆为方](conjectures/squaring-circle.md) · [开普勒](conjectures/kepler.md) · [高斯–邦内](conjectures/gauss-bonnet.md) |
| 拓扑与代数几何；流形、曲率或代数曲线背景 | [庞加莱](conjectures/poincare.md) · [几何化](conjectures/geometrization.md) · [四维光滑庞加莱](conjectures/smooth-poincare.md) · [霍奇](conjectures/hodge.md) · [BSD](conjectures/birch-swinnerton-dyer.md) · [莫德尔](conjectures/mordell.md) |
| 计算、逻辑与公理；算法模型和形式系统 | [停机问题](conjectures/halting-problem.md) · [P vs NP](conjectures/p-vs-np.md) · [AKS](conjectures/aks-primality.md) · [哥德尔不完备](conjectures/godel-incompleteness.md) · [连续统假设](conjectures/continuum-hypothesis.md) |
| 数学物理与 PDE；分析、偏微分方程或量子场论背景 | [纳维–斯托克斯](conjectures/navier-stokes.md) · [杨–米尔斯质量间隙](conjectures/yang-mills.md) |

最后一组建议直接对照 [Clay / Fefferman 正式 Navier–Stokes 陈述](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)：把维数、初值、黏性、外力、时间范围和能量条件逐项写下来，再回读通俗说明。不同表述的条件不可拼接成另一个问题。
