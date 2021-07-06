# main.py
#/usr/bin/python3

#import sys
import argparse
import datetime
import jsonpickle
import os
#from pathlib import Path

class StatusReport():
    def __init__(self):
        self.monday_date : datetime
        self.messages = [ "", "", "", "", ""]
        self.next_week_goal = ""
        self.need_help = ""
    
    def overwrite(self, day) -> bool:
        n : str = ""
        if self.messages[day] != "":
            n = input("Already filled: " + self.messages[day] + "\nErase? (y/n)")
        else: return True

        n = n.lower().strip()
        if n == "y" or n == "yes":
            return True
        return False
        
    
    def setMondayDate(self, date) -> None:
        self.monday_date = date

    def recordMessage(self, day):
        assert(day < 8 and day > -1)

        if self.overwrite(day):
            self.messages[day] = input("enter reflection: ")
        else:
            return

    def recordMessage(self, day, message) -> None:
        assert(day < 8 and day > -1)
        print (message)
        if self.overwrite(day):
            self.messages[day] = message
            print("message written" + message)
        else:
            print("message not written")
            return
    
    def isFinished(self) -> bool:
        return self.next_week_goal != "" and self.need_help != ""

    def setNextWeekGoal(self) -> None:
        n : str = ""
        if self.next_week_goal != "":
            n = input("Already filled! Erase? (y/n)")
        if n == "y" or n == "Y" or n == "":
            self.next_week_goal = input("enter next step: ")
        else:
            return
        
    def setNeedHelp(self) -> None:
        n : str = ""
        if self.need_help != "":
            n = input("Already filled! Erase need help? (y/n)")
        if n == "y" or n == "Y" or n == "":
            self.need_help = input("enter need help: ")
        else:
            return

    def generate(self) -> str:
        if self.isFinished() == False:
            print("Not finished!")
            return ""
        else:
            return """Launchie Weekly Report
Name: Eric Sims
Date of Monday: """ + self.monday_date.strftime("%d %B %Y") + """

What I've learned from specific activities and accomplishments throughout the week
Monday: """ + self.messages[0] + """
Tuesday: """ + self.messages[1] + """
Wednesday: """ + self.messages[2] + """
Thursday: """ + self.messages[3] + """
Friday: """ + self.messages[4] + """

Planned accomplishments for next week: """ + self.next_week_goal + """

Requested assistance: """ + self.need_help
    

# Command line arguments
arg_parser = argparse.ArgumentParser(description="Filling out the Weekly Status Report")
arg_parser.add_argument("-m", "--message", type=str, help="Reflect on the day")
arg_parser.add_argument("-e", "--email", help="Email to supervisor")

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

verbose : bool = args.verbose
quiet : bool  = args.quiet 
cmd : str = ""

currentDate = datetime.datetime.now()
weekday = currentDate.weekday()
mondayDate = datetime.datetime.now() - datetime.timedelta(days=currentDate.weekday())
filePathJSON = "data/report_" + mondayDate.strftime("%m_%d_%Y") + ".json"
filePathTXT = "reports/report_" + mondayDate.strftime("%m_%d_%Y") + ".txt"

print("filePath: " + filePathJSON) if verbose else None

# Check if report is already created
if (os.path.isfile(filePathJSON)):
    with open(filePathJSON, "r") as f:
        report = jsonpickle.decode(f.read())
else:
    # no previous report made, make a new one
    report = StatusReport()
    report.setMondayDate(mondayDate)

if args.message != None:
    report.recordMessage(weekday, str(args.message))
    print("Recorded message for " + currentDate.strftime("%A"))
else:
    # INPUT EVENT LOOP
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
            custom_day = int(input("0 - Monday\t1 - Tuesday\t2 - Wednesday\t3 - Thursday\t4 - Friday\nday: "))
            report.recordMessage(custom_day)
            print(report.messages) if verbose else None
        
        elif cmd == 'e':
            print("emailing supervisor") if verbose else None
            txt = report.generate()
            with open(filePathTXT, "w") as f:
                f.write(txt)
            

        elif cmd == 'f':
            print("finishing documentation") if verbose else None
            report.setNextWeekGoal()
            report.setNeedHelp()

        elif cmd == 'h' or cmd == 'help':
            prompt()
        
        else:
            print("Invalid command")


# Save report
frozen = jsonpickle.encode(report)

with open(filePathJSON, "w") as f:
    f.write(frozen)





