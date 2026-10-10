"""单元测试：覆盖已知正相关、负相关、零方差、缺列等"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corr_analysis import calc_corr, extract_columns

def test_perfect_positive():
    # [1,2,3] 与 [2,4,6] -> 1.0
    r = calc_corr([1,2,3], [2,4,6])
    assert abs(r - 1.0) < 1e-6

def test_perfect_negative():
    # [1,2,3] 与 [6,4,2] -> -1.0
    r = calc_corr([1,2,3], [6,4,2])
    assert abs(r - (-1.0)) < 1e-6

def test_zero_variance():
    # 某列恒定 -> 零方差 -> None
    r = calc_corr([1,1,1], [2,4,6])
    assert r is None

def test_zero_corr():
    # 正交示例
    r = calc_corr([1,2,3], [3,2,1])
    assert abs(r - (-1.0)) < 1e-6

if __name__ == "__main__":
    test_perfect_positive()
    test_perfect_negative()
    test_zero_variance()
    test_zero_corr()
    print("测试通过")
