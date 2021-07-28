from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException        
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import listdir
from os.path import isfile, join
import requests, time, pathlib, re, os, sys
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
from plyer import notification 
import webbrowser
import threading

old = 0

window = tk.Tk(className='Shubham computers')
window.geometry("500x500")
# T = tk.Text(window, height = 6, width = 53)
window['background']='#00c4cc'
image1 = Image.open("C:\\Users\\Lenovo\\Pictures\\Saved Pictures\\sc.png")
test = ImageTk.PhotoImage(image1)
label1 = tk.Label(image=test)
label1.image = test
label1.place(x=0, y=0)
global progress
progress = ttk.Progressbar(window, orient = tk.HORIZONTAL, length = 100, mode = 'indeterminate')
progress.pack(padx=5, pady=25, side=tk.BOTTOM)



class OnMyWatch:
    def __init__(self, driver):
        self.observer = Observer()
        self.driver = driver
  
    def run(self, driver):
        event_handler = Handler(driver)
        self.observer.schedule(event_handler, "C:\\Users\\Lenovo\\Desktop\\Busy_Automation", recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
    def __init__(self, driver):
        self.driver = driver
    
    def element_presence(self, by,xpath,time):
        element_present = EC.presence_of_element_located((by, xpath))
        WebDriverWait(self.driver, time).until(element_present)

    def msgTxt(self):
        global types, name, mobile_numbers, bill_no, amount, owner,message_text
        with open("C://Users//Lenovo//Desktop//Busy_Automation//details.txt") as file:
            types = file.readline()[:-1]
            name = file.readline()[:-1]
            mobile_numbers = [int("91"+mobile) for mobile in file.readline()[:-1].split(",")]
            bill_no = file.readline()[:-1]
            amount = file.readline()[:-1]
            owner = "Ajay Mantri"
        message_text='Dear '+name+' Please find the attached "'+types+'" for Rs. '+amount+'. Regards '+owner+'.'


    def send_msg(self, text):
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        txt_box=self.driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        self.msgTxt()
        txt_box.send_keys(text)
        txt_box.send_keys("\n")
        attachment_box = self.driver.find_element(By.XPATH, '//div[@title="Attach"]')
        attachment_box.click()
        pdf_box = self.driver.find_element(By.XPATH, '//input[@accept="*"]')
        mypath = "C://Users//Lenovo//Desktop//Busy_Automation"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            if file != 'details.txt':
                bill = file
        file_path = "C:\\Users\\Lenovo\\Desktop\\Busy_Automation\\" + bill; 
        pdf_box.send_keys(file_path)
        self.element_presence(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div', 30)
        send_btn = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div') 
        time.sleep(2) 
        send_btn.click()
        time.sleep(2)

    def search_contact(self, phone_no, text):
        self.element_presence(By.XPATH,'//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*', 30)
        searchbar = self.driver.find_element(By.XPATH, '//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*')
        searchbar.send_keys(phone_no)
        searchbar.send_keys("\n")

    def on_any_event(self, event):
        global old

        if event.is_directory:
            return None
  
        elif event.event_type == 'modified':
            global types, name, mobile_numbers, bill_no, amount, owner,message_text
            self.msgTxt()
            try:
                mypath = "C://Users//Lenovo//Desktop//Busy_Automation"
                onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                for file in onlyfiles:
                    if file != 'details.txt':
                        bill = file
                file_path = "C:\\Users\\Lenovo\\Desktop\\Busy_Automation\\" + bill
                statbuf = os.stat(file_path)
                new = statbuf.st_mtime
                if new - old > 0.5:
                    try:
                        driver.find_element(By.XPATH, '//div[@class="_1wQdF"]')
                        notification.notify(
                            title = "Phone not Connected",
                            message = "Please check your phone's connection",
                            app_icon = "sc.ico",
                            timeout  = 1
                        )
                    except: 
                        for mobile in mobile_numbers:
                            self.search_contact(mobile, message_text)            
                            self.send_msg(message_text)
                        notification.notify(
                            title = "Success",
                            message = "Your Message is delivered Successfully",
                            app_icon = "sc.ico",
                            timeout  = 1
                        )
                        window.update()
                old = new
            except Exception as e:
                print(e)
        # elif event.event_type == 'modified':
        #     try:
        #         #set_up_whatsapp(driver)#,moblie_no,message_text)
        #         for mobile in mobile_numbers:
        #             self.search_contact(mobile, message_text)
        #             self.send_msg(message_text)
        #         notification.notify(
        #             title = "Success",
        #             message = "Your Message is delivered Successfully",
        #             app_icon = "sc.ico",
        #             timeout  = 1
        #         )
        #     except Exception as e:
        #         print(e)   

def element_presence(driver, by,xpath,time):
    element_present = EC.presence_of_element_located((by, xpath))
    WebDriverWait(driver, time).until(element_present)

def initializing_driver():
    driveron = False; 
    options = FirefoxOptions()
    profile = "C://Users//Lenovo//AppData//Roaming//Mozilla//Firefox//Profiles//j5hi6h30.smprofile"
    options.add_argument("-profile")
    options.add_argument(profile)
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(executable_path="C://Users//Lenovo//Desktop//geckodriver.exe",options=options, capabilities=firefox_capabilities, service_args=["--marionette-port", "2828"])
    try:
        driver.get("https://web.whatsapp.com/")
        element_presence(driver,By.XPATH,'//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*', 30)
        notification.notify(
            title = "Success",
            message = "Connected to Whatsapp",
            app_icon = "sc.ico",
            timeout  = 1
        )
    except Exception as e:
        print(e)
        notification.notify(
            title = "Error",
            message = "Please Check your internet connection.",
            app_icon = "sc.ico",
            timeout  = 0.5
        )        
        global progress
        progress.stop()
        global counter
        counter = 1
        driver.close()
        sys.exit()
        # window.quit()
    return driver

def checkLoginStatus(driver):
    try:
        driver.find_element(By.XPATH, '//div[@class="O1rXL"]')
        return False
    except NoSuchElementException:
        return True

def watchDir(driver):
    watch = OnMyWatch(driver)
    watch.run(driver)

global t

def check_thread():
    global counter
    if counter == 1:
        b1["state"] = "normal"
        b2["state"] = "disabled"
        driver.close()
        window.update()
        counter = 0
    else:
        window.after(1000, check_thread)

def startProgress():
    global progress
    progress.start(10)

def startThread(cmd):
    global counter
    if cmd == 1:
        counter = 0
        b1["state"] = "disabled"
        b2["state"] = "normal"
        tp = threading.Thread(target=startProgress, args=(), daemon = True)
        tp.start() 
        t = threading.Thread(target=startDriver, args=(cmd,), daemon = True)
        t.start()
        window.after(1000, check_thread)
    else:
        counter = 1

def startDriver(cmd):
    if cmd == 1:
        try:
            os.system("taskkill /IM firefox.exe /F")
        except:
            print(e)
        global driver 
        driver = initializing_driver()
        if(not checkLoginStatus(driver)):
            notification.notify(
                title = "Please Login Whatsapp",
                message = "Please Open Firefox and Scan QR code to login.", 
                app_icon = "sc.ico",
                timeout  = 0.5
            )
            webbrowser.get('firefox').open_new_tab("https://web.whatsapp.com/")
            time.sleep(10)
        else:
            global progress
            progress.stop()
            watchDir(driver)   
    else:
        driver.close()

global b2,b1
b1=tk.Button(window, text="Start",  command=lambda: startThread(1), height=2, width=10, bg='black',fg='white')
b1.place(x=380, y=430)
b2=tk.Button(window, text="Stop",  command=lambda: startThread(2), height=2, width=10, bg='black', fg='white')
b2.place(x=30, y=430)
window.mainloop() 





############################################# Force #########################################################
def element_presence(driver,by,xpath,time):
    element_present = EC.presence_of_element_located((by, xpath))
    WebDriverWait(driver, time).until(element_present)

def send_msg(driver, text):
    element_presence(driver,By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
    txt_box=driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    txt_box.send_keys(text)
    txt_box.send_keys("\n")
    attachment_box = driver.find_element(By.XPATH, '//div[@title="Attach"]')
    attachment_box.click()
    pdf_box = driver.find_element(By.XPATH, '//input[@accept="*"]')
    pdf_box.send_keys(file_path)
    element_presence(driver,By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div', 30)
    send_btn = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div') 
    time.sleep(2) 
    send_btn.click()
    time.sleep(2)

def search_contact(driver, phone_no, text):
    element_presence(driver, By.XPATH,'//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*', 30)
    searchbar = driver.find_element(By.XPATH, '//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*')
    searchbar.send_keys(phone_no)
    searchbar.send_keys("\n")

def force():
    driver = initializing_driver()
    if(not checkLoginStatus(driver)):
        notification.notify(
            title = "Please Login Whatsapp",
            message = "Please Open Firefox and Scan QR code to login.",
            app_icon = "sc.ico",
            # the notification stays for 50sec
            timeout  = 1
        )        
        webbrowser.get('firefox').open_new_tab("https://web.whatsapp.com/")
        time.sleep(5)
    else:
        try:
        #set_up_whatsapp(driver)#,moblie_no,message_text)
            for mobile in mobile_numbers:
                search_contact(driver, mobile, message_text)            
                send_msg(driver, message_text)   
        except Exception as e:
            print(e)
    driver.close()
##################################################################################################