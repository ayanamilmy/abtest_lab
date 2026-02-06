import sys
import os
import pytest
import math

# 让测试代码能找到上一层的 src 代码
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from abtest_lab.tools import calculate_sample_size

def test_sample_size_calculation():
    """
    测试正常情况：
    Baseline: 20% (0.2)
    MDE: 5% (0.05) -> 目标 25%
    Power: 0.8
    Alpha: 0.05
    """
    n = calculate_sample_size(0.2, 0.05, power=0.8, alpha=0.05)
    print(f"Calculated Sample Size: {n}")
    
    # 工业界标准结果大约在 1030-1090 之间（取决于具体公式细节）
    # 只要落在这个区间，说明你的数学逻辑是对的
    assert 1000 < n < 1100

def test_input_validation():
    """
    测试异常情况：你的防御性编程起作用了吗？
    """
    # 1. 转化率大于 1，应该报错
    with pytest.raises(ValueError):
        calculate_sample_size(1.5, 0.05)
    
    # 2. Power 必须在 0-1 之间
    with pytest.raises(ValueError):
        calculate_sample_size(0.5, 0.05, power=1.2)