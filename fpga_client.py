# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import socket
from time import sleep
import constants
import io
from PIL import Image

tcp_socket = socket.socket()

def connect():
    print("Connecting to FPGA server at: " + constants.IP + ":" + str(constants.PORT))
    tcp_socket.connect((constants.IP, constants.PORT))
    # establish TCP connection to fpga server
    print("Connection has been established!")

def close():
    tcp_socket.close()

# example of sending whole image
def send(img):
    byte_arr = io.BytesIO()
    img.save(byte_arr, format=img.format)
    byte_arr = byte_arr.getvalue()

    print("Amount of bytes to be sent:")
    print(len(byte_arr))
    total_len = len(byte_arr)
    print("First byte to be sent:")
    print(byte_arr[0])
    print("Last byte to be sent:")
    print(byte_arr[total_len-1])
    
    # send image to fpga server
    tcp_socket.send(byte_arr) 

    data_rec_len = 0
    all_bytes = []

    # wait until complete image received
    while data_rec_len != total_len:
        fpga_server_response = tcp_socket.recv(total_len)
        sleep(1)

        if not fpga_server_response:
            print("No response from fpga server")
            return img
        r_len = len(fpga_server_response)
        print(r_len)
        data_rec_len = data_rec_len + r_len

        for img_byt in fpga_server_response:
            all_bytes.append(img_byt)

    print("First byte received:")
    print(all_bytes[0])
    print("Last byte received:")
    print(all_bytes[total_len-1])

    print("Amount of bytes received:")
    print(len(all_bytes))

    img_bytes_from_fpga = bytes(all_bytes)
    byt_img = io.BytesIO(img_bytes_from_fpga)
    img_result = Image.open(byt_img)
    return img_result

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]
