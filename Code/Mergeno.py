import os
import glob
import argparse
import pandas as pd
from functools import reduce

def load_sample_name_map(mapping_file):
    """读取样本名映射文件"""
    name_map = {}
    with open(mapping_file, "r") as f:
        for line in f:
            if line.strip() == "":
                continue
            old, new = line.strip().split()
            name_map[old] = new
    return name_map

def parse_args():
    parser = argparse.ArgumentParser(description="合并多个 .geno 文件，样本名重命名，按位点对齐，缺失填N")
    parser.add_argument("-i", "--input_dir", required=True, help="输入目录，包含多个 .geno 文件")
    parser.add_argument("-s", "--sample_map", required=True, help="样本名映射文件，每行原名 新名")
    parser.add_argument("-o", "--output_file", default="merged.geno.txt", help="输出合并后的文件名")
    return parser.parse_args()

def main():
    args = parse_args()

    sample_map = load_sample_name_map(args.sample_map)
    geno_files = glob.glob(os.path.join(args.input_dir, "*.geno"))
    df_list = []

    for file in geno_files:
        fname = os.path.basename(file)
        df = pd.read_csv(file, sep="\t")

        # 重命名样本列
        renamed_cols = []
        for col in df.columns:
            if col in ['#CHROM', 'POS']:
                renamed_cols.append(col)
            else:
                renamed_cols.append(sample_map.get(col, col))  # 如果没找到映射就保留原名
        df.columns = renamed_cols

        df_list.append(df)

    # 合并所有文件，按CHROM+POS对齐
    merged_df = reduce(lambda l, r: pd.merge(l, r, on=["#CHROM", "POS"], how="outer"), df_list)

    merged_df.fillna("N", inplace=True)

    merged_df.to_csv(args.output_file, sep="\t", index=False)
    print(f"Files merged，output file：{args.output_file}")

if __name__ == "__main__":
    main()
