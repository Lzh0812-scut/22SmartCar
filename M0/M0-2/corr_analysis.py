"""
皮尔逊相关系数计算模块
用途：读取 CSV 双列数据，计算其皮尔逊相关系数（取值范围 [-1, 1]）
公式：r = (n*Σxy - Σx*Σy) / sqrt((n*Σx²-Σx²)*(n*Σy²-Σy²))
异常覆盖：文件不存在、空文件、列名不匹配(缺列)、除零(零方差)
验证：引入 numpy.corrcoef 仅做结果对比，核心计算必须手写
"""

import csv
import math
import os

def load_data(file_path):
    """读取 CSV 数据。
    参数: file_path - CSV 文件路径（需含表头）
    返回: (headers, rows)
    异常: FileNotFoundError(文件不存在), ValueError(空文件)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件未找到: {file_path}")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError("空文件：CSV 文件无表头")
        rows = list(reader)
    return headers, rows

def extract_columns(rows, headers, idx1=0, idx2=1):
    """提取指定两列并转为浮点数列表。
    异常: IndexError(列名不匹配/缺列)
    """
    if max(idx1, idx2) >= len(headers):
        raise IndexError(f"列名不匹配或缺列：表头仅 {len(headers)} 列")
    col1 = [float(r[idx1]) for r in rows]
    col2 = [float(r[idx2]) for r in rows]
    return col1, col2

def calc_corr(x, y):
    """计算皮尔逊相关系数（手写核心逻辑）。
    返回: r；若长度不一致或除零(零方差)则返回 None
    """
    n = len(x)
    if n == 0 or len(y) != n:
        return None
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi**2 for xi in x)
    sum_y2 = sum(yi**2 for yi in y)
    
    # 方差项（分母核心）
    var_x = n * sum_x2 - sum_x**2
    var_y = n * sum_y2 - sum_y**2
    
    # 除零保护：某一列取值恒定 -> 方差为0 -> 相关系数无定义
    if var_x <= 0 or var_y <= 0:
        return None
        
    denom = math.sqrt(var_x * var_y)
    return (n * sum_xy - sum_x * sum_y) / denom

def verify_with_numpy(x, y):
    """使用 numpy.corrcoef 进行结果验证（不参与核心计算）。
    参数: x, y - 数值列表
    返回: numpy 计算的相关系数，若无法计算返回 None
    """
    try:
        import numpy as np
        # 仅当数据有效时验证
        if len(x) == 0 or len(x) != len(y):
            return None
        return np.corrcoef(x, y)[0, 1]
    except ImportError:
        return None

def main():
    """主入口：加载数据、提取两列、计算并输出相关系数及验证"""
    try:
        headers, rows = load_data("sample_data.csv")
        col1, col2 = extract_columns(rows, headers, 0, 1)
        r = calc_corr(col1, col2)
        
        if r is None:
            print("相关系数无定义（可能某列取值恒定/零方差或数据异常）")
        else:
            print(f"手写计算相关系数: {r}")
            # numpy 仅做验证对比
            r_np = verify_with_numpy(col1, col2)
            if r_np is not None:
                print(f"Numpy 验证相关系数: {r_np} (差异: {abs(r - r_np):.2e})")
                
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(f"运行错误: {e}")

if __name__ == "__main__":
    main()
