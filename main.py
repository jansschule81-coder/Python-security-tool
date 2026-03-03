from icmplib import ping
import nmap
import requests
import whois
import subprocess
import time
import datetime
from collections import Counter
import socketio
import json
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scapy.all import sniff, Raw
from scapy.layers.http import HTTPRequest
def port():
 lebron = input("enter website: ")
 host = ping(lebron, count=4, interval=1, timeout=2, privileged=False)
 target = host.address
 range = "22-443"
 scanner = nmap.PortScanner()
 scanner.scan(target, range, arguments='-sS')
 print("ip:", host.address)
 for host in scanner.all_hosts():
   for proto in scanner[host].all_protocols():
    print(f'Protocol: {proto}')
    ports = scanner[host][proto].keys()
    for port in ports:
     print(f'Port: {port}\tState: {scanner[host][proto][port]["state"]}')

def fuzzer():
 print("fuzzer")
 b = input("website: ").strip()
 with open('wordlists/common.txt', 'r', encoding='utf-8', errors='ignore') as file:
   for a in file:
     a = a.strip() 
     website = f'{b}{a}/'
     response = requests.get(website)
     if response.status_code == 200:
       print(website)
       
def get_whois():
  domain = input("domain: ")
  w = whois.whois(domain)
  print(f"Domain: {domain}")
  print(f"Registrar: {w.registrar}")
  print(f"Creation Date: {w.creation_date}")
  print(f"Expiration Date: {w.expiration_date}")
  print(f"Name Servers: {w.name_servers}")
  print(f"Status: {w.status}")
  print(f"Emails: {w.emails}")

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'

THRESHOLD = 5      
INTERVAL = 2      
PORT = 8000        
LOG_FILE = 'ddos_log.txt'

def get_connections():
    try:
        cmd = (
            f'Get-NetTCPConnection -State Established '
            f'| Where-Object {{ $_.RemotePort -eq {PORT} }} '
            f'| Select-Object -ExpandProperty RemoteAddress'
        )
        output = subprocess.check_output(
            ['powershell', '-Command', cmd],
            text=True,
            stderr=subprocess.STDOUT
        )
        ips = [line.strip() for line in output.splitlines() if line.strip()]
        return Counter(ips)
    except Exception as e:
        print(f"{YELLOW}Error fetching connections: {e}{RESET}")
        return Counter()

def print_bar(value, max_val=200, width=40):
    if max_val <= 0:
        max_val = 1
    ratio = min(value / max_val, 1.0)
    filled = int(width * ratio)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}] {value}/{max_val}'
def dos():
 print(f"{BLUE}DDOS monitor started")
 print(f"Watching port {PORT}, threshold {THRESHOLD}")
 print(f"Logs: {LOG_FILE}{RESET}")

 try:
    while True:
        conn_count = get_connections()
        total_conns = sum(conn_count.values())
        print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')} total connections: {total_conns}")
        print("DEBUG connections:", dict(conn_count))

        suspicious = {
            ip: count
            for ip, count in conn_count.most_common(10)
            if count >= THRESHOLD
        }

        if suspicious:
            print(f"{RED} Dos/DDOS detected{RESET}")
            for ip, count in suspicious.items():
                bar = print_bar(count)
                print(f"{RED}  {ip}: {bar}{RESET}")

            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.datetime.now()}: alert {suspicious}\n")

            print('\a')  
        else:
            if conn_count:
                top_ip, top_count = conn_count.most_common(1)[0]
                print(f"{GREEN}ok: {top_ip}: {print_bar(top_count)}{RESET}")
            else:
                print(f"{GREEN}ok: no connections on this port {PORT}{RESET}")

        time.sleep(INTERVAL)

 except KeyboardInterrupt:
    print(f"\n{BLUE}stopped: logs saved to: {LOG_FILE}.{RESET}")

def http_https():
    url = input("Input URL like this: http://192.168.2.183:3000/):")
    url2 = input("Input URL like this: http://192.168.2.183:3000/api/messages): ").strip()
    if not url.startswith(('http://', 'https://')):
        print("Error: http:// or https://")
        return
    try:
        multiplier = int(input("spam multi (1 for 10,000 As total): "))
    except ValueError:
        print("Error: Enter a valid number")
        return
    msg = "B" * 10000
    message = {"message": msg}
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Origin': url,
    'Referer': url
    }
    for _ in range(multiplier):
     r = requests.post(url2, json=message, headers=headers)
     print("status code:", r.status_code)
def sniffer():
   def sniffing(packet):
      if packet.haslayer(HTTPRequest):
         host = packet[HTTPRequest].Host.decode()
         path = packet[HTTPRequest].Path.decode()
         method = packet[HTTPRequest].Method.decode()
         print(f"http: {method} {host}{path}")
   mangos = input("input port:")
   sniff(filter=f"port {mangos}", prn=sniffing, store=False)
         
def main():
 print("Jans Tool")
 print("port scanner = 1")
 print("fuzzer = 2")
 print("domain lookup = 3")
 print("dos scanner = 4")
 print("chat spammer: 5")
 print("packet sniffer: 6")
 a = int(input("Tool:"))
 if a == 1:
   port()
 if a == 2:
  fuzzer()
 if a == 3:
  get_whois()
 if a == 4:
    dos()
 if a == 5:
    http_https()
 if a == 6:
    sniffer()
while 1 == 1:
  main()