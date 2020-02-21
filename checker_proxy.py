from sys import exit,argv
from requests import get
from multiprocessing import Pool
from os import mkdir
from os.path import exists
from time import ctime

def fread(filename):
    try:
        f = open(filename, 'r')
        a=f.read()
        f.close()
        a=a.split("\n")
        if a[-1]=="":
            del a[-1]
        a=list(set(a))
        return a
    except:
        print("error in reading file")
        log_out(0)

def fwrite(filename,a):
    try:
        f = open(filename, 'w')
        for x in range(len(a)):
            f.write(a[x]+"\n")
        f.close()
    except:
        print("error in writing file")
        log_out(0)

def fwrite_result(t):
    try:
        if exists("result")!=True:
            mkdir("result")
        if exists("result\\"+t)!=True:
            mkdir("result\\"+t)
    except:
        print("error in creating dirs")
        log_out(0)

def socks4_checker(proxysite):
    try:
        proxy=proxysite[0]
        site="https://"+proxysite[1]
        result = get(site, proxies={'http': 'socks4://'+proxy,'https': 'socks4://'+proxy},timeout=20)
        if result.status_code==200:
            print("good:"+proxy)
            return proxy
    except:
        print("bad:"+proxy)
        return "null"

def socks5_checker(proxysite):
    try:
        proxy=proxysite[0]
        site="https://"+proxysite[1]
        result = get(site, proxies={'http': 'socks5://'+proxy,'https': 'socks5://'+proxy},timeout=20)
        if result.status_code==200:
            print("good:"+proxy)
            return proxy
    except:
        print("bad:"+proxy)
        return "null"

def http(proxysite):
    try:
        proxy=proxysite[0]
        site="https://"+proxysite[1]
        result = get(site, proxies={'http': proxy,'https': proxy},timeout=20)
        if result.status_code==200:
            print("good:"+proxy)
            return proxy
    except:
        print("bad:"+proxy)
        return "null"

def log_out(a):
    if a==0:
        print("for help use -h")
    elif a==1:
        print("---------------------------------------------------------------------------------------------------")
        print("1) write path to proxy example: -proxy=C:\\proxy.txt")
        print("2) select type proxy: -type_proxy=http or -type_proxy=socks4 or -type_proxy=socks5 ")
        print("3) write number of processes: -procs=100")
        print("4) write site: -site=google.com")
        print("5) example: checker_proxy -proxy=C:\\proxy.txt -type_proxy=socks4 -procs=100 -site=google.com")
        print("Created by Gick)")
        print("---------------------------------------------------------------------------------------------------")
    elif a==2:
        print("no good proxy")
    else:
        print("don't work yet")
    exit(0)

def check_proxy(n):
    proxy_list=fread(n[2])
    for x in range(len(proxy_list)):
        proxy_list[x]=[proxy_list[x],n[3]]
    try:
        pool=Pool(int(n[0]))
    except:
        print("error in initialization of procs")
        log_out(0)
    if n[1]=="http":
        print("Start checking proxy")
        proxy_list=pool.map(http_checker, proxy_list)
    elif n[1]=="socks4":
        print("Start checking proxy")
        proxy_list=pool.map(socks4_checker, proxy_list)
    elif n[1]=="socks5":
        print("Start checking proxy")
        proxy_list=pool.map(socks5_checker, proxy_list)
    else:
        print("error in checking proxy")
        log_out(0)
    good_proxy=[]
    for x in range(len(proxy_list)):
        if proxy_list[x]!="null":
            good_proxy.append(proxy_list[x])
    print("Proxy checker result: all-"+str(len(proxy_list))+" good-"+str(len(good_proxy))+" bad-"+str(len(proxy_list)-len(good_proxy)))
    
    del proxy_list
    
    if good_proxy==[]:
        log_out(2)
    else:
        print("Saving good proxy")
        t_result=str(ctime()).replace(":","_")
        fwrite_result(t_result)
        fwrite("result\\"+t_result+"\\"+"good_"+n[1]+".txt",good_proxy)

def main():
    try:
        if argv[1]=="-h" or argv[1]=="-help":
            log_out(1)

        else:
            n=["0","0","0","0"]
            for x in range(len(argv)):
                if argv[x].split('=')[0]=="-procs":
                    n[0]=argv[x].replace("-procs=","")
                elif argv[x].split('=')[0]=="-type_proxy":
                    n[1]=argv[x].replace("-type_proxy=","")
                elif argv[x].split('=')[0]=="-proxy":
                    n[2]=argv[x].replace("-proxy=","")
                elif argv[x].split('=')[0]=="-site":
                    n[3]=argv[x].replace("-site=","")
            check_proxy(n)
    except:
        log_out(0)
    




if __name__ == '__main__': 
    main()
