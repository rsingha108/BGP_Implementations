import json

def remove_private_as(aspath):
    aspath = aspath.split(" ")
    isPublicAS = False
    for asn in aspath:
        if (int(asn) < 64512) or (int(asn) == 65535):
            isPublicAS = True
            break
    if isPublicAS:
        return " ".join(aspath)
    
    new_aspath = []
    for asn in aspath:
        if int(asn) >= 64512 and int(asn) < 65535:
            continue
        new_aspath.append(asn)
    return " ".join(new_aspath)

def remove_private_as_all(aspath):
    aspath = aspath.split(" ")
    new_aspath = []
    for asn in aspath:
        if int(asn) >= 64512 and int(asn) < 65535:
            continue
        new_aspath.append(asn)
    return " ".join(new_aspath)

def remove_private_as_all_replace_as(aspath, my_asn):
    aspath = aspath.split(" ")
    new_aspath = []
    for asn in aspath:
        if int(asn) >= 64512 and int(asn) < 65535:
            new_aspath.append(my_asn)
        new_aspath.append(asn)
    return " ".join(new_aspath)

def expected_output(comb_nums):
    r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf = comb_nums

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
        r3_aspath = f"{r2_as} {r3_aspath}"
    
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
        r3_aspath = f"{r2c_as} {r3_aspath}"
    
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
        r3_aspath = f"{r2c_as} {r3_aspath}"

    ## Case 4: R2 and R3 in same confed
    if (r2c_as != None) and (r3c_as != None) and (r2c_as == r3c_as):
        isR2received, isR3received = True, True
        r2_aspath = f"{r1_as}"
        r3_aspath = f"{r1_as}"
        if r2conf == "remove-private-AS":
            r3_aspath = remove_private_as(r3_aspath)
        elif r2conf == "remove-private-AS all":
            r3_aspath = remove_private_as_all(r3_aspath)
        elif r2conf == "remove-private-AS all replace-AS":
            r3_aspath = remove_private_as_all_replace_as(r3_aspath, r2_as)
        r3_aspath = f"({r2_as}) {r3_aspath}"

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
        r3_aspath = f"({r2_as}) {r3_aspath}"

    return isR2received, isR3received, r2_aspath, r3_aspath


if __name__ == "__main__":
    with open("tests.txt", "r") as f:
        testlines = f.readlines()

    with open("frr_results.txt", "r") as f:
        reslines = f.readlines()

    anomalies = []
    for i in range(len(testlines)):
        comb_nums = testlines[i].strip().split(",")
        isR2received, isR3received, r2_aspath, r3_aspath = expected_output(comb_nums)
        res = reslines[i].strip().split(",")
        if (isR2received == bool(res[0])) and (isR3received == bool(res[1])):
            if (r2_aspath == res[2]) and (r3_aspath == res[3]):
                print(f"Test {i+1} passed")
            else:
                print(f"Test {i+1} failed")
                d = {"Test Case": testlines[i].strip(), "Expected": (isR2received, isR3received, r2_aspath, r3_aspath), "Actual": (bool(res[0]), bool(res[1]), res[2], res[3])}
                anomalies.append(d)
        else:
            print(f"Test {i+1} failed")
            d = {"Test Case": testlines[i].strip(), "Expected": (isR2received, isR3received, r2_aspath, r3_aspath), "Actual": (bool(res[0]), bool(res[1]), res[2], res[3])}
            anomalies.append(d)

    with open("diff_test_results.json", "w") as f:
        json.dump(anomalies, f, indent=4)
        

    

        
    
