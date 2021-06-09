# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import socket
from time import sleep
import constants
import io
from PIL import Image
import math

tcp_socket = socket.socket()

def connect():
    print("Connecting to FPGA server at: " + constants.IP + ":" + str(constants.PORT))
    tcp_socket.connect((constants.IP, constants.PORT))
    # establish TCP connection to fpga server
    print("Connection has been established!")

def close():
    tcp_socket.close()

# Source: https://stackoverflow.com/questions/4801366/convert-rgb-values-to-integer/4801397
def convert_pixel_to_rgb_int(pixel):
    if len(pixel) < 3:
        print("rgb pixel should have length 3")
        return None
    
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    
    return ((r&0x0ff)<<16)|((g&0x0ff)<<8)|(b&0x0ff)

# Source: https://stackoverflow.com/questions/4801366/convert-rgb-values-to-integer/4801397
def convert_rgb_int_to_rgb_pixel(rgb_int):
    red = (rgb_int>>16)&0x0ff
    green = (rgb_int>>8) &0x0ff
    blue = (rgb_int)    &0x0ff

    return (red, green, blue)

# divide array to chunks
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

# sends image to fpga server
def send(img):
    # bytes
    byte_arr = io.BytesIO()
    img.save(byte_arr, format=img.format)
    byte_arr = byte_arr.getvalue()

    # pixel
    pix = img.load()  
    width, height = img.size

    pixel_int_values = []
    byt_arr = []
    total_len = 0
    foo = []
    
    for y in range(0, height):
        for x in range(0, width):
            pixel_rgb = pix[x,y]
            foo.append(pix[x,y])
            byt_val = convert_pixel_to_rgb_int(pixel_rgb)
            byt = byt_val.to_bytes(3, 'little')
            total_len = total_len + 3
            for b in byt:
                byt_arr.append(b)
            pixel_int_values.append(byt_val)

    print("TOTAL LEN:")
    print(len(byt_arr))
    # divides image to chunks of size specified below
    chunk_size = 999
    chunks = divide_chunks(byt_arr, chunk_size)
    idx = 0
    pix_arr = []
    total_chunks = len(byt_arr) / chunk_size
    for chunk in chunks:
        chunk_bytes = bytes(chunk)
        nu = idx + 1
        # print chunk number to show progress
        print("#: " + str(nu) + "/" + str(int(math.ceil(total_chunks))))
        
        if constants.IS_SERVER_IN_USE:
            tcp_socket.send(chunk_bytes)
            fpga_server_response = tcp_socket.recv(len(chunk_bytes))
            sleep(0.001)
        
            if not fpga_server_response:
                print("No response from fpga server")
                return
            resp_chunks = divide_chunks(fpga_server_response, 3)

            for r_chunk in resp_chunks:
                byt_int = int.from_bytes(r_chunk, 'little')
                byt_pix = convert_rgb_int_to_rgb_pixel(byt_int)
                pix_arr.append(byt_pix)
        idx = idx + 1

    # checking in terminal that amount of pixels received equals to sent
    print(len(pix_arr))
    print(len(foo))

    # create image from response data
    im = Image.new('RGB', (width, height))
    im.putdata(pix_arr)
    im.save('image.bmp')
    # return image back to ui, it will be shown on right hand side
    return im

