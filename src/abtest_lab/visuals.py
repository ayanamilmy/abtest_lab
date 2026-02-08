import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, beta


def plot_z_test_result(z_score, alpha=0.05):
    """
    绘制标准正态分布，并标出拒绝域和观测到的 Z 值。
    :param z_score: 实验计算出的 Z 统计量
    :param alpha: 显著性水平 (默认 0.05)
    """
    # 生成 X 轴数据点
    x = np.linspace(-4, 4, 1000)
    y = norm.pdf(x)
    
    # 创建图形
    plt.figure(figsize=(10, 6))
    
    # 绘制标准正态分布曲线
    plt.plot(x, y, 'k-', linewidth=2, label='Standard Normal Distribution')
    
    # 计算临界值（双尾检验）
    critical_value = norm.ppf(1 - alpha / 2)
    
    # 填充拒绝域（右侧）- 只在第一个区域添加标签
    right_reject = x > critical_value
    plt.fill_between(x[right_reject], 0, y[right_reject],
                     color='red', alpha=0.3, label='Rejection Region')
    
    # 填充拒绝域（左侧）- 不添加标签避免重复
    left_reject = x < -critical_value
    plt.fill_between(x[left_reject], 0, y[left_reject],
                     color='red', alpha=0.3)
    
    # 绘制观测到的 Z 值
    plt.axvline(x=z_score, color='blue', linestyle='--', linewidth=2, 
                label='Observed Z')
    
    # 添加垂直线标记临界值
    plt.axvline(x=critical_value, color='gray', linestyle=':', linewidth=1, 
                alpha=0.7, label=f'Critical Value (±{critical_value:.3f})')
    plt.axvline(x=-critical_value, color='gray', linestyle=':', linewidth=1, 
                alpha=0.7)
    
    # 判断是否显著
    is_significant = abs(z_score) > critical_value
    result_text = "Result: Significant!" if is_significant else "Result: Not Significant"
    
    # 添加标题和标签
    plt.title(f'Z-Test Result Visualization\n{result_text}', fontsize=14, fontweight='bold')
    plt.xlabel('Z-score', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 设置 X 轴范围
    plt.xlim(-4, 4)
    
    # 显示图形
    plt.tight_layout()


def plot_bayesian_distribution(conv_a, n_a, conv_b, n_b, alpha=0.05, figsize=(10, 6)):
    """
    绘制 A/B 两组的 Beta 分布曲线，展示后验分布。
    
    :param conv_a: A 组转化数
    :param n_a: A 组总样本数
    :param conv_b: B 组转化数
    :param n_b: B 组总样本数
    :param alpha: 先验参数（默认 0.05，用于 Beta 先验）
    :param figsize: 图形尺寸
    """
    # 计算 Beta 分布参数（使用均匀先验 Beta(1,1)）
    alpha_a = conv_a + 1
    beta_a = n_a - conv_a + 1
    alpha_b = conv_b + 1
    beta_b = n_b - conv_b + 1
    
    # 生成 x 轴数据点（根据数据自动聚焦）
    # 确定 x 轴范围：覆盖两个分布的主要概率区域
    x_min = 0.0
    x_max = 1.0
    # 使用 Beta 分布的众数附近扩展
    mode_a = (alpha_a - 1) / (alpha_a + beta_a - 2) if alpha_a + beta_a > 2 else 0.5
    mode_b = (alpha_b - 1) / (alpha_b + beta_b - 2) if alpha_b + beta_b > 2 else 0.5
    # 计算标准差以确定范围
    std_a = np.sqrt((alpha_a * beta_a) / ((alpha_a + beta_a) ** 2 * (alpha_a + beta_a + 1)))
    std_b = np.sqrt((alpha_b * beta_b) / ((alpha_b + beta_b) ** 2 * (alpha_b + beta_b + 1)))
    # 扩展范围
    lower = max(0.0, min(mode_a - 4 * std_a, mode_b - 4 * std_b))
    upper = min(1.0, max(mode_a + 4 * std_a, mode_b + 4 * std_b))
    # 确保有足够的宽度
    if upper - lower < 0.1:
        center = (lower + upper) / 2
        lower = max(0.0, center - 0.05)
        upper = min(1.0, center + 0.05)
    x = np.linspace(lower, upper, 1000)
    
    # 计算概率密度
    pdf_a = beta.pdf(x, alpha_a, beta_a)
    pdf_b = beta.pdf(x, alpha_b, beta_b)
    
    # 创建图形
    plt.figure(figsize=figsize)
    
    # 绘制曲线
    plt.plot(x, pdf_a, 'b-', linewidth=2, label=f'Group A (α={alpha_a:.1f}, β={beta_a:.1f})')
    plt.plot(x, pdf_b, 'r-', linewidth=2, label=f'Group B (α={alpha_b:.1f}, β={beta_b:.1f})')
    
    # 填充曲线下方区域
    plt.fill_between(x, pdf_a, alpha=0.3, color='blue')
    plt.fill_between(x, pdf_b, alpha=0.3, color='red')
    
    # 添加标题和标签
    plt.title('Bayesian Beta Distribution for A/B Test', fontsize=14, fontweight='bold')
    plt.xlabel('Conversion Rate', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 自动调整 x 轴范围
    plt.xlim(lower, upper)
    
    plt.tight_layout()


if __name__ == "__main__":
    # 自测代码：模拟调用一次 plot_z_test_result(z_score=2.5)
    plot_z_test_result(z_score=2.5)
    plt.show()