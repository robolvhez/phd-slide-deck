import csv
import os

tsv_path = "/home/rolvhdez/data/effect-size-differences/significant_FDR_joined.tsv"
anc_dir = "/home/rolvhdez/data/effect-size-differences/ancestries"

with open(tsv_path, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        snp = row["SNP"]
        parts = snp.split(":")
        chrom = parts[0].replace("chr", "")
        pos, ref, alt = parts[1:]
        filename = f"allele-freq-by-population-{chrom}_{pos}_{ref}_{alt}.csv"
        filepath = os.path.join(anc_dir, filename)
        
        imx = ""
        eur = ""
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8-sig") as af:
                areader = csv.DictReader(af)
                for arow in areader:
                    if arow["Ancestry"] == "Indigenous Mexican (IMX)":
                        imx = arow.get("MCPS", "")
                    elif arow["Ancestry"] == "European (EUR)":
                        eur = arow.get("MCPS", "")
        pheno = row["Phenotype"]
        gene = row["GENE"]
        diff_beta = row["Diff_Beta"]
        fdr = row["FDR"]
        print(f"{pheno} | {snp} | {gene} | {diff_beta} | {fdr} | {imx} | {eur}")
