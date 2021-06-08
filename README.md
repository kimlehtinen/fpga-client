# fpga-client
FPGA Client

Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

## How to run this application

### NOTE! Before start
Don't start this client before you see these lines in FPGA SDK Terminal
```
-----lwIP TCP echo server ------

TCP packets sent to port 6001 will be echoed back

Start PHY autonegotiation 
Waiting for PHY to complete autonegotiation.
autonegotiation complete 
link speed for phy address 1: 1000
DHCP Timeout
Configuring default IP of 192.168.1.10
Board IP: 192.168.1.10

Netmask : 255.255.255.0

Gateway : 192.168.1.1

TCP echo server started @ port 7
```

### Start server
```
python app.py
```

### Useful info

#### Image selection
Use small images only, I recommend you send mars23.jpg or mars24.bmp to fpga server. First image is quite big.

#### UI
UI is split into two columns. On left side you can select image that will be sent. On right side you will see output image from fpga if full image is received.

## In case of error
Try ctrl + c or ctrl + z repeatedly in terminal until it closes :D
