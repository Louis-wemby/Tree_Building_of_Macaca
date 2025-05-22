#!/bin/bash

# 输入文件名
input_file="./.geno.txt"
# 使用 awk 统计每个样本非N的数量
awk '
BEGIN { FS="\t" }
NR==1 {
    for(i=3;i<=NF;i++) sample[i]=$i
    next
}
{
    for(i=3;i<=NF;i++) {
        if(toupper($i) != "N") count[i]++
    }
}
END {
    for(i=3;i<=length(sample);i++) {
        print sample[i] "\t" count[i]+0
    }
}
' "$input_file" > valid_snp_counts.txt

echo "Result saved to valid_snp_counts.txt"
