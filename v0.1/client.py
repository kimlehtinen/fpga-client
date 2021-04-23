# importing the module tkinter
import tkinter as tk
import socket
from time import sleep

IP = '192.168.1.10'
PORT = 7

desktop = tk.Tk(className='FPGA project work - TCP client') 

def connect():
    print("Connecting to FPGA server at: " + IP + ":" + str(PORT))
    # establish TCP connection to fpga server
    tcp_socket = socket.socket()
    tcp_socket.connect((IP, PORT))
    print("Connection has been established!")

    while True:
        try:
            # tcp payload data sent to fpga server
            data = bytes('Hello python!', encoding='utf8')
            
            # send data to fpga server
            tcp_socket.send(data)

            sleep(1)
            
            # recieve data from fpga server
            # max data amount is 100 (bufsize)
            fpga_server_response = tcp_socket.recv(100)

            # stop if no response from fpga server
            if not fpga_server_response:
                break

            print("SERVER SENT: " + fpga_server_response.decode('utf8') )
        
        except KeyboardInterrupt:
            print("KeyboardInterrupt: closing program")
            break

    tcp_socket.close()

# add button to GUI that connects to fpga server
connect_button = tk.Button(desktop, text ="Connect", command = connect)
connect_button.pack()

# start desktop application
desktop.mainloop()
