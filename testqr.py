import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, OptionMenu
import qrcode

def generate_qr_code(medicine_name, time_to_take, additional_info):
    data = f"Medicine: {medicine_name}\nTime: {time_to_take}\nAdditional Info: {additional_info}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("medicine_qr_code.png")
    return img

def generate_qr_code_and_display():
    medicine_name = medicine_name_entry.get()
    time_to_take = f"{time_to_take_entry.get()} {ampm_var.get()}"
    additional_info = additional_info_entry.get()

    qr_code_image = generate_qr_code(medicine_name, time_to_take, additional_info)

    # QR code image
    qr_code_image.show()

# main window
root = tk.Tk()
root.title("QR Code Generator")

# labels and widgets
Label(root, text="Medicine Name:").pack()    
medicine_name_entry = Entry(root)
medicine_name_entry.pack()

Label(root, text="Time to Take:").pack()
time_to_take_entry = Entry(root)
time_to_take_entry.pack()

# AM/PM dropdown
Label(root, text="AM/PM:").pack()
ampm_var = StringVar(root)
ampm_var.set("AM")
ampm_menu = OptionMenu(root, ampm_var, "AM", "PM")
ampm_menu.pack()

Label(root, text="Additional Info:").pack()
additional_info_entry = Entry(root)
additional_info_entry.pack()

# Button to generate QR code and display
generate_button = Button(root, text="Generate QR Code", command=generate_qr_code_and_display)
generate_button.pack()

# Run main loop
root.mainloop()
