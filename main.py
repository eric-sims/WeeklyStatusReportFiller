# main.py
#/usr/bin/python3

from enum import Enum
import sys
import argparse
import datetime
import xml.sax

class StatusReport(xml.sax.ContentHandler):
    def __init__(self) -> None:
        self.monday_date : datetime
        self.messages = [ "", "", "", "", "", "", ""]
        self.need_help = ""
        
    def hasMessage(self, day) -> bool:
        return len(self.messages[day]) > 0

    def setDate(self) -> None:
        self.monday_date = datetime.datetime.now()

    def recordMessage(self, day, message):
        assert(day < 8)
        self.messages[day] = message


arg_parser = argparse.ArgumentParser(description="Filling out the Weekly Status Report")
arg_parser.add_argument("-m", "--message", help="Reflect on the day", action="store_true")
arg_parser.add_argument("-e", "--email", help="Email to supervisor", action="store_true")

group = arg_parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args = arg_parser.parse_args()

def prompt():
    print( """************** Launchie Report Filler ****************
    w - Reflections for today's work
    p - Reflections for another weekday
    f - Finish the document
    e - Email report to supervisor
    h - help
    q - quit
******************************************************""")


if __name__ == "__main__":
    #import from [xml/JSON] file

    #evaluate command line arguments
    # ARGUMENTS TO ADD:
    # Add report of current date (Automatically add date of Monday and name)
    # Add report of previous date
    # Add comments of Planned accomplishments for next week
    # Add comments of Requested Assistance

    # Create Status Report object
    report = StatusReport()
    currentDate = datetime.datetime.now()
    weekday = currentDate.today().weekday()
    cmd : str

    prompt()
    while (1):
        cmd = input(">>> ")
        if cmd == 'q': break
        elif cmd == 'w':
            # print ("response for today")
            if report.hasMessage(weekday): 
                print("Already filled!")
            else: 
                reflection = input("enter reflection: ")
                report.recordMessage(weekday, reflection)
            print(report.messages)

        elif cmd == 'p':
            # print("response for previous days")
            custom_day = int(input("0 - Monday\n1 - Tuesday\n2 - Wednesday\n3 - Thursday\n4 - Friday\n5 - Saturday\n6 - Sunday\nday: "))
            if report.hasMessage(custom_day): 
                print("Already filled!")
            else: 
                reflection = input("enter reflection: ")
                report.recordMessage(custom_day, reflection)
        elif cmd == 'e':
            print("emailing supervisor")
        elif cmd == 'f':
            print("finishing documentation")
        elif cmd == 'h':
            prompt()
        

    # if args.message:
    #     if args.verbose:
    #         print("message")
    #         print(currentDate.strftime("%x"))

    # elif args.email:
    #     if args.verbose: print("email")