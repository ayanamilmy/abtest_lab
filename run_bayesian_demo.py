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
    from abtest_lab.validators import check_srm
    from abtest_lab.bayesian import calculate_bayesian_prob
    from abtest_lab.visuals import plot_bayesian_distribution
    n_a=1000
    conv_a=100
    n_b=1000
    conv_b=120
    is_valid, srm_p = check_srm(n_a, n_b)
    if is_valid==False:
        print("SRM 检测失败！样本有严重偏差")
    else:
        print("SRM 检测通过，数据健康。")
        prob, uplift = calculate_bayesian_prob(conv_a, n_a, conv_b, n_b)
        print(f" B组获胜概率: {prob:.2%}")
        print(f" 预期提升幅度: {uplift:.2%}")
        if prob > 0.95:
            print("💡 结论：胜算很大！建议全量上线！(High Confidence)")
        elif prob > 0.90:
            print("💡 结论：看起来不错，但建议再观察两天。(Medium Confidence)")
        else:
            print("💡 结论：差别不大，甚至可能 B 组更差，别瞎折腾了。(Low Confidence)")     
        plot_bayesian_distribution(conv_a, n_a, conv_b, n_b)
        plt.show()

if __name__ == "__main__":
    main()