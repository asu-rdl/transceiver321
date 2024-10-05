"""
:author: Cody Roberson
:date: 2024-06-19
:version: 2.1.0
:license: All Rights Reserved
:contact: carobers@asu.edu
:organization: ASU

Description
-----------

This is a GUI for controlling the transceiver

Revisions
---------
+---------+---------------+---------------------------------------------------------------+
| Version | Author        | Revision                                                      |
+=========+===============+===============================================================+
| 2.1.0   | Cody Roberson | - Added linux support                                         |
|         |               | - Improved UI Design                                          |
|         |               | - Replaced success message with attenuation status indication |
+---------+---------------+---------------------------------------------------------------+

"""
import transceiver_serialdriver as tsd
import tkinter as tk
from tkinter import messagebox
import time

VERSION = "2.1.0"
_PAD = 10

def main():
    print("\nTrying to connect to the device...\n")
    sercom = tsd.connect()

    root = tk.Tk()
    root.title("Transceiver 3.2.1 GUI; sw_ver {}".format(VERSION))

    controlframe = tk.LabelFrame(root, text="Control", padx=_PAD, pady=_PAD)
    controlframe.grid(column=0, row=0, columnspan=8, padx=_PAD, pady=_PAD)

    address_label = tk.Label(controlframe, text="Address:")
    address_label.grid(column=0, row=0, padx=_PAD, pady=_PAD)

    address_entry = tk.Entry(controlframe)
    address_entry.grid(column=1, row=0, padx=_PAD, pady=_PAD)

    value_label = tk.Label(controlframe, text="Value:")
    value_label.grid(column=0, row=1, padx=_PAD, pady=_PAD)

    value_entry = tk.Entry(controlframe)
    value_entry.grid(column=1, row=1, padx=_PAD, pady=_PAD)

    # Generate list of attenuation values
    statusframe = tk.LabelFrame(root, text="Attenuation Status", padx=_PAD, pady=_PAD)
    statusframe.grid(column=0, row=3, columnspan=8, padx=_PAD, pady=_PAD)

    attentable = {}
    for i in range(8):
        attentable[i] = tk.Label(statusframe, text="{}: {}".format(i, "Unset"))
        attentable[i].grid(column = i, row = 3, padx = _PAD, pady = _PAD)


    def go_button_clicked():
        address = address_entry.get()
        value = value_entry.get()
        try:
            address = int(address)
            value = float(value)

            if address < 0 or address > 7:
                messagebox.showerror("Error", "Address must be between 0 and 7")
                return
            if value < 0 or value > 31.75:
                messagebox.showerror("Error", "Value must be between 0 and 31.75")
                return
            print("Setting attenuation at address {} to {}".format(address, value))
            result, msg = tsd.set_atten(sercom, address, value)
            if result:
                attentable[address].config(text="{}: {}".format(address, value))
                attentable[address].config(fg="black")
            else:
                attentable[address].config(text="{}: {}".format(address, "ERROR"))
                attentable[address].config(fg="red")
                messagebox.showerror("Error", msg)

        except ValueError:
            messagebox.showerror("Error", "Address must be an integer and value must be a float")
            root
            return
        
    def setallatten_clicked():
        value = value_entry.get()
        try:
            value = float(value)
            if value < 0 or value > 31.75:
                messagebox.showerror("Error", "Value must be between 0 and 31.75")
                return
            print("Setting all to {}".format(value))

            errors = []
            for address in range(8):
                result, msg = tsd.set_atten(sercom, address, value)
                msg = msg + " AT ADDRESS = {}\n".format(address)
                errors.append(msg)
                if result:
                    attentable[address].config(text="{}: {}".format(address, value))
                    attentable[address].config(fg="black")
                else:
                    attentable[address].config(text="{}: {}".format(address, "ERROR"))
                    attentable[address].config(fg="red")
                time.sleep(0.05)
            if len(errors) > 0:
                print(" \n".join(errors))
                messagebox.showerror("Error", " \n".join(errors))
        
        except ValueError:
            messagebox.showerror("Error", "Address must be an integer and value must be a float")
            return
        

    # Do something with the address and valu
    go_button = tk.Button(controlframe, text="Set Attenuation", command=go_button_clicked)
    setall_button = tk.Button(controlframe, text="Set All Attenuators", command=setallatten_clicked)
    value_entry.bind("<Return>", lambda x: go_button_clicked())
    address_entry.bind("<Return>", lambda x: go_button_clicked())
    go_button.grid(column=0, row=2, columnspan=2, padx=_PAD, pady=_PAD)
    setall_button.grid(column=2, row=2, columnspan=2, padx=_PAD, pady=_PAD)

    root.mainloop()


if __name__ == "__main__":
    main()