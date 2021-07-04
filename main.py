# main.py
#/usr/bin/python3

import sys
import argparse
import datetime
import json
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

    def recordMessage(self, day, message):
        assert(day < 8)
        self.messages[day] = message

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
    q - quit
******************************************************""")


if __name__ == "__main__":
    cmd : str
    
    currentDate = datetime.datetime.now()
    weekday = currentDate.today().weekday()
    mondayDate = datetime.datetime.now() - datetime.timedelta(days=currentDate.weekday())
    filePath = "reports/report_" + mondayDate.strftime("%m_%d_%Y") + ".json"

    print("filePath: " + filePath)

    # Check if report is already created
    if (os.path.isfile(filePath)):
        with open(filePath, "r") as f:
            report = json.load(f)
    else:
        report = StatusReport()
        report.setMondayDate(mondayDate)

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
        else:
            print("Invalid command")
    

    # Save report
    with open(filePath, "w") as f:
        json.dump(report.__dict__, f, indent=4, default=str)