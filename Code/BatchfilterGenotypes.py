import os
import glob
import math
import subprocess

# 遍历当前目录下所有 .geno.txt 文件
geno_files = glob.glob("*.geno.txt")

for geno_file in geno_files:
    # 提取物种名（不带后缀）
    species = geno_file.replace(".geno.txt", "")

    # 读取 header，确定样本数量
    with open(geno_file, "r") as f:
        header = f.readline().strip().split("\t")
        sample_count = len(header) - 2  # 除去 #CHROM 和 POS 两列
        min_calls = sample_count // 2

    # 构造输出文件名
    output_file = f"{species}.geno.diplo.txt"

    # 构造命令
    cmd = [
        "python", "filterGenotypes.py",
        "-i", geno_file,
        "-o", output_file,
        "-of", "diplo",
        "--minCalls", str(min_calls)
    ]

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
