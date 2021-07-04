# main.py
#/usr/bin/python3

import sys
import argparse
import datetime
import jsonpickle
import os
from pathlib import Path

class StatusReport():
    def __init__(self):
        self.monday_date : datetime
        self.messages = [ "", "", "", "", "", "", ""]
        self.next_step = ""
        self.need_help = ""
        
    def hasMessage(self, day) -> bool:
        return len(self.messages[day]) > 0

    def setMondayDate(self, date) -> None:
        self.monday_date = date

    def recordMessage(self, day):
        assert(day < 8 and day > -1)
        n : str = ""
        if self.hasMessage(day): 
            n = input("Already filled! Erase day? (y/n)")

        if n == "y" or n == "Y" or n == "":
            self.messages[day] = input("enter reflection: ")
        else:
            return

    def isFinished(self) -> bool:
        return self.next_step != "" and self.need_help != ""



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
    q - quit (auto saves)
******************************************************""")


if __name__ == "__main__":
    verbose = args.verbose
    quiet = args.quiet 

    cmd : str
    
    currentDate = datetime.datetime.now()
    weekday = currentDate.weekday()
    mondayDate = datetime.datetime.now() - datetime.timedelta(days=currentDate.weekday())
    filePath = "reports/report_" + mondayDate.strftime("%m_%d_%Y") + ".json"

    print("filePath: " + filePath) if verbose else None

    # Check if report is already created
    if (os.path.isfile(filePath)):
        with open(filePath, "r") as f:
            report = jsonpickle.decode(f.read())
    else:
        report = StatusReport()
        report.setMondayDate(mondayDate)

    prompt() if not quiet else None
    while (1):
        cmd = input(">>> ")
        if cmd == 'q': break
        
        elif cmd == 'w':
            print ("response for today") if verbose else None
            report.recordMessage(weekday)
            print(report.messages) if verbose else None
        
        elif cmd == 'p':
            print("response for previous days") if verbose else None
            custom_day = int(input("0 - Monday\t1 - Tuesday\t2 - Wednesday\t3 - Thursday\t4 - Friday\t5 - Saturday\t6 - Sunday\nday: "))
            report.recordMessage(custom_day)
            print(report.messages) if verbose else None
        
        elif cmd == 'e':
            print("emailing supervisor") if verbose else None
            print(report.messages)
            report.next_step = "sent"

        elif cmd == 'f':
            print("finishing documentation") if verbose else None
        
        elif cmd == 'h' or cmd == 'help':
            prompt()
        
        else:
            print("Invalid command")
    

    # Save report
    frozen = jsonpickle.encode(report)

    with open(filePath, "w") as f:
        f.write(frozen)