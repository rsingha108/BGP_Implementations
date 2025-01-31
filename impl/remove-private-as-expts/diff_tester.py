import json

def is_private_as(asn):
    if (int(asn) >= 64512) and (int(asn) <= 65535):
        return True
    return False

def remove_private_as(aspath, tag=None):
    aspath = aspath.split(" ")
    ## Adding code to accept anomaly in case of same confed (do not remove private AS)
    if tag == "same-confed":
        return " ".join(aspath)
    isPublicAS = False
    for asn in aspath:
        if not is_private_as(asn):
            isPublicAS = True
            break
    if isPublicAS:
        return " ".join(aspath)
    
    new_aspath = []
    for asn in aspath:
        if is_private_as(asn):
            continue
        new_aspath.append(asn)
    return " ".join(new_aspath)

def remove_private_as_all(aspath, tag=None):
    aspath = aspath.split(" ")
    ## Adding code to accept anomaly in case of same confed (do not remove private AS)
    if tag == "same-confed":
        return " ".join(aspath)
    new_aspath = []
    for asn in aspath:
        if is_private_as(asn):
            continue
        new_aspath.append(asn)
    return " ".join(new_aspath)

def remove_private_as_all_replace_as(aspath, my_asn, tag=None):
    aspath = aspath.split(" ")
    ## Adding code to accept anomaly in case of same confed (do not remove private AS)
    if tag == "same-confed":
        return " ".join(aspath)
    new_aspath = []
    for asn in aspath:
        if is_private_as(asn):
            new_aspath.append(str(my_asn))
        else:
            new_aspath.append(asn)
    return " ".join(new_aspath)

def get_category(comb_nums):
    r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf = comb_nums
    r1_as = int(r1_as); r2_as = int(r2_as); r2c_as = eval(r2c_as); r3_as = int(r3_as); r3c_as = eval(r3c_as); r2conf = r2conf

    if (r2c_as == None) and (r3c_as == None):
        return "No confed"
    elif (r2c_as != None) and (r3c_as == None):
        return "Only R2 confed"
    elif (r2c_as != None) and (r3c_as != None) and (r2c_as != r3c_as):
        return "R2 and R3 in diff confed"
    elif (r2c_as != None) and (r3c_as != None) and (r2c_as == r3c_as):
        return "R2 and R3 in same confed"
    elif (r2c_as == None) and (r3c_as != None):
        return "R3 confed"
    else:
        return "Unknown"


def expected_output(comb_nums):
    r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf = comb_nums
    r1_as = int(r1_as); r2_as = int(r2_as); r2c_as = eval(r2c_as); r3_as = int(r3_as); r3c_as = eval(r3c_as); r2conf = r2conf

    isR2received, isR3received, r2_aspath, r3_aspath  = False, False, None, None

    ## Case 1: No confed
    if (r2c_as == None) and (r3c_as == None):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath)
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath)
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as)
        r3_aspath = f"{r2_as} {r3_aspath}".strip()
    
    ## Case 2: only R2 confed
    if (r2c_as != None) and (r3c_as == None):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath)
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath)
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as)
        r3_aspath = f"{r2c_as} {r3_aspath}".strip()
    
    ## Case 3: R2 and R3 in diff confed
    if (r2c_as != None) and (r3c_as != None) and (r2c_as != r3c_as):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath)
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath)
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as)
        r3_aspath = f"{r2c_as} {r3_aspath}".strip()

    ## Case 4: R2 and R3 in same confed
    if (r2c_as != None) and (r3c_as != None) and (r2c_as == r3c_as):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath, tag="same-confed")
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath, tag="same-confed")
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as, tag="same-confed")
        r3_aspath = f"({r2_as}) {r3_aspath}".strip()

    ## Case 5: only R3 in confed
    if (r2c_as == None) and (r3c_as != None):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath)
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath)
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as)
        r3_aspath = f"{r2_as} {r3_aspath}".strip()

    return isR2received, isR3received, r2_aspath, r3_aspath


if __name__ == "__main__":
    with open("tests.txt", "r") as f:
        testlines = f.readlines()

    with open("frr_results.txt", "r") as f:
        reslines = f.readlines()

    anomalies = []
    failed = 0
    for i in range(len(testlines)):
        comb_nums = testlines[i].strip().split(",")
        category = get_category(comb_nums)
        isR2received, isR3received, r2_aspath, r3_aspath = expected_output(comb_nums)
        res = reslines[i].strip().split(",")
        if (isR2received == bool(res[0])) and (isR3received == bool(res[1])):
            if (r2_aspath == res[2]) and (r3_aspath == res[3]):
                print(f"Test {i+1} passed")
            else:
                print(f"Test {i+1} failed")
                d = {"Test Case": testlines[i].strip(), "Category": category, "Expected": (isR2received, isR3received, r2_aspath, r3_aspath), "Actual": (bool(res[0]), bool(res[1]), res[2], res[3])}
                anomalies.append(d)
                failed += 1
        else:
            print(f"Test {i+1} failed")
            d = {"Test Case": testlines[i].strip(), "Category": category, "Expected": (isR2received, isR3received, r2_aspath, r3_aspath), "Actual": (bool(res[0]), bool(res[1]), res[2], res[3])}
            anomalies.append(d)
            failed += 1

    print(f"Total failed tests: {failed}")

    ## sort anomalies by category
    anomalies = sorted(anomalies, key=lambda x: x["Category"])

    with open("diff_test_results.json", "w") as f:
        json.dump(anomalies, f, indent=4)
        

    

        
    
