#!/usr/bin/env python3
import re
import requests
import argparse
import ipaddress
from requests.packages.urllib3.exceptions import InsecureRequestWarning

parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip", type=str)
parser.add_argument("-c", "--cookie", type=str)
parser.add_argument("-u", "--url", type=str)
parser.add_argument("--no-ssl", action='store_false', default=True)
args = parser.parse_args()


def getIP(ip):
    # reference https://support.f5.com/csp/article/K6917
    x = ip.split(".")
    cookieIP = ( int(x[0]) +
                (int(x[1])* 256) +
                (int(x[2])*(256**2)) +
                (int(x[3])*(256**3))
               )
    print(str(cookieIP))


def parseCookie(cookie):
    '''
    BIG-IP system uses the following address encoding algorithm:
        1. Convert each octet value to the equivalent 1-byte hexadecimal value
        2. Reverse the order of the hexadecimal bytes
        3. Concatenate to make one 4-byte hexadecimal value
        4. Convert the resulting 4-byte hexadecimal value to decimal

    '''
    ip, port, empty = cookie.split(".")
    ip = str(ipaddress.IPv4Address(int(ip)))
    splitIP = ip.split(".")
    reverse = splitIP[::-1]
    ip = ".".join(reverse)
    print("IP:\t%s" % ip)

    '''
    BIG-IP system uses the following port encoding algorithm:
        1. Convert the decimal port value to equivalent 2-byte hexadecimal
        2. Reverse the order of the 2 hexadecimal bytes
        2. Convert the resulting 2-byte hexadecimal value to decimal equivalent

    '''
    port = hex(int(port))
    port = "0x" + port[4:6] + port[2:4]
    port = int(port, 16)
    print("PORT:\t%d" % port)


def getCookie(url):
    session = requests.Session()
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                   'AppleWebKit/537.36 (KHTML, like Gecko)'
                                   'Chrome/42.0.2311.135 Safari/537.36'
                                   'Edge/12.246')})
    session.get(url, headers=headers, verify=args.no_ssl)
    cookies = session.cookies.get_dict()
    cookie = ""
    for key, value in cookies.items():
        if re.match("^\d+\.\d+\.\d+$", value):
            print(key)
            cookie = value
    if cookie:
        try:
            parseCookie(cookie)
        except:
            print("[!] Error parsing cookie")
    else:
        print("[!] No BIGip cookie returned")

# 'not' logic  because --no-ssl is 'store_false'
if not args.no_ssl:
    # suppress SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if args.ip:
    getIP(args.ip)

if args.cookie:
    parseCookie(args.cookie)

if args.url:
    getCookie(args.url)
