#!/bin/python

from PIL import Image, ImageDraw, ImageFont
import textwrap

"""
The MIT License (MIT)

Copyright (c) 2016 Saurabh Deochake

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

### A script which handles the creation of image and returns it to airbot.py to reply to a user. The image contains air quality index, quality and color of aqi.

image = Image.open('1.png')
image.load()

fill = "red"
index = "Index: 123.3"
quality = "Hazardous"
text = "The air quality index in New Brunswick is Hazardous. Please stay inside the houses!"

draw = ImageDraw.Draw(image)
draw.rectangle([130, 130, 190, 190 ],  fill=fill, outline = "black")

font = ImageFont.truetype("arial.ttf", 16)
# boldFont = ImageFont.truetype("arial.ttf", 16)

#draw.text((x, y),"Sample Text",(r,g,b))
draw.text((120, 210),quality,(0,0,0),font=font)
draw.text((120, 232), index, fill=fill, font=font )
#draw.text((100, 250), description, (0,0,0), font=font)

offset = 250
for line in textwrap.wrap(text, width=40):
    draw.text( (30, offset + 10), line, (0,0,0), font=font)
    offset += font.getsize(line)[1]

image.show()