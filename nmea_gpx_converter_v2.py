"""
Get position from Water Linked Underwater GPS
"""


import argparse
from calendar import c
import csv

import json
import socket
import threading
import time
import requests
import threading
import datetime
from csv import DictWriter
import tkinter as tk
from tkinter import filedialog
from tkinter import Canvas
from tkinter import Label
# from tkinter import Text
# from tkinter import Entry
from threading import Thread
from gpx_converter import Converter
import platform
import subprocess

import os
from datetime import datetime
from time import strftime
from pynmeagps.nmeareader import NMEAReader
import pynmeagps.exceptions as nme

from math import floor

import customtkinter
from tkcalendar import Calendar, DateEntry

# create splash screen for .exe opening
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass        



def convert_dms_to_dec(value, dir):
	dPos = value.find(".")
	
	mPos = dPos - 2
	ePos = dPos
	
	main = float(value[:mPos])	
	min1 = float(value[mPos:])
		
#	print "degrees:'%s', minutes:'%s'\n" % (main, min1)
	
	newval = float(main) + float(min1)/float(60)
	
	if dir == "W":
		newval = -newval
	elif dir == "S":
		newval = -newval
	
	return newval

def format_coord(value):
	return "%.9f" % float(round(value, 8))

def format_time(value):
	pre = strftime("%Y-%m-%dT") #"2007-04-15T"
	hour = value[:2]
	minute = value[2:4]
	second = value[4:6]
	timeval = pre + hour + ":" + minute + ":" + second + "Z"
	return timeval

def convert(inputfile, outputfile,cal):
	print(inputfile)
	reader = csv.reader(open(inputfile, "r"))
	file = open(outputfile, 'w+')
	
	file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gpx version=\"1.0\" creator=\"nmea_conv\"\nxmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://www.topografix.com/GPX/1/0\"\nxsi:schemaLocation=\"http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd\">\n")
	
	points = []
	count = 0
	minlat = 90
	maxlat = -90
	minlon = 180
	maxlon = -180
	
	for row in reader:
		type = row[0]
        # ignore dodgy values - safe to do, as it's unlikely I'm going to be in the South Atlantic anytime soon
		if row[2] == 0.0 and row[4] == 0.0:
			continue
		if row[2] == '':
			continue


		if type == "$GPGGA" and  row[6] == "2":
			lat = convert_dms_to_dec(row[2], row[3])
			lon = convert_dms_to_dec(row[4], row[5])
			
			points.append([])
			points[count].append(row[1])
			
			if lat < minlat:
				minlat = lat
			if lat > maxlat:
				maxlat = lat
			if lon < minlon:
				minlon = lon
			if lon > maxlon:
				maxlon = lon
			
			points[count].append(lat)
			points[count].append(lon)

			points[count].append(row[9])
			count += 1

	
	strbounds = "<bounds minlat=\"" + format_coord(minlat) + "\" minlon=\"" + format_coord(minlon) + "\" maxlat=\"" + format_coord(maxlat) + "\" maxlon=\"" + format_coord(maxlon) + "\"/>\n<trk>\n<trkseg>\n"
	file.write(strbounds)
		
	for point in range(count):
		time = points[point][0]
		lat_val = points[point][1]
		long_val = points[point][2]
		elev = points[point][3]
		
		strElev = "%.4f" % float(elev)
		
		strtrkpt = "<trkpt lat=\"" + format_coord(lat_val) + "\" lon=\"" + format_coord(long_val) + "\">\n  <ele>" + strElev + "</ele>\n<time>" + format_time(time) + "</time>\n</trkpt>\n"
		file.write(strtrkpt)
	
	file.write("</trkseg>\n</trk>\n</gpx>\n")
	file.close()
	
	print(cal.selection_get())






def get_nmea_file_path():
    global nmea_file_path
    global ouput_dir
    nmea_file_path = filedialog.askopenfilename(title='Select NMEA file')
    ouput_dir = nmea_file_path.split(".")[0] + f".gpx"
    



def run_conversion():
	global cal
	convert(nmea_file_path, ouput_dir,cal)
	






app = tk.Tk()
app.title("")
app.geometry('300x500')

# customtkinter.set_appearance_mode("dark")

nmea_choose_button = tk.Button(app, text="Choose NMEA file",command=get_nmea_file_path)
nmea_choose_button.pack(pady=8,padx=8)



create_gpx_button = tk.Button(app, text="Create GPX",command=run_conversion)
create_gpx_button.pack(pady=8,padx=8)

# top = tk.Toplevel(app)

cal = Calendar(app,font="Arial 14", selectmode='day',cursor="hand1", year=2018, month=2, day=5)
cal.pack(pady=8,padx=8)
 


app.mainloop()