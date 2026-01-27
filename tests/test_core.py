import sys
import os

# 1. 解决路径问题：强行告诉 Python 去上一级目录的 src 里找代码
# 这两行代码必须放在 import abtest_lab 之前！
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 2. 解决名字问题：注意这里导入的是 quick_z_test (和你 core.py 里定义的一样)
from abtest_lab.core import quick_z_test

def test_z_test_basic():
    """
    测试 A/B 测试的核心计算逻辑
    """
    # 场景：A组1000人50转化(5%)，B组1000人70转化(7%)
    # 注意：这里调用时也要用 quick_z_test
    z, p = quick_z_test(50, 1000, 80, 1000)
    
    print(f"Z-score: {z}")
    print(f"P-value: {p}")
    
    # 断言检查：
    # 1. B组转化率高，P值应该很小（显著）
    assert p < 0.05
    # 2. P值必须在 0 到 1 之间
    assert 0 <= p <= 1