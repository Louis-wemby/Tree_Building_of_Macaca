import os
import math
import argparse
import subprocess
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="批量调用 parseVCF.py，使用每个物种样本的DP值确定过滤阈值")
    parser.add_argument("-i", "--input_dir", required=True, help="VCF文件目录")
    parser.add_argument("-d", "--depth_file", required=True, help="depth.txt文件路径")
    parser.add_argument("-o", "--output_dir", required=True, help="输出目录（保存 .geno.txt 文件）")
    parser.add_argument("--parser_script", default="parseVCF.py", help="parseVCF.py脚本路径（默认当前目录）")
    return parser.parse_args()

def main():
    args = parse_args()

    input_dir = args.input_dir
    depth_file = args.depth_file
    output_dir = args.output_dir
    parser_script = args.parser_script

    os.makedirs(output_dir, exist_ok=True)

    # 读取 depth.txt，按物种分组采集 DP 信息
    species_dp = defaultdict(list)
    with open(depth_file, "r") as f:
        for line in f:
            if line.strip() == "":
                continue
            species, sample, chrom, dp = line.strip().split()
            species_dp[species].append(float(dp))

    # 逐物种构造命令
    for species, dplist in species_dp.items():
        min_dp = math.floor(min(dplist) / 2)
        max_dp = math.ceil(max(dplist) * 2)

        input_file = os.path.join(input_dir, f"{species}.vcf.gz")
        output_file = os.path.join(output_dir, f"{species}.geno.txt")

        if not os.path.exists(input_file):
            print(f"[Pass] VCF file not found：{input_file}")
            continue

        cmd = [
            "python", parser_script,
            "-i", input_file,
            "-o", output_file,
            "--gtf", "flag=DP",
            f"min={min_dp}",
            f"max={max_dp}"
        ]

        print(f"[Running] {species}: min_DP={min_dp}, max_DP={max_dp}")
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
