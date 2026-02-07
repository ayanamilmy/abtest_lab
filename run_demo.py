import sys
import os
import matplotlib.pyplot as plt
def main():
    # 1. 解决路径问题：强行告诉 Python 去 src 里找代码
    current_path = os.path.dirname(__file__)
    # 拼接路径
    src_path = os.path.abspath(os.path.join(current_path, 'src'))
    # python的搜索路径是一个列表，我们把 src_path 插入到这个列表的最前面，这样 Python 就会优先在 src 里找代码了。
    sys.path.insert(0, src_path)

    # 从不同的Python文件中导入需要的函数
    from abtest_lab.tools import calculate_sample_size # 计算样本量
    from abtest_lab.core import quick_z_test # Z_检验
    from abtest_lab.visuals import plot_z_test_result # 可视化

    # 策划实验
    baseline_rate=0.1 # 基准转化率
    mde=0.01
    n=calculate_sample_size( baseline_rate,0.01,0.05 )
    print("我们需要的样本数量至少为")
    print(n)

    # 模拟一下，自己做一个假数据
    n_a=n
    conv_a = int(n_a * baseline_rate)
    n_b = n
    #expected_rate_b = baseline_rate * (1 + mde)
    #conv_b = int(n_b * (expected_rate_b) ) # 说实话有点蠢
    conv_b = conv_a*2
    # 传入第一天写的那个简单的Z检验函数
    z_score, p_value=quick_z_test(conv_a, n_a, conv_b, n_b)
    print(f"Z值是: {z_score}")
    print(f"P值是: {p_value}")
    if(p_value < 0.05):
        print("很好，有明显提升！")
    else:
        print("在当前显著性水平5%下，无法断言有明显提升")

    # 画个图
    plot_z_test_result(z_score)
    plt.show()


if __name__ == "__main__":
    main()