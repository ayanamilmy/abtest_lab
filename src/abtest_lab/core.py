import numpy as np
from scipy import stats

def quick_z_test(conv_a, n_a, conv_b, n_b):
    """
    计算双样本比例检验的 Z 值和 P 值
    """
    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))

    z_score = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return z_score, p_value
 