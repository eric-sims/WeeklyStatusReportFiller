# main.py
#/usr/bin/python3

import sys
import argparse
import datetime
import xml.sax

class StatusReport(xml.sax.ContentHandler):
    def __init__(self) -> None:
        self.monday_date : datetime
        self.messages = {
            'Monday'    : "",
            'Tuesday'   : "",
            'Wednesday' : "",
            'Thursday'  : "",
            'Friday'    : "",
        }
        self.need_help = ""
        
    def setDate(self) -> None:
        self.monday_date = datetime.datetime.now()

    def recordMessage(self, day, message):
        self.messages[day] = message

    

arg_parser = argparse.ArgumentParser(description="Filling out the Weekly Status Report")
arg_parser.add_argument("-m", "--message", help="Reflect on the day", action="store_true")
arg_parser.add_argument("-e", "--email", help="Email to supervisor", action="store_true")

group = arg_parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args = arg_parser.parse_args()


if __name__ == "__main__":
    #import from [xml/JSON] file

    #evaluate command line arguments
    # ARGUMENTS TO ADD:
    # Add report of current date (Automatically add date of Monday and name)
    # Add report of previous date
    # Add comments of Planned accomplishments for next week
    # Add comments of Requested Assistance
    
    currentDate = datetime.datetime.now()

    if args.message:
        if args.verbose:
            print("message")
            print(currentDate.strftime("%x"))

    elif args.email:
        if args.verbose: print("email")