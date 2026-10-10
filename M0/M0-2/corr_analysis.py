"""
皮尔逊相关系数计算模块（入口脚本）
用途：通过 --config 读取 yaml（含 input_csv），计算并输出 r = <数值>
公式：手写皮尔逊相关系数，numpy 仅做验证（不参与核心计算）
异常：文件不存在/空文件/缺列/零方差 -> 可读信息 + 非0退出（无 Traceback）
"""

import argparse
import csv
import math
import os
import sys

def load_yaml(path):
    """简易 yaml 解析（避免额外依赖，支持 input_csv 字段）"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件未找到: {path}")
    cfg = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg

def resolve_csv_path(yaml_path, input_csv):
    """解析 csv 路径：优先相对 yaml 所在目录，否则相对当前工作目录"""
    yaml_dir = os.path.dirname(os.path.abspath(yaml_path))
    candidate = os.path.join(yaml_dir, input_csv)
    if os.path.exists(candidate):
        return candidate
    return input_csv  # 回退到当前工作目录

def load_data(file_path):
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
    if max(idx1, idx2) >= len(headers):
        raise IndexError(f"列名不匹配或缺列：表头仅 {len(headers)} 列")
    col1 = [float(r[idx1]) for r in rows]
    col2 = [float(r[idx2]) for r in rows]
    return col1, col2

def calc_corr(x, y):
    """手写皮尔逊核心逻辑"""
    n = len(x)
    if n == 0 or len(y) != n:
        return None
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi**2 for xi in x)
    sum_y2 = sum(yi**2 for yi in y)
    var_x = n * sum_x2 - sum_x**2
    var_y = n * sum_y2 - sum_y**2
    if var_x <= 0 or var_y <= 0:
        return None  # 零方差（某列恒定）
    denom = math.sqrt(var_x * var_y)
    return (n * sum_xy - sum_x * sum_y) / denom

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='yaml 配置文件路径')
    args = parser.parse_args()
    try:
        cfg = load_yaml(args.config)
        if 'input_csv' not in cfg:
            print("错误：yaml 缺少 input_csv 字段", file=sys.stderr)
            sys.exit(1)
        csv_path = resolve_csv_path(args.config, cfg['input_csv'])
        headers, rows = load_data(csv_path)
        col1, col2 = extract_columns(rows, headers, 0, 1)
        r = calc_corr(col1, col2)
        if r is None:
            print("错误：相关系数无定义（可能某列取值恒定/零方差或数据异常）", file=sys.stderr)
            sys.exit(1)
        print(f"r = {r}")
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
