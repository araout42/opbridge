import sys

if sys.version_info[0] == 3:
    from tkinter import *   ## notice lowercase 't' in tkinter here
else:
    from Tkinter import *   ## notice capitalized T in Tkinter


def send_mail():
    print(mail_list.get())

root = Tk()
mail_list = Entry(root)
myLabel = Label(root, text="Email a inviter a la converstation (separer par des virgules)!")


submit_btn = Button(root, text="Go", padx=50, command=send_mail)

myLabel.pack()
mail_list.pack()
submit_btn.pack()
root.mainloop()
