import os
import argparse
import glob
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="批量运行 IQ-TREE2，支持指定模型、引导次数、前缀和输出目录结构")
    parser.add_argument("-i", "--input_dir", required=True, help="包含多个 .phy 文件的目录")
    parser.add_argument("-o", "--output_dir", required=True, help="用于保存每个输入文件的IQ-TREE输出目录")
    parser.add_argument("-m", "--model", required=True, help="模型，如 GTR, HKY 等")
    parser.add_argument("-b", "--bootstrap", default="1000", help="引导次数，默认1000")
    parser.add_argument("-p", "--prefix", default=None, help="每个分析的前缀，默认使用输入文件名")
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    model = args.model
    bootstrap = args.bootstrap
    use_prefix = args.prefix

    os.makedirs(output_dir, exist_ok=True)

    phylip_files = glob.glob(os.path.join(input_dir, "*.phy"))
    if not phylip_files:
        print("No .phy files found")
        return

    for phylip_file in phylip_files:
        base_name = os.path.basename(phylip_file).replace(".phy", "")
        run_prefix = use_prefix + "_" + base_name if use_prefix else base_name

        # 每个文件对应的子目录
        out_dir = os.path.join(output_dir, run_prefix)
        os.makedirs(out_dir, exist_ok=True)

        # 构造 IQ-TREE 命令
        cmd = [
            "iqtree2",
            "-s", phylip_file,
            "-m", model,
            "-b", bootstrap,
            "-pre", os.path.join(out_dir, run_prefix)
        ]

        print(f"[Running] {' '.join(cmd)}")
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
