# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import tkinter as tk
import fpga_client
import constants
import utils

# create desktop app
window = tk.Tk()

# other files can use these variables to access desktop elements
server_ip_text = tk.StringVar()
server_port_text = tk.StringVar()
server_response_msg = tk.StringVar()

input_images = utils.get_input_images()
output_images = utils.get_output_images()

current_input_image_label = tk.Label(text='Input', image=input_images[0], compound='bottom')
current_input_image_label.image = input_images[0]

def on_close():
    print("Connection close")
    fpga_client.close()
    print("Closing program")
    window.destroy()

def configure_window():
    window.title('Kim Lehtinen - Zybo Z7-20 FPGA TCP client')
    # set main window size
    window.geometry("1500x800")

def create_footer_bar():
    ip_text = "FPGA server IP: " + constants.IP
    port_text = "FPGA server port: " + str(constants.PORT)
    final_text = ip_text + "    " + port_text
    status = tk.Label(window,text=final_text,bd=1,relief=tk.SUNKEN,anchor=tk.E)
    status.grid(row=2,column=0,columnspan=6,sticky=tk.W+tk.E)

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

## Image viewer ##

# Source code based on: https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/status.py
def forward(image_number):
	global current_input_image_label
	global button_forward
	global button_back

	current_input_image_label.grid_forget()
	current_input_image_label = tk.Label(text='Input', image=input_images[image_number-1], compound='bottom')
	button_forward = tk.Button(window, text=">>", command=lambda: forward(image_number+1))
	button_back = tk.Button(window, text="<<", command=lambda: back(image_number-1))
	
	if image_number == len(input_images):
		button_forward = tk.Button(window, text=">>", state=tk.DISABLED)

	current_input_image_label.grid(row=0, column=0, columnspan=3, sticky="N")
	button_back.grid(row=1, column=0)
	button_forward.grid(row=1, column=2)
	
# Source code based on: https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/status.py
def back(image_number):
	global current_input_image_label
	global button_forward
	global button_back

	current_input_image_label.grid_forget()
	current_input_image_label = tk.Label(text='Input', image=input_images[image_number-1], compound='bottom')
	button_forward = tk.Button(window, text=">>", command=lambda: forward(image_number+1))
	button_back = tk.Button(window, text="<<", command=lambda: back(image_number-1))

	if image_number == 1:
		button_back = tk.Button(window, text="<<", state=tk.DISABLED)

	current_input_image_label.grid(row=0, column=0, columnspan=3, sticky="N")
	button_back.grid(row=1, column=0)
	button_forward.grid(row=1, column=2)

def init_input_image_viewer():
    current_input_image_label.grid(row=0, column=0, columnspan=3, sticky="N")

    button_back = tk.Button(window, text="<<", command=back, state=tk.DISABLED)
    button_exit = tk.Button(window, text="Send", command=window.quit)
    button_forward = tk.Button(window, text=">>", command=lambda: forward(2))


    button_back.grid(row=1, column=0)
    button_exit.grid(row=1, column=1)
    button_forward.grid(row=1, column=2, pady=10)

def init_output_image_viewer():
    out = tk.Label(text='Output (placeholder)', image=output_images[0], compound='bottom')
    out.image = output_images[0]
    out.grid(row=0, column=3, columnspan=3, sticky="N")

def init_image_viewer():
    init_input_image_viewer()
    init_output_image_viewer()
## ./Image viewer ##

def init():
    configure_window()
    #create_send_server_button()
    #init_server_response_msg()
    init_image_viewer()

    create_footer_bar()

    init_window_event_listeners()

    # fill out
    window.columnconfigure(1, weight=1)
    window.rowconfigure(1, weight=1)
