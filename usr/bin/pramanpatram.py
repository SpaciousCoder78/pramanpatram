#!/usr/bin/env python3
#pramanpatram
#developed by : Aryan Karamtoth of Department of Information Technology, KITS Warangal

#importing modules
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap



print("-----------------------------Pramanpatram---------------------------------")
print("-------------------------------v1.0---------------------------------------")
print("--------------------------------------------------------------------------")
print("-----------------------Developed by SpaciousCoder78-----------------------")
print("--------------------------------------------------------------------------")
print("-----------------------------Main Menu------------------------------------")
print('''CSV PATH
      Provide the Path of the CSV File
      Ensure that the participants name is in the column named "Attendee"''')
csvPath=input("Enter the path of the csv file: ")
print("--------------------------------------------------------------------------")
samplePath=input("Enter the path of the sample certificate: ")
print("--------------------------------------------------------------------------")
textcoords_x= int(input("Enter the x coordinate of the text: "))
textcoords_y= int(input("Enter the y coordinate of the text: "))
print("--------------------------------------------------------------------------")
textSize= int(input("Enter the size of the text: "))
print("--------------------------------------------------------------------------")
print("Enter RGB values of the text colour:")
r_value= int(input("Enter the R value: "))
g_value= int(input("Enter the G value: "))
b_value= int(input("Enter the B value: "))
print("--------------------------------------------------------------------------")
textWidth= int(input("Enter the width of the text: "))
print("--------------------------------------------------------------------------")
certificateText=input("Enter the text to be written on the certificate, refer to docs to know how to insert names: ")
certificatePath=input("Enter the path of the folder where the certificates are to be saved: ")

# read the csv file
persons = pd.read_csv(csvPath)

# find all columns that contain "Attendee" in their name
name_columns = [col for col in persons.columns if "Attendee" in col]

# iterate over the name columns
for name_column in name_columns:
    # convert the column to a list
    namelist = persons[name_column].tolist()

    # iterate over the names in the list
    for i in namelist:
        im = Image.open(samplePath)
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

        im.save(f"{certificatePath}+certificate_{i}.jpg")