import os
import math
import glob
import argparse
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="批量调用 filterGenotypes.py 对多个物种的 .geno 文件进行 minCalls 过滤和 diplo 输出")
    parser.add_argument("-i", "--input_dir", required=True, help="输入目录，包含 .geno.txt 文件")
    parser.add_argument("-o", "--output_dir", required=True, help="输出目录，用于存放 .geno.diplo.txt 文件")
    parser.add_argument("--filter_script", default="filterGenotypes.py", help="filterGenotypes.py 脚本路径（默认在当前目录）")
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    geno_files = glob.glob(os.path.join(args.input_dir, "*.geno.txt"))

    for geno_file in geno_files:
        species = os.path.basename(geno_file).replace(".geno.txt", "")

        # 获取样本数
        with open(geno_file, "r") as f:
            header = f.readline().strip().split("\t")
            sample_count = len(header) - 2
            min_calls = sample_count // 2

        output_file = os.path.join(args.output_dir, f"{species}.geno.diplo.txt")

        cmd = [
            "python", args.filter_script,
            "-i", geno_file,
            "-o", output_file,
            "-of", "diplo",
            "--minCalls", str(min_calls)
        ]

        print(f"Running：{' '.join(cmd)}")
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
