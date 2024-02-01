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

# create splash screen for .exe opening
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass




XML_HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

GPX_NS = " ".join(
    (
        'xmlns="http://www.topografix.com/GPX/1/1"',
        'creator="pynmeagps" version="1.1"',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
        'http://www.topografix.com/GPX/1/1/gpx.xsd"',
    )
)
GITHUB_LINK = "https://github.com/semuconsulting/pynmeagps"


class NMEATracker:
    """
    NMEATracker class.
    """

    def __init__(self, infile):
        """
        Constructor.
        """

        self._filename = infile
        self._infile = None
        self._trkfname = None
        self._trkfile = None
        self._nmeareader = None
        self._connected = False

    def open(self):
        """
        Open datalog file.
        """

        self._infile = open(self._filename, "rb")
        self._connected = True

    def close(self):
        """
        Close datalog file.
        """

        if self._connected and self._infile:
            self._infile.close()

    def reader(self, validate=False):
        """
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        """

        i = 0
        self._nmeareader = NMEAReader(self._infile, validate=validate)

        self.write_gpx_hdr()

        for (_, msg) in self._nmeareader:  # invokes iterator method
            try:
                if msg.msgID == "GGA":
                    dat = datetime.now()
                    tim = msg.time
                    dat = (
                        dat.replace(
                            year=dat.year,
                            month=dat.month,
                            day=dat.day,
                            hour=tim.hour,
                            minute=tim.minute,
                            second=tim.second,
                        ).isoformat()
                        + "Z"
                    )
                    if msg.quality == 1:
                        fix = "3d"
                    elif msg.quality == 2:
                        fix = "2d"
                    else:
                        fix = "none"
                    self.write_gpx_trkpnt(
                        msg.lat,
                        msg.lon,
                        ele=msg.alt,
                        time=dat,
                        fix=fix,
                        hdop=msg.HDOP,
                    )
                    i += 1
            except (nme.NMEAMessageError, nme.NMEATypeError, nme.NMEAParseError) as err:
                print(f"Something went wrong {err}")
                continue

        self.write_gpx_tlr()

        print(f"\n{i} GGA message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {self._trkfname}")

    def write_gpx_hdr(self):
        """
        Open gpx file and write GPX track header tags
        """

        timestamp = strftime("%Y%m%d%H%M%S")

        self._trkfname = self._filename.split(".")[0] + f".gpx"
        print(self._trkfname)

        self._trkfile = open(self._trkfname, "a")

        date = datetime.now().isoformat() + "Z"
        gpxtrack = (
            XML_HDR + "<gpx " + GPX_NS + ">"
            f"<metadata>"
            f'<link href="{GITHUB_LINK}"><text>pynmeagps</text></link><time>{date}</time>'
            "</metadata>"
            "<trk><name>GPX track from NMEA datalog</name><trkseg>"
        )

        self._trkfile.write(gpxtrack)

    def write_gpx_trkpnt(self, lat: float, lon: float, **kwargs):
        """
        Write GPX track point from NAV-PVT message content
        """

        trkpnt = f'<trkpt lat="{lat}" lon="{lon}">'

        # these are the permissible elements in the GPX schema for wptType
        # http://www.topografix.com/GPX/1/1/#type_wptType
        for tag in (
            "ele",
            "time",
            "magvar",
            "geoidheight",
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "sym",
            "type",
            "fix",
            "sat",
            "hdop",
            "vdop",
            "pdop",
            "ageofdgpsdata",
            "dgpsid",
            "extensions",
        ):
            if tag in kwargs:
                val = kwargs[tag]
                trkpnt += f"<{tag}>{val}</{tag}>"

        trkpnt += "</trkpt>"

        self._trkfile.write(trkpnt)

    def write_gpx_tlr(self):
        """
        Write GPX track trailer tags and close file
        """

        gpxtrack = "</trkseg></trk></gpx>"
        self._trkfile.write(gpxtrack)
        self._trkfile.close()

def get_nmea_file_path():
    global nmea_file_path
    nmea_file_path = filedialog.askopenfilename(title='Select NMEA file')

# def choose_ouput_dir():
#     global ouput_dir
#     ouput_dir = filedialog.askdirectory(title='Select gpx output Directory')


def run_conversion():
    tkr = NMEATracker(nmea_file_path)
    tkr.open()
    tkr.reader()
    tkr.close()






app = customtkinter.CTk()
app.title("")
app.geometry('160x130')
customtkinter.set_appearance_mode("dark")

nmea_choose_button = customtkinter.CTkButton(app, text="Choose NMEA file",command=get_nmea_file_path)
nmea_choose_button.grid(row=1,pady=8,padx=8)

# gpx_choose_button = customtkinter.CTkButton(app, text="Choose gpx directory",command=choose_ouput_dir)
# gpx_choose_button.grid(row=2,pady=8,padx=8)

create_gpx_button = customtkinter.CTkButton(app, text="Create GPX",command=run_conversion)
create_gpx_button.grid(row=2,pady=8,padx=8)








app.mainloop()