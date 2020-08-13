# PORTBUSTER

### Multithreader Port Scanner with automated ping scan and nmap scan

#### Update 1: Nmap integration done
#### Update 2: Docker integration (WIP)

#### Requirements: pingparsing, pyfiglet

`pip3 install -r requirements.txt`

#### Docker
*In the portBuster directory*

`docker build --tag port-buster .`

<<<<<<< HEAD
```
python3 portBuster.py -t <TARGET_MACHINE_IP> -p <Boolean for ping scans> -T <No. of threads>
```
![](./images/usage.png)
**symbolic link**
cd to portBuster directory
```
ln -s $(pwd)/portBuster.py /usr/local/bin/portBuster
```


=======
`docker run -it port-buster`

![](./images/sample.png)
>>>>>>> b0851dc6179b11fcc203d04ccd4ee1773e542854
