# Author: Kim Lehtinen <kim.lehtinen@student.uwasa.fi>

import fpga_client
import constants
import desktop
import tkinter as tk

# connnect to fpga server
fpga_client.connect()

# init desktop app
desktop.init()

# start desktop application
desktop.window.mainloop()