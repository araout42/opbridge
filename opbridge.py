import sys
import time
import os
import signal
import subprocess
import smtplib
import uuid

from PIL import ImageTk
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.version_info[0] == 3:
    from tkinter import *   ## notice lowercase 't' in tkinter here
else:
    from Tkinter import *   ## notice capitalized T in Tkinter


DOORBELL_PIN = 26
DOORBELL_SCREEN_ACTIVE_S = 60
RING_SFX_PATH = None  # If None, no sound effect plays
ENABLE_EMAIL = True
FROM_EMAIL = 'arthur.raout@gmail.com'
FROM_EMAIL_PASSWORD = 'dlpxshfcydeakoli'


#def show_screen():
#    os.system("tvservice -p")
#    os.system("xset dpms force on")


#def hide_screen():
#    os.system("tvservice -o")


def send_email_notification(chat_url):
    if ENABLE_EMAIL:
        sender = EmailSender(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        email = Email(
            sender,
            'Invitation, conversation',
            'Bonjour',
            'Vous avez ete invite a une conversation video sur  %s' % chat_url,
        )
        email.send(mail_list.get())


def ring_doorbell():
    SoundEffect(RING_SFX_PATH).play()

    chat_id = str(uuid.uuid4())
    video_chat = VideoChat(chat_id)
    send_email_notification(video_chat.get_chat_url())
   
#    show_screen()

    video_chat.start()
    #time.sleep(DOORBELL_SCREEN_ACTIVE_S)
    #video_chat.end()

    #hide_screen()


class SoundEffect:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        if self.filepath:
            subprocess.Popen(["aplay", self.filepath])


class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "https://call.oopercast.com/%s" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["chromium", "-kiosk", "--no-sandbox", self.get_chat_url()])
        else:
            print("Can't start video chat -- already started or missing chat id")

    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)


class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class Email:
    def __init__(self, sender, subject, preamble, body):
        self.sender = sender
        self.subject = subject
        self.preamble = preamble
        self.body = body

    def send(self, to_email):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.sender.email
        msgRoot['To'] = to_email
        msgRoot.preamble = self.preamble

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgText = MIMEText(self.body)
        msgAlternative.attach(msgText)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.sender.email, self.sender.password)
        smtp.sendmail(self.sender.email, to_email, msgRoot.as_string())
        smtp.quit()


class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:
            print("Starting Doorbell...")
            #self._setup_gpio()
            print("Waiting for doorbell rings...")
            #self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

        #finally:
        #    self._cleanup()

    def _wait_forever(self):
        while True:
            time.sleep(0.1)

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)

    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)
        #show_screen()


if __name__ == "__main__":
    root = Tk()
    img = ImageTk.PhotoImage(file="logo.png")
    root['background'] = '#000000'
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen',True)
    
    label = Label(root, image=img)
    label.configure(bg='black')
    label.pack(side='top', fill='both', expand='yes')


    mail_list = Entry(root, width=100)
    mail_list.configure(bg='black', fg='white')
    myLabel = Label(root, text="Email a inviter a la converstation (separer par des virgules)!")
    myLabel.configure(bg='black', fg='white')


    submit_btn = Button(root, text="Go", padx=50, command=ring_doorbell)
    submit_btn.configure(bg='black', fg='white', relief=SUNKEN)
    myLabel.pack()
    submit_btn.pack(side='bottom', pady=50)
    mail_list.pack(side='bottom')
    doorbell = Doorbell(DOORBELL_PIN)
    doorbell.run()
    root.mainloop()
