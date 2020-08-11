# PORTBUSTER

### Multithreader Port Scanner with automated ping scan and nmap scan

#### Update 1: nmap integration done


#### Requirements: pingparsing

`pip3 install pingparsing`

**Usage**

```
python3 portBuster.py -t <TARGET_MACHINE_IP> -p <Boolean for ping scans> -T <No. of threads>
```
![](./images/usage.png)
**symbolic link**
cd to portBuster directory
```
ln -s $(pwd)/portBuster.py /usr/local/bin/portBuster
```


