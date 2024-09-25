#!/usr/bin/env python3
# pramanpatram
# developed by : Aryan Karamtoth of Department of Information Technology, KITS Warangal

# importing modules
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap
import PySimpleGUI as sg

# Define the layout of the GUI
layout = [
    [sg.Text('CSV PATH')],
    [sg.InputText(key='csvPath')],
    [sg.Text('Sample Certificate Path')],
    [sg.InputText(key='samplePath')],
    [sg.Text('X Coordinate of the Text')],
    [sg.InputText(key='textcoords_x')],
    [sg.Text('Y Coordinate of the Text')],
    [sg.InputText(key='textcoords_y')],
    [sg.Text('Size of the Text')],
    [sg.InputText(key='textSize')],
    [sg.Text('Enter RGB values of the text colour:')],
    [sg.Text('R Value'), sg.InputText(key='r_value')],
    [sg.Text('G Value'), sg.InputText(key='g_value')],
    [sg.Text('B Value'), sg.InputText(key='b_value')],
    [sg.Text('Width of the Text')],
    [sg.InputText(key='textWidth')],
    [sg.Text('Text to be written on the certificate')],
    [sg.InputText(key='certificateText')],
    [sg.Text('Path of the folder where the certificates are to be saved')],
    [sg.InputText(key='certificatePath')],
    [sg.Button('Generate Certificates')]
]

# Create the window
window = sg.Window('Pramanpatram', layout)

# Event loop to process events and get the values of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Generate Certificates':
        # Validation
        if not values['csvPath'] or not values['samplePath'] or not values['textcoords_x'] or not values['textcoords_y'] or not values['textSize'] or not values['r_value'] or not values['g_value'] or not values['b_value'] or not values['textWidth'] or not values['certificateText'] or not values['certificatePath']:
            sg.popup('Error', 'Please fill all the fields.')
            continue

        try:
            textcoords_x = int(values['textcoords_x'])
            textcoords_y = int(values['textcoords_y'])
            textSize = int(values['textSize'])
            r_value = int(values['r_value'])
            g_value = int(values['g_value'])
            b_value = int(values['b_value'])
            textWidth = int(values['textWidth'])
        except ValueError:
            sg.popup('Error', 'Please enter valid numeric values for coordinates, size, RGB values, and text width.')
            continue

        csvPath = values['csvPath']
        samplePath = values['samplePath']
        certificateText = values['certificateText']
        certificatePath = values['certificatePath']

        # read the csv file
        try:
            persons = pd.read_csv(csvPath)
        except Exception as e:
            sg.popup('Error', f'Failed to read CSV file: {e}')
            continue

        # find all columns that contain "Attendee" in their name
        name_columns = [col for col in persons.columns if "Attendee" in col]

        if not name_columns:
            sg.popup('Error', 'No columns with "Attendee" found in the CSV file.')
            continue

        # iterate over the name columns
        for name_column in name_columns:
            # convert the column to a list
            namelist = persons[name_column].tolist()

            # iterate over the names in the list
            for i in namelist:
                try:
                    im = Image.open(samplePath)
                except Exception as e:
                    sg.popup('Error', f'Failed to open sample certificate image: {e}')
                    continue

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
                    sg.popup('Error', f'Failed to save certificate image: {e}')
                    continue

        sg.popup('Success', 'Certificates generated successfully!')

window.close()