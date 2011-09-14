
import xmlrpclib
import json
import sys
import os
import re

cmd_str  = "(\S+)\s+(\S+).*(%s)\s+(.*)"

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
