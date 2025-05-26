def update_batfish_config(rmap):
    g = open('../networks/route-analysis/configs/border4.cfg','w')
    g.write('!\n')
    g.write('hostname border4\n')

    if rmap["prefix-list"] != []:
        for prefix in rmap["prefix-list"]:
            g.write(f'ip prefix-list PFXL {prefix["action"]} {prefix["match"]}\n')

    if rmap["community-list"] != []:
        for comm in rmap["community-list"]:
            crgx = comm["match"].replace(" ","_")
            g.write(f'ip community-list 100 {comm["action"]} {crgx}\n')
        
    if rmap["as-path-list"] != []:
        for asp in rmap["as-path-list"]:
            g.write(f'ip as-path access-list 99 {asp["action"]} {asp["match"]}\n')


    ## all match statements first (AND of them) then set statements 
    g.write(f'route-map Rmap {rmap["rmap-action"]} 10\n')
    if rmap["prefix-list"] != []:
        g.write(f'	match ip address prefix-list PFXL\n')
    if rmap["community-list"] != []:
        g.write(f'	match community 100\n')
    if rmap["as-path-list"] != []:
        g.write(f'	match as-path 99\n')
    g.write('end\n')
    g.close()
