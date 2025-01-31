from utils import *
import os

r1pas = [True, False]
r2pas = [True, False]
r2cpas = [True, False, None]
r3pas = [True, False]
r3cpas = [True, False, None]
r2r3c = [True, False]
r2conf = ["remove-private-AS", "remove-private-AS all", "remove-private-AS all replace-AS"]

combinations = compute_all_combinations([r1pas, r2pas, r2cpas, r3pas, r3cpas, r2r3c, r2conf])

filtered_combinations = filter_combinations(combinations)

f = open("tests.txt", "w")
f.close()
f = open("frr_results.txt", "w")
f.close()

for comb in filtered_combinations:
    r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf = combination_to_configs(comb)
    with open("tests.txt", "a") as f:
        f.write(f"{r1_as},{r2_as},{r2c_as},{r3_as},{r3c_as},{r2conf}\n")
    ## Add code for testing the configurations here
    os.system("bash run.sh")
    ## Add code to parse output 
    isR2received, isR3received, r2_aspath, r3_aspath = parse_rib()
    with open("frr_results.txt", "a") as f:
        f.write(f"{isR2received},{isR3received},{r2_aspath},{r3_aspath}\n")
    ## expected output code
    ## all test results
    ## unexpected results




