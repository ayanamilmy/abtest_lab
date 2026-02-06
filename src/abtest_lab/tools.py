from scipy.stats import norm
import math

import scipy


def calculate_sample_size(baseline_rate:float, minimum_detectable_effect:float, power=0.8, alpha=0.05):
    

    if not (0 < baseline_rate < 1):
        raise ValueError("Baseline rate must be between 0 and 1.")
    if not (0 < minimum_detectable_effect < 1):
        raise ValueError("Minimum detectable effect must be between 0 and 1.")
    if not (0 < power < 1):
        raise ValueError("Power must be between 0 and 1.")
    if not (0 < alpha < 1):    
        raise ValueError("Alpha must be between 0 and 1.")
# 定义 p1 和 p2，彻底消灭括号地狱
    p1 = baseline_rate
    p2 = baseline_rate + minimum_detectable_effect
    p_avg = (p1 + p2) / 2

    # s_root_1 (零假设下的标准差)
    # 公式：sqrt(2 * p_avg * (1 - p_avg))
    s_root_1 = (2 * p_avg * (1 - p_avg)) ** 0.5
    
    # s_root_2 (备择假设下的标准差)
    # 公式：sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    # 看！现在这里清爽多了，绝对不会算错顺序
    s_root_2 = (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5

    # 计算 n
    n = (scipy.stats.norm.ppf(1 - alpha / 2) * s_root_1 + scipy.stats.norm.ppf(power) * s_root_2)**2 / minimum_detectable_effect**2

    return math.ceil(n)

    