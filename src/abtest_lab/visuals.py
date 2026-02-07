import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


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


if __name__ == "__main__":
    # 自测代码：模拟调用一次 plot_z_test_result(z_score=2.5)
    plot_z_test_result(z_score=2.5)
    plt.show()