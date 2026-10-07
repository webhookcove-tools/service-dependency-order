"""Produce a dependency-first order or identify unresolved cycles."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

import base64,ipaddress,uuid
from urllib.parse import parse_qsl,urlsplit
from http.cookies import SimpleCookie

def analyze(data):
    remaining={name:set(deps) for name,deps in data['dependencies'].items()}
    for dep in set().union(*remaining.values()) if remaining else set():remaining.setdefault(dep,set())
    order=[]
    while remaining:
        ready=sorted(name for name,deps in remaining.items() if not deps)
        if not ready:break
        order.extend(ready)
        for name in ready:remaining.pop(name)
        for deps in remaining.values():deps.difference_update(ready)
    return {'order':order,'unresolved':sorted(remaining)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
