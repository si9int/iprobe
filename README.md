# iprobe
Takes a list of IP addresses and probes it for working `HTTP` and `HTTPS` servers.  
Inspired by: https://github.com/tomnomnom/httprobe
```
usage: iprobe.py [-h] [-c CONCURRENCY]

This tool resolves given IP addresses via STDIN to http(s) hosts

optional arguments:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        number of threads (default: 40)
```
## Install
- Python3 required
```
$ git clone https://github.com/si9int/iprobe.git
```
## Basic Usage
"iprobe" accepts line-delimited addresses on `STDIN`
```
$ cat recon/example/ips.txt

104.244.45.254
104.244.42.132
209.237.199.128
```
**Probe a file**
- Format: `[HTTP status-code] URL`
```
$ cat recon/example/ips.txt | python3 iprobe.py

[404] https://104.244.42.2/
[404] https://104.244.42.5/
[404] https://104.244.42.1/
[404] https://104.244.42.7/
```
**Probe an address**
```
$ echo "104.244.42.2" | python3 iprobe.py 

[404] https://104.244.42.2/
[404] http://104.244.42.2/
```

## Concurrency

You can set the concurrency level with the `-c` flag (default: 40)
```
$ cat recon/example/ips.txt | python3 iprobe.py -c 100
```
