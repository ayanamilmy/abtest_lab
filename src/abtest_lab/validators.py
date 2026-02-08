from scipy.stats import chisquare

def check_srm(n_a, n_b, ratio_a=0.5, ratio_b=0.5, alpha=0.01):
    """
    检查样本比率偏差 (SRM - Sample Ratio Mismatch)
    
    参数:
        n_a (int): A组实际样本量
        n_b (int): B组实际样本量
        ratio_a (float): A组预期的比例 (默认 0.5)
        ratio_b (float): B组预期的比例 (默认 0.5)
        alpha (float): 报警阈值 (默认 0.01，小于这个值就报错)
        
    返回:
        is_valid (bool): True 代表通过 (健康)，False 代表有 SRM (异常)
        p_value (float): 卡方检验的 P 值
    """
    
    # 1. 算出总人数
    total = n_a + n_b
    
    # 2. 算出“理论上应该有多少人” (Expected)
    expected_a = total * ratio_a
    expected_b = total * ratio_b
    
    # 3. 准备数据：[观察值] 和 [理论值]
    f_obs = [n_a, n_b]            # 实际跑出来的
    f_exp = [expected_a, expected_b]  # 理论上该有的
    
    # 4. 调用卡方检验 (Chi-Square Test)
    # 这一步 SciPy 会自动帮你算差距大不大
    chi2, p_value = chisquare(f_obs=f_obs, f_exp=f_exp)
    
    # 5. 【核心逻辑】条件分支
    # 如果 P 值太小，说明“实际”和“理论”差距显著 -> 有问题！
    if p_value < alpha:
        is_valid = False  # ? 失败！有 SRM！
    else:
        is_valid = True   # ? 成功！样本健康
        
    return is_valid, p_value