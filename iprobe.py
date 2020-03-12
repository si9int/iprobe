#!/usr/bin/env python3
# v.0.1 - Written by SI9INT (https://twitter.com/si9int) | 2020-03
import requests, queue, threading, sys, argparse

from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from requests.exceptions import TooManyRedirects

requests.packages.urllib3.disable_warnings()
q = queue.Queue(maxsize=0)

header = {
     'Accept'           : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Cache-Control'    : 'no-cache',
     'User-Agent'       : 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
     'Connection'       : 'close',
}

def fetch_target(q):
    while True:        
        ip = q.get()
        variants = ['https://{}/'.format(ip), 'http://{}/'.format(ip)]
        
        for v in variants:
            try:
                res = requests.get(v, headers=header, timeout=3, verify=False)
                if res.status_code:
                    print('[{}] {}'.format(res.status_code, v))
            except ConnectionError:
                pass
            except ConnectTimeout:
                pass
            except TooManyRedirects:
                pass
            except ReadTimeout:
                pass

        q.task_done()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool resolves given IP addresses via STDIN to http(s) hosts')
    parser.add_argument('-c', '--concurrency', type=int, help='number of threads (default: 40)')
    
    args = parser.parse_args()
    
    if args.concurrency:
        num_threads = args.concurrency
    else:
        num_threads = 40
        
    for t in range(num_threads):
        thread = threading.Thread(target=fetch_target, args=(q,))
        thread.setDaemon(True)
        
        thread.start()
    
    for ip in sys.stdin:
        q.put(ip.rstrip())
    
    q.join()
