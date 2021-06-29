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


# Source: Stackoverflow 2011, KitsuneYMG https://stackoverflow.com/a/4801433
def convert_pixel_to_rgb_int(pixel):
    if len(pixel) < 3:
        print("rgb pixel should have length 3")
        return None
    
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    
    return ((r&0x0ff)<<16)|((g&0x0ff)<<8)|(b&0x0ff)

# Source: Stackoverflow 2011, KitsuneYMG https://stackoverflow.com/a/4801433
def convert_pixel_to_rgba_int(pixel):
    if len(pixel) < 4:
        print("rgb pixel should have length 3")
        return None
    
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    a = pixel[3]
    
    return ((r&0x0ff)<<24)|((g&0x0ff)<<16)|((b&0x0ff)<<8)|(a&0x0ff)

# Source: Stackoverflow 2011, KitsuneYMG https://stackoverflow.com/a/4801433
def convert_rgb_int_to_rgb_pixel(rgb_int):
    red = (rgb_int>>16)&0x0ff
    green = (rgb_int>>8) &0x0ff
    blue = (rgb_int)    &0x0ff

    return (red, green, blue)

# Source: Stackoverflow 2011, KitsuneYMG https://stackoverflow.com/a/4801433
def convert_rgba_int_to_rgba_pixel(rgb_int):
    red = (rgb_int>>24)&0x0ff
    green = (rgb_int>>16) &0x0ff
    blue = (rgb_int>>8)    &0x0ff
    alpha = (rgb_int)    &0x0ff

    return (red, green, blue, alpha)

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
    img = img.convert('RGBA')
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
            byt_val = convert_pixel_to_rgba_int(pixel_rgb)
            byt = byt_val.to_bytes(4, 'little')
            total_len = total_len + 4
            for b in byt:
                byt_arr.append(b)
            pixel_int_values.append(byt_val)

    print("TOTAL LEN:")
    print(len(byt_arr))
    # divides image to chunks of size specified below
    chunk_size = 400
    chunks = divide_chunks(byt_arr, chunk_size)
    idx = 0
    pix_arr = []
    total_chunks = len(byt_arr) / chunk_size
    chunks_sent = 0
    for chunk in chunks:
        chunks_sent = chunks_sent + len(chunk)
        chunk_bytes = bytes(chunk)
        nu = idx + 1
        # print chunk number to show progress
        print("#: " + str(nu) + "/" + str(int(math.ceil(total_chunks))))
        
        if constants.IS_SERVER_IN_USE:
            tcp_socket.send(chunk_bytes)

            # when last chunks are sent, wait for complete image
            if chunks_sent == total_len:
                print("All chunks sent now")
                rec_len = 0

                # wait for complete image to return
                while rec_len != total_len:
                    print("Waiting for all data to be received")
                    fpga_server_response = tcp_socket.recv(total_len)
                    print("RECLEN:")
                    print(len(fpga_server_response))
                    rec_len = rec_len + len(fpga_server_response)
            else:
                fpga_server_response = tcp_socket.recv(1)
                print("RECLEN PARTIAL:")
                print(len(fpga_server_response))

            sleep(0.001)
        
            if not fpga_server_response:
                print("No response from fpga server")
                return
            resp_chunks = divide_chunks(fpga_server_response, 4)

            for r_chunk in resp_chunks:
                byt_int = int.from_bytes(r_chunk, 'little')
                byt_pix = convert_rgba_int_to_rgba_pixel(byt_int)
                pix_arr.append(byt_pix)
        idx = idx + 1

    # checking in terminal that amount of pixels received equals to sent
    print(len(pix_arr))
    print(len(foo))

    return img

    # create image from response data
    im = Image.new('RGBA', (width, height))
    im.putdata(pix_arr)
    im.save('image.bmp')
    # return image back to ui, it will be shown on right hand side
    return im

