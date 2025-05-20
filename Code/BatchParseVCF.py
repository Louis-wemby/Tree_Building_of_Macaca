import os
import math
import subprocess
from collections import defaultdict

# 路径设置
input_dir = "/absolute/path/to/vcf_files"       # VCF文件目录
depth_file = "/absolute/path/to/depth.txt"    # DP测序深度文件
output_dir = "/absolute/path/to/output_files"       # 输出目录

# 读取 depth.txt，按物种分组采集 DP 信息
species_dp = defaultdict(list)

with open(depth_file, "r") as f:
    for line in f:
        if line.strip() == "":
            continue
        species, sample, chrom, dp = line.strip().split()
        species_dp[species].append(float(dp))

# 逐物种计算 DP 阈值并调用 parseVCF.py
for species, dplist in species_dp.items():
    min_dp = math.floor(min(dplist) / 2)
    max_dp = math.ceil(max(dplist) * 2)

    input_file = os.path.join(input_dir, f"{species}.vcf.gz")
    output_file = os.path.join(output_dir, f"{species}.geno.txt")

    if not os.path.exists(input_file):
        print(f"[Pass] VCF file not found：{input_file}")
        continue

    cmd = [
        "python", "parseVCF.py",
        "-i", input_file,
        "-o", output_file,
        "--gtf", "flag=DP",
        "min=" + str(min_dp),
        "max=" + str(max_dp)
    ]

    print(f"[Running] {species}: min_DP={min_dp}, max_DP={max_dp}")
    subprocess.run(cmd)
