#!/usr/bin/env python3
# pramanpatram
# developed by : Aryan Karamtoth of Department of Information Technology, KITS Warangal

# importing modules
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    csv_path_entry.delete(0, tk.END)
    csv_path_entry.insert(0, filename)

def browse_sample():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    sample_path_entry.delete(0, tk.END)
    sample_path_entry.insert(0, filename)

def browse_folder():
    foldername = filedialog.askdirectory()
    certificate_path_entry.delete(0, tk.END)
    certificate_path_entry.insert(0, foldername)

def generate_certificates():
    csvPath = csv_path_entry.get()
    samplePath = sample_path_entry.get()
    textcoords_x = textcoords_x_entry.get()
    textcoords_y = textcoords_y_entry.get()
    textSize = text_size_entry.get()
    r_value = r_value_entry.get()
    g_value = g_value_entry.get()
    b_value = b_value_entry.get()
    textWidth = text_width_entry.get()
    certificateText = certificate_text_entry.get()
    certificatePath = certificate_path_entry.get()

    # Validation
    if not csvPath or not samplePath or not textcoords_x or not textcoords_y or not textSize or not r_value or not g_value or not b_value or not textWidth or not certificateText or not certificatePath:
        messagebox.showerror("Error", "Please fill all the fields.")
        return

    try:
        textcoords_x = int(textcoords_x)
        textcoords_y = int(textcoords_y)
        textSize = int(textSize)
        r_value = int(r_value)
        g_value = int(g_value)
        b_value = int(b_value)
        textWidth = int(textWidth)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for coordinates, size, RGB values, and text width.")
        return

    # read the csv file
    try:
        persons = pd.read_csv(csvPath)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV file: {e}")
        return

    # find all columns that contain "Attendee" in their name
    name_columns = [col for col in persons.columns if "Attendee" in col]

    if not name_columns:
        messagebox.showerror("Error", 'No columns with "Attendee" found in the CSV file.')
        return

    # iterate over the name columns
    for name_column in name_columns:
        # convert the column to a list
        namelist = persons[name_column].tolist()

        # iterate over the names in the list
        for i in namelist:
            try:
                im = Image.open(samplePath)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open sample certificate image: {e}")
                return

            draw = ImageDraw.Draw(im)
            location = (textcoords_y, textcoords_x)
            text_color = (r_value, g_value, b_value)
            selectFont = ImageFont.load_default()  # use the system's default font

            # format the text to be printed on the image
            text = f"{certificateText.replace('{name}', i)}"

            # wrap the text into multiple lines if it's too long
            wrapper = textwrap.TextWrapper(width=textWidth)  # decrease width to increase line breaks
            text_lines = wrapper.wrap(text=text)

            # draw each line of text
            for line in text_lines:
                draw.text(location, line, fill=text_color, font=selectFont)
                location = (location[0], location[1] + 35)  # increase vertical spacing between lines

            try:
                im.save(f"{certificatePath}/certificate_{i}.jpg")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save certificate image: {e}")
                return

    messagebox.showinfo("Success", "Certificates generated successfully!")

# Create the main window
root = tk.Tk()
root.title("Pramanpatram")

# Create and place the input fields
tk.Label(root, text="CSV PATH").grid(row=0, column=0, padx=10, pady=5, sticky='e')
csv_path_entry = tk.Entry(root, width=50)
csv_path_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_csv).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Sample Certificate Path").grid(row=1, column=0, padx=10, pady=5, sticky='e')
sample_path_entry = tk.Entry(root, width=50)
sample_path_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_sample).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="X Coordinate of the Text").grid(row=2, column=0, padx=10, pady=5, sticky='e')
textcoords_x_entry = tk.Entry(root, width=50)
textcoords_x_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Y Coordinate of the Text").grid(row=3, column=0, padx=10, pady=5, sticky='e')
textcoords_y_entry = tk.Entry(root, width=50)
textcoords_y_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Size of the Text").grid(row=4, column=0, padx=10, pady=5, sticky='e')
text_size_entry = tk.Entry(root, width=50)
text_size_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Enter RGB values of the text colour:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
tk.Label(root, text="R Value").grid(row=6, column=0, padx=10, pady=5, sticky='e')
r_value_entry = tk.Entry(root, width=50)
r_value_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="G Value").grid(row=7, column=0, padx=10, pady=5, sticky='e')
g_value_entry = tk.Entry(root, width=50)
g_value_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="B Value").grid(row=8, column=0, padx=10, pady=5, sticky='e')
b_value_entry = tk.Entry(root, width=50)
b_value_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Width of the Text").grid(row=9, column=0, padx=10, pady=5, sticky='e')
text_width_entry = tk.Entry(root, width=50)
text_width_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Text to be written on the certificate").grid(row=10, column=0, padx=10, pady=5, sticky='e')
certificate_text_entry = tk.Entry(root, width=50)
certificate_text_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Path of the folder where the certificates are to be saved").grid(row=11, column=0, padx=10, pady=5, sticky='e')
certificate_path_entry = tk.Entry(root, width=50)
certificate_path_entry.grid(row=11, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_folder).grid(row=11, column=2, padx=10, pady=5)

# Create and place the button
generate_button = tk.Button(root, text="Generate Certificates", command=generate_certificates, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
generate_button.grid(row=12, column=0, columnspan=3, pady=20)

# Run the main loop
root.mainloop()