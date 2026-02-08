# abtest-lab

> 一个abtest测试项目，测试是运气好还是实力佳
> ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
> ![License](https://img.shields.io/badge/License-MIT-green)
> ![Status](https://img.shields.io/badge/Status-Educational-orange)

## 简介 (Introduction)

## ?快速上手

```bash
git clone [https://github.com/ayanamilmy/abtest-lab.git](https://github.com/ayanamilmy/abtest-lab.git)
cd abtest-lab
pip install -e .
```

### 1.核心功能：

#### (1) 计算样本量（即如果想要测出5%的提升，需要多少样本，才可以成功划分出一条能够分辨归属的界限）

数学原理：

$$
n = \frac{\left( Z_{\alpha/2} \sqrt{2\bar{p}(1-\bar{p})} + Z_{\beta} \sqrt{p_1(1-p_1) + p_2(1-p_2)} \right)^2}{MDE^2}
$$

代码实现：

```
    p1 = baseline_rate
    p2 = baseline_rate + minimum_detectable_effect
    p_avg = (p1 + p2) / 2

    #原假设方差
    sqrt(2 * p_avg * (1 - p_avg))
    s_root_1 = (2 * p_avg * (1 - p_avg)) ** 0.5

    #备择假设方差
    sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    s_root_2 = (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5

    n = (scipy.stats.norm.ppf(1 - alpha / 2) * s_root_1 + scipy.stats.norm.ppf(power) * s_root_2)**2 / minimum_detectable_effect**2
```

#### (2) 计算双样本比例检验的 Z 值和 P 值

在 `core.py` 中，我使用了使用**混合方差 (Pooled Variance)** 的 Z 检验公式来评估两组转化率是否存在显著差异。

1.  **计算混合转化率 (`p_pool`)**:
    在零假设 ($H_0: p_a = p_b$) 下，我们假设两组没有区别，因此将样本合并计算总体转化率：
    $$\hat{p} = \frac{x_a + x_b}{n_a + n_b}$$

2.  **计算标准差 (`se`)**:
    基于混合转化率估算分布的波动范围：
    $$SE = \sqrt{\hat{p}(1 - \hat{p}) \left( \frac{1}{n_a} + \frac{1}{n_b} \right)}$$

3.  **计算 Z 值 (`z_score`)**:
    计算观测到的差异距离零假设有多少个“标准差”：
    $$Z = \frac{p_b - p_a}{SE}$$

4.  **计算 P 值 (`p_value`)**:
    双尾检验 (Two-tailed Test) 的概率：
    $$P\text{-value} = 2 \times (1 - \Phi(|Z|))$$
    _(其中 $\Phi$ 是标准正态分布的累积分布函数)_

代码实现：

```
    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))

    z_score = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
```

### 笔记 ( notes for me )

#### 1. 通俗理解

A/B 测试的本质是在两个“房间”中做判断：假设我们有两个房间，一个房间里全部都是普通人，另一个房间全都是NBA大中锋

- **H0（没用）**：就是普通人身高的均值，假设是170cm
- **H1（有用）**：就是NBA大中锋身高的均值，假设是210cm

为了区分它们，我们需要保证两个分布不重叠。

- **Z_alpha** 是为了防止普通人也有稍微高个子的被误判成NBA球星了，比如身高一米八的
- **Z_beta** 是为了防止NBA大中锋里稍微矮一点的被漏掉了

### 2. 核心公式

$$
n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \cdot \sigma^2}{MDE^2}
$$

(看这里：样本量 n 和 MDE 的平方成反比，意味着想要看到的差异越小，代价就是你所需要的样本量越大。样本量一大了，钟形曲线就更瘦了，这样即使MDE比较小，**Z_alpha** 和**Z_beta**也不会打架)

### ??开发环境

本项目采用 **Pytest** 进行测试。
运行测试命令：

```bash
python -m pytest
```

### TODO List

- [x] 完成 Z 检验核心逻辑
- [x] 完成样本量计算器
- [x] 画出精致又学术的图
