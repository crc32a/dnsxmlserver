
import xmlrpclib
import json
import sys
import os
import re

cmd_str  = "(\S+)\s+(\S+).*(%s)\s+(.*)"
CONF_FILE = "~/dnsxmlclient.json"


def chop(line):
    return line.replace("\r","").replace("\n","")

def choplines(lines):
    lines_out = []
    for line in lines:
        lines_out.append(chop(line))
    return lines_out

def load_json(json_file):
    full_path = os.path.expanduser(json_file)
    full_path = os.path.abspath(full_path)
    fp = open(full_path,"r")
    json_data = fp.read()
    fp.close()
    out = json.loads(json_data)
    return out


def save_json(json_file,obj):
    full_path = os.path.expanduser(json_file)
    full_path = os.path.abspath(full_path)
    fp = open(full_path,"w")
    out = json.dumps(obj, indent=2)
    fp.write(out)
    fp.close()

def psAll():
    lines = os.popen("ps -ef -ww","r").readlines()
    return lines


def match_cmd(lines,cmd):
    out = {}
    cmd_r = re.escape(cmd)
    cmd_re = re.compile(cmd_str%cmd_r)
    for line in lines:
        m = cmd_re.match(chop(line))
        if m:
            pid = int(m.group(2))
            cmd_name = m.group(3)
            params = m.group(4)
            out[pid] = (m.group(3),m.group(4))
    return out

def getCurrentDomain(*args):
    conf = load_json(CONF_FILE)
    if len(args)==0:
        domain = conf["curr_domain"]
    else:
        domain = args[0]
    url = conf["domains"][domain]["url"]
    baseDomain = conf["domains"][domain]["baseDomain"]
    cred = conf["domains"][domain]["cred"]
    return (url,domain,baseDomain,cred)

def pad(digits,ch,val,*args,**kw):
  str_out=str(val)
  side = kw.pop("side","LEFT")
  if side == "LEFT":
    for i in xrange(0,digits-len(str_out)):
      str_out = ch + str_out
    return str_out
  if side == "RIGHT":
    for i in xrange(0,digits-len(str_out)):
      str_out = str_out + ch
    return str_out

