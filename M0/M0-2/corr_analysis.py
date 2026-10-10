import csv
import math

def load_data(file_path):
    """读取CSV数据，返回表头与行数据"""
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows

def calc_corr(x, y):
    """计算皮尔逊相关系数（已补 sqrt）"""
    n = len(x)
    if n == 0:
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
    headers, rows = load_data("sample_data.csv")
    col1 = [float(r[0]) for r in rows]
    col2 = [float(r[1]) for r in rows]
    r = calc_corr(col1, col2)
    print(f"相关系数: {r}")

if __name__ == "__main__":
    main()
