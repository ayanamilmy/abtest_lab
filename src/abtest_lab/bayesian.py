import numpy as np
def calculate_bayesian_prob(conv_a, n_a, conv_b, n_b, num_simulations=100000):
    alpha_a=conv_a+1
    beta_a=n_a-conv_a+1

    alpha_b = conv_b + 1
    beta_b = n_b - conv_b + 1

    #蒙特卡洛模拟
    samples_a=np.random.beta(alpha_a,beta_a,num_simulations)
    #电脑，请根据 A 组目前的表现（成功了 alpha 次，失败了 beta 次），帮我脑补出 10 万个‘A 组真实的转化率’可能是多少
    samples_b=np.random.beta(alpha_b,beta_b,num_simulations)
    #一样

    prob_b_wins = (samples_b > samples_a).mean()

    uplift = (samples_b - samples_a) / samples_a 
    
    expected_uplift = uplift.mean()

    return prob_b_wins, expected_uplift