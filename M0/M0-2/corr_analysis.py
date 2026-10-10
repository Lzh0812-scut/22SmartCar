"""
皮尔逊相关系数计算模块
用途：读取 CSV 双列数据，计算其皮尔逊相关系数（取值范围 [-1, 1]）
公式：r = (n*Σxy - Σx*Σy) / sqrt((n*Σx²-Σx²)*(n*Σy²-Σy²))
"""

import csv
import math
import os

def load_data(file_path):
    """读取 CSV 数据。
    参数: file_path - CSV 文件路径（需含表头）
    返回: (headers, rows)，headers 为表头列表，rows 为数据行列表
    异常: FileNotFoundError 当文件不存在时抛出
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件未找到: {file_path}")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows

def calc_corr(x, y):
    """计算皮尔逊相关系数。
    参数: x, y - 等长度数值列表
    返回: 相关系数 r（分母异常或长度不一致时返回 0.0）
    """
    n = len(x)
    if n == 0 or len(y) != n:
        return 0.0
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi**2 for xi in x)
    sum_y2 = sum(yi**2 for yi in y)
    denom = (n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2)
    if denom <= 0:
        return 0.0
    return (n * sum_xy - sum_x * sum_y) / math.sqrt(denom)

def main():
    """主入口：加载数据、提取两列、计算并输出相关系数"""
    headers, rows = load_data("sample_data.csv")
    col1 = [float(r[0]) for r in rows]
    col2 = [float(r[1]) for r in rows]
    r = calc_corr(col1, col2)
    print(f"相关系数: {r}")

if __name__ == "__main__":
    main()
