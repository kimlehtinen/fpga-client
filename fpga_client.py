# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import socket
from time import sleep
import desktop
import constants

tcp_socket = socket.socket()

def connect():
    print("Connecting to FPGA server at: " + constants.IP + ":" + str(constants.PORT))
    tcp_socket.connect((constants.IP, constants.PORT))
    # establish TCP connection to fpga server
    print("Connection has been established!")

def close():
    tcp_socket.close()

def send():
    # tcp payload data sent to fpga server
    data = bytes('Hello from python!', encoding='utf8')
            
    # send data to fpga server
    tcp_socket.send(data)

    sleep(1)
            
    # recieve data from fpga server
    # max data amount is 100 (bufsize)
    fpga_server_response = tcp_socket.recv(100)

    # stop if no response from fpga server
    if not fpga_server_response:
        print("No response from fpga server")

    print("SERVER SENT: " + fpga_server_response.decode('utf8') )

    # remove extra spaces from response
    fpga_server_response = fpga_server_response.rstrip()

    # show response in desktop app
    desktop.server_response_msg.set(fpga_server_response)