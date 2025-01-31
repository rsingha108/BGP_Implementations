import random

def compute_all_combinations(ll):
    """
    takes a list of lists of options and returns all possible combinations of these options
    """
    if len(ll) == 1:
        return [[x] for x in ll[0]]
    else:
        return [[x] + y for x in ll[0] for y in compute_all_combinations(ll[1:])]
    
def filter_combinations(combinations):
    """
    filters out some combination if r2 r3 are in same confederation AS
    """
    
    new_combs = []
    for comb in combinations:
        if comb[5] == True and (comb[2] == None or comb[4] == None):
            continue
        elif comb[5] == True and comb[2] != None and comb[4] != None and comb[2] != comb[4]:
            continue
        else:
            new_combs.append(comb)

    return new_combs

def combination_to_numbers(combination):
    """
    takes a combination and returns the actual number of private/non-private ASes in the combination
    """
    private_as_nums = [64512, 65001, 65002, 65003, 65534]
    non_private_as_nums = [100, 200, 300, 64511, 65535]

    isr1pas, isr2pas, isr2cpas, isr3pas, isr3cpas, isr2r3same, r2conf = combination

    r2c_as, r3c_as = None, None

    if isr1pas:
        r1_as = random.choice(private_as_nums)
        private_as_nums.remove(r1_as)
    else:
        r1_as = random.choice(non_private_as_nums)
        non_private_as_nums.remove(r1_as)
    
    if isr2pas:
        r2_as = random.choice(private_as_nums)
        private_as_nums.remove(r2_as)
    else:
        r2_as = random.choice(non_private_as_nums)
        non_private_as_nums.remove(r2_as)
    
    if isr3pas:
        r3_as = random.choice(private_as_nums)
        private_as_nums.remove(r3_as)
    else:
        r3_as = random.choice(non_private_as_nums)
        non_private_as_nums.remove(r3_as)
    
    if isr2cpas == True:
        r2c_as = random.choice(private_as_nums)
        private_as_nums.remove(r2c_as)
    elif isr2cpas == False:
        r2c_as = random.choice(non_private_as_nums)
        non_private_as_nums.remove(r2c_as)
    
    if isr3cpas == True:
        r3c_as = random.choice(private_as_nums)
        private_as_nums.remove(r3c_as)
    elif isr3cpas == False:
        r3c_as = random.choice(non_private_as_nums)
        non_private_as_nums.remove(r3c_as)

    if isr2r3same:
        r3c_as = r2c_as

    return r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf
    

def combination_to_configs(combination):
    """
    takes a combination and updates configs for exabgp, r2, r3
    """

    r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf = combination_to_numbers(combination)
    # print(f"r1_as: {r1_as}, r2_as: {r2_as}, r2c_as: {r2c_as}, r3_as: {r3_as}, r3c_as: {r3c_as}, r2conf: {r2conf}")

    peer_as = r2c_as if (r2c_as != None) else r2_as

    exa_config = f"""
process announce-routes {{  
    run python exabgp/example.py;
    encoder json;
}}

neighbor 3.0.0.2 {{                 # Remote neighbor to peer with
    router-id 3.0.0.3;              # Our local router-id
    local-address 3.0.0.3;          # Our local update-source
    local-as {r1_as};                    # Our local AS
    peer-as {peer_as};                     # Peer's AS

    api {{
        processes [announce-routes];
    }}
}}
"""

    r2_confed = ""
    if r2c_as != None:
        r2_confed += f"bgp confederation identifier {r2c_as}\n"
    if (r2c_as != None) and (r2c_as == r3c_as):
        r2_confed += f"bgp confederation peers {r3_as}\n"

    nbr1_as = r1_as
    nbr3_as = r3_as
    if (r3c_as != None) and (r3c_as != r2c_as):
        nbr3_as = r3c_as

    r2_config = f"""
router bgp {r2_as}
no bgp ebgp-requires-policy
{r2_confed}
neighbor 3.0.0.3 remote-as {nbr1_as}
neighbor 4.0.0.3 remote-as {nbr3_as}
neighbor 4.0.0.3 {r2conf}
exit
!
"""

    r3_confed = ""
    if r3c_as != None:
        r3_confed += f"bgp confederation identifier {r3c_as}\n"
    if (r3c_as != None) and (r2c_as == r3c_as):
        r3_confed += f"bgp confederation peers {r2_as}\n"

    nbr2_as = r2_as
    if (r2c_as != None) and (r3c_as != r2c_as):
        nbr2_as = r2c_as

    r3_config = f"""
router bgp {r3_as}
no bgp ebgp-requires-policy
{r3_confed}
neighbor 4.0.0.2 remote-as {nbr2_as}
exit
!
"""

    with open("exabgp1/conf.ini", "w") as f:
        f.write(exa_config)
    
    with open("frr2/frr.conf", "w") as f:
        f.write(r2_config)

    with open("frr3/frr.conf", "w") as f:
        f.write(r3_config)

    return r1_as, r2_as, r2c_as, r3_as, r3c_as, r2conf

    
def parse_rib():
    isR2received = False
    isR3received = False
    r2_aspath = None
    r3_aspath = None

    with open("router2_RIB.txt", "r") as f:
        lines = f.readlines()
    # print(lines)
    if lines[0].strip() == "% Network not in table":
        isR2received = False
    else:
        isR2received = True
        r2_aspath = lines[4].strip()

    with open("router3_RIB.txt", "r") as f:
        lines = f.readlines()
    # print(lines)
    if lines[0].strip() == "% Network not in table":
        isR3received = False
    else:
        isR3received = True
        r3_aspath = lines[4].strip()

    return isR2received, isR3received, r2_aspath, r3_aspath

