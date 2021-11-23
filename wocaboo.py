import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import smtplib
from tkinter import messagebox
import cv2
import pytesseract, string
import numpy as np
from PIL import Image
import pyautogui
import time
import sys
from licensing.models import *
from licensing.methods import Key, Helpers
import os

try:
    os.remove(".work")
except:
    pass

def destroy():
    root.destroy()


def licensed(keyread):
    root = tk.Tk()
    RSAPubKey = "<RSAKeyValue><Modulus>rSsL8WogUCedv3iYiC3HMdBy63Uuolzf+zvquFgvDdz5Xj1mGWarieNFFo2fO5EWzYmL106YKV+O3d3oEoK0wPjfIhF7HxaRw6B99MJncMlfpKHF/JSxTThBJlio/GDi9BBCtQTNVXMkU4DLtLFpFV+BlSdUIBWAmbyaPd058xA/uGovODISSfRzZzrRUZEZ9ADVYNwViNT6slkuO9rb+oO+mfxuMSLMl4YzTLnfMpVJROnlWAs8LwLf6L40zt9eJ1mSN40LCeURDGN0bf0E7NNgzJM1YktTem3dpQJvQLufw6Cf7hXrwqLWbQxCM0sJApBSpJShpRQVcskV0mAElQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    auth = "WyI3MTcyNzgzIiwiRnJUYzViSVdmNVphUlJ4RjY5cklkcWhja0luR1cvcXpJY3Q2WHMycSJd"

    result = Key.activate(token=auth,\
                       rsa_pub_key=RSAPubKey,\
                       product_id=13265, \
                       key=keyread,\
                       machine_code=Helpers.GetMachineCode())

    if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
        # an error occurred or the key is invalid or it cannot be activated
        # (eg. the limit of activated devices was achieved)
        messagebox.showerror('License', 'The license does not work: {0}'.format(result[1]))
        root.destroy()
        exit()
    else:
        f = open(".work", "w+")
        f.close()
        # everything went fine if we are here!
        license_key = result[0]
        messagebox.showinfo('License', "License expires: " + str(license_key.expires))
        root.destroy()

try:
    f = open("license.key", "r+")
    keyread = f.read()
    f.close()
    licensed(keyread)
except:
        word = ""
        f = open("license.key", "w")
        root=tk.Tk()
        root.iconbitmap("wocaboo.ico")
        root.title("License input")
        def retrieve_input():
            inputValue=textBox.get("1.0","end-1c")
            word = inputValue
            f.write(word)
            f.close()
            licensed(word)
            root.destroy()
        textBox=Text(root, height=1, width=40)
        textBox.pack()
        buttonCommit=Button(root, height=1, width=10, text="Enter", 
                            command=lambda: retrieve_input())
        buttonCommit.pack()

            

        mainloop()


try:
    f = open(".work", "r+")
except:
    exit()

directory = ".\Database"    

if not os.path.exists(directory):
    os.makedirs(directory)


class App:
    def __init__(self, root):
        #setting title
        root.title("Wocaboo")
        root.iconbitmap("wocaboo.ico")
        #setting window size
        width=550
        height=320
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GMessage_21=tk.Message(root)
        ft = tkFont.Font(family='Times',size=28)
        GMessage_21["font"] = ft
        GMessage_21["fg"] = "#333333"
        GMessage_21["justify"] = "center"
        GMessage_21["text"] = "WOCABOO"
        GMessage_21.place(x=0,y=0,width=550,height=70)

        GButton_869=tk.Button(root)
        GButton_869["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=14)
        GButton_869["font"] = ft
        GButton_869["fg"] = "#000000"
        GButton_869["justify"] = "center"
        GButton_869["text"] = "Search in database"
        GButton_869.place(x=40,y=100,width=200,height=50)
        GButton_869["command"] = self.database

        GButton_839=tk.Button(root)
        GButton_839["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=33)
        GButton_839["font"] = ft
        GButton_839["fg"] = "#000000"
        GButton_839["justify"] = "center"
        GButton_839["text"] = "Start wocaboo 1.0"
        GButton_839.place(x=100,y=220,width=340,height=80)
        GButton_839["command"] = self.run

        GButton_599=tk.Button(root)
        GButton_599["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=14)
        GButton_599["font"] = ft
        GButton_599["fg"] = "#000000"
        GButton_599["justify"] = "center"
        GButton_599["text"] = "Request new words"
        GButton_599.place(x=300,y=100,width=200,height=50)
        GButton_599["command"] = self.request

    def run(self):
        messagebox.showinfo("Run", "Press 'OK' to start the program (program will start 10 secconds after clicking the button)")
        destroy()
        time.sleep(7)
        
        def hack():
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save('image.jpg')

            im = Image.open('image.jpg').convert('L')
            im = im.crop((350, 250, 1000, 290))
            im.save('image.jpg')

            pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'

            img = cv2.imread('image.jpg')
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            gray = cv2.bitwise_not(img_bin)
            kernel = np.ones((2, 1), np.uint8)
            img = cv2.erode(gray, kernel, iterations=1)
            img = cv2.dilate(img, kernel, iterations=1)
            out_below = pytesseract.image_to_string(img)

            final = out_below.replace("", "")
            print("---------")
            print("")
            print(final)
            print("")
            print("---------")
            print("")

            if "zemiak" in final:
                word = "die Kartoffel"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "maso" in final:
                word = "das Fleisch"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "marmeláda" in final or "marmeléda" in final:
                word = "die Marmelade"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "jest" in final:
                word = "Essen"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "chlieb" in final:
                word = "das Brot"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "Zemla" in final:
                word = "das Brotchen"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "ryba" in final:
                word = "der Fisch"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "ryza" in final or "tyta" in final or "ryZa" in final:
                word = "der Reis"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "salát" in final or "Salat" in final:
                word = "der Salat"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "ovocie" in final:
                word = "das Obst"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "polievka" in final:
                word = "die Suppe"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "kolác" in final or "koldé" in final:
                word = "der Kuchen"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "zelenina" in final or "Zelenina" in final:
                word = "das Gemuse"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "zdravy" in final:
                word = "gesund"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "taZzky" in final:
                word = "schwer"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "noha" in final:
                word = "das Bein"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "behat" in final:
                word = "laufen"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "viasy" in final or "vlasy" in final:
                word = "die Haare"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "rameno" in final:
                word = "der Arm"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "chrbat" in final:
                word = "der Rücken"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "koleno" in final:
                word = "das Knie"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            elif "hlava" in final:
                word = "der Kopf"
                img = Image.open("image.jpg")
                img.save(f".\database\{word}.jpg")
            else:
                word = "error"


            pyautogui.write(word)
            if word in "error":
                time.sleep(1)
                pyautogui.press("enter")
            else:
                pyautogui.press("enter")


        while True:
            time.sleep(3)
            hack()

    def database(self):
        word = ""
        f = open("words.txt", "r+")
        data = f.read()
        f.close()
        root=tk.Tk()
        root.iconbitmap("wocaboo.ico")
        root.title("Wocaboo databse search")
        def retrieve_input():
            inputValue=textBox.get("1.0","end-1c")
            word = inputValue
            if word in data :
                messagebox.showinfo("Search", "We sucessfully found this word in our database!")

            else:
                messagebox.showerror('Search', 'Sorry, but this word is not in our database :(')

        textBox=Text(root, height=1, width=40)
        textBox.pack()
        buttonCommit=Button(root, height=1, width=10, text="Search", 
                            command=lambda: retrieve_input())
        buttonCommit.pack()

            

        mainloop()


        

    def request(self):
        word = ""
        f = open("words.txt", "r+")
        data = f.read()
        f.close()
        root=tk.Tk()
        def destroye():
            root.destroy()
        root.iconbitmap("wocaboo.ico")
        root.title("Wocaboo word request")
        def retrieve_input():
            inputValue=textBox.get("1.0","end-1c")
            word = inputValue
            #-------------------------------------
            gmail_user = 'wordrequestwocaboo@gmail.com'
            gmail_password = 'wocaboo-1!'

            sent_from = gmail_user
            to = ['wocaboo@gmail.com']
            subject = 'Word request'
            body = word

            email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)

            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                print ("Email sent successfully!")
                destroye()
                messagebox.showinfo("Word requested", "Word was requested sucesfully!")
            except Exception as ex:
                ex = str(ex)
                messagebox.showerror("Some error ocourded", "Some error ocourded : " + ex)
            #-------------------------------------
        w = tk.Label(root, text="format : *<slovak word> = <german word>*(ag. chlieb = das Brot)")
        w.pack()
        textBox=Text(root, height=1, width=50)
        textBox.pack()
        u = tk.Label(root, text="Window will close automatically when your word request will be submited")
        u.pack()
        buttonCommit=Button(root, height=1, width=15, text="Reequest", 
                            command=lambda: retrieve_input())
        buttonCommit.pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
