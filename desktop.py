# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import tkinter as tk
import fpga_client
import constants

# create desktop app
window = tk.Tk()

# other files can use these variables to access desktop elements
server_ip_text = tk.StringVar()
server_port_text = tk.StringVar()
server_response_msg = tk.StringVar()

def on_close():
    fpga_client.close()
    window.destroy()

def configure_window():
    window.title('Kim Lehtinen - Zybo Z7-20 FPGA TCP client')
    # set main window size
    window.geometry("1000x500")

def show_ip_address():
    # show fpga server ip
    server_ip_text_label = tk.Label( window, textvariable=server_ip_text )
    server_ip_text.set("FPGA server IP: " + constants.IP)
    server_ip_text_label.pack()

def show_port():
    # show fpga server port
    server_port_text_label =  tk.Label( window, textvariable=server_port_text )
    server_port_text.set("FPGA server port: " + str(constants.PORT))
    server_port_text_label.pack()

def init_server_response_msg():
    # label to show response
    server_response_label = tk.Label( window, textvariable=server_response_msg )
    server_response_msg.set(" ")
    server_response_label.pack()

def create_send_server_button():
    # add button to GUI that connects to fpga server
    connect_button = tk.Button(window, text="Send message", command=fpga_client.send)
    connect_button.pack()

def init_window_event_listeners():
    # on window close click
    window.protocol("WM_DELETE_WINDOW", on_close)

def init():
    configure_window()
    show_ip_address()
    show_port()
    create_send_server_button()
    init_server_response_msg()
    init_window_event_listeners()
