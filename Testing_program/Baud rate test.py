spe_type = [64, 16]
st_list = [8000000, 12000000, 16000000]
br_list = [9600, 19200, 38400, 57600, 115200]

for hi in spe_type:
    print('type:', hi)
    for st in st_list:
        print('system clock:', st)
        for br in br_list:
            N = st//(hi * br) - 1
            nebr = st//(hi * (N+1))
            er = abs(br - nebr) / br * 100
            print('Baud Rate:', br, 'Error value:', er, 'N:', N)
