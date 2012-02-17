#!/usr/bin/env python

import json
import sys
import os

BUFFSIZE = 4096

def fullPath(file_name):
    return os.path.abspath(os.path.expanduser(file_name))

def printf(format,*args): sys.stdout.write(format%args)

def fprintf(fp,format,*args): fp.write(format%args)

def usage(prog):
    printf("usage is %s <oldRecords.json> <newRecords.json>\n",prog)
    printf("\n")
    printf("Migrates the records.json file to the new format\n")

def openfiles(fi_name,fo_name,buffsize=BUFFSIZE):
    if fi_name == "-":
        fi = sys.stdin
    else:
        fi = open(fullPath(fi_name),"r",buffsize)

    if fo_name == "-":
        fo = sys.stdout
    else:
        fo = open(fullPath(fo_name),"w",buffsize)
    return (fi,fo)
        

def convert(fi,fo):
    obj = json.loads(fi.read())
    #Convert A records
    a = obj["A"]
    obj["A"]=[]
    for(h,(ip,ttl)) in a.iteritems():
        obj["A"].append((h,ip,ttl))
    obj["A"].sort()
    #Convert AAAA records
    aaaa = obj["AAAA"]
    obj["AAAA"]=[]
    for(h,(ip,ttl)) in aaaa.iteritems():
        obj["AAAA"].append((h,ip,ttl))
    obj["AAAA"].sort()
    #Save the results
    jsonStr = json.dumps(obj,indent=4)
    fo.write(jsonStr)
    fo.flush()    

if __name__=="__main__":
    prog = os.path.basename(sys.argv[0])
    if len(sys.argv)<3:
        usage(prog)
        sys.exit()
    fi_name = sys.argv[1]
    fo_name = sys.argv[2]        
    (fi,fo) = openfiles(fi_name,fo_name)
    convert(fi,fo)
