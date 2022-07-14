import os
import datetime
from datetime import timedelta
from time import sleep

from getpass import getpass
from tkinter import filedialog, Tk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from functions import *


selem_("KLDZ")

print("")
print(f"{Fore.LIGHTYELLOW_EX}Program start ... ")
print("")
print("")


######################################### INITIALIZATION ###############################################


print(f"{Fore.LIGHTMAGENTA_EX}Please enter an Facebook account")
print("")

email_input =  input(f"{Fore.LIGHTCYAN_EX}Facebook account name (email) : ")
password_input = getpass(f"Facebook password (hidden) : {Style.RESET_ALL}")
print("")

print(f"{Fore.LIGHTMAGENTA_EX}Do you want to load the texts used during your last use?")
doyouload = input(f"If yes press Y otherwise enter any other key : {Style.RESET_ALL}")
print("")

if doyouload.lower() == "y":
    try:
        fichier = open("data/save_facebookGROUP.txt", "r")
        line = fichier.readline()
        data = []

        while line:
            data.append(line)
            line = fichier.readline()
        fichier.close()

        pub_text = data[0].strip()

        try:
            selected_file = data[1].strip()
            picture_flag = True
        except:
            picture_flag = False

    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}No backups found.{Style.RESET_ALL}")
        print('')
        doyouload = 'x'
        
if doyouload != "y":
    fichier_save = open("data/save_facebookGROUP.txt", "w")
    pub_text = input(f"{Fore.LIGHTMAGENTA_EX}Please enter your advertising text : {Style.RESET_ALL}")
    fichier_save.write(f"\n{pub_text}")
    print("")

    print(f"{Fore.LIGHTMAGENTA_EX}Would you like to upload an image? ")
    picture_flag = input(f"Enter yes otherwise enter any letter : {Style.RESET_ALL}")
    print("")

    if picture_flag.lower() == "yes":
        picture_flag = True
        print("")
        print(f"{Fore.LIGHTYELLOW_EX}Please select - in the window that will open - the image to upload : {Style.RESET_ALL}")
        print("")
        sleep(2)
        root = Tk()
        selected_file = filedialog.askopenfilename()
        fichier_save.write(f"\n{selected_file}")
        print(f"{Fore.LIGHTGREEN_EX}Image selected.")
        print("")
    else:
        picture_flag = False

print("")
print(f"{Fore.LIGHTCYAN_EX}Enter the URLs of the groups to ignore one after the other, separated by commas")
ignored_groups = input(f"{Fore.LIGHTCYAN_EX}If you don't want to ignore anything, leave the field empty : ")

if len(ignored_groups) > 0:
    ignored_groups = ignored_groups.split(',')

print("")
print(f"{Fore.LIGHTYELLOW_EX}loading ... {Style.RESET_ALL}") 

######################################## SETTINGS ###############################################
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
mobile_emulation = {"deviceName": "iPhone X"}
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1420, 1080")
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

time_supplement = 1
current=0
scroll_flag=0
ignore = False
#################################################################################################


def facebook_groups_chrome_core(email_input, password_input):
    """ Launching the page and navigating to groups """

    global driver

    service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.get("https://www.facebook.com/login/")
    driver.maximize_window()

    print("")
    print(f"{Fore.LIGHTGREEN_EX}Settings: OK. {Style.RESET_ALL}")
    print("")
    print(f"{Fore.LIGHTYELLOW_EX}Connexion to Facebook : In progress ... {Style.RESET_ALL}")

    email = driver.find_element(by=By.ID, value="m_login_email")
    mdp = driver.find_element(by=By.ID, value="m_login_password")
    email.send_keys(email_input)
    mdp.send_keys(password_input)
    sleep(2)

    driver.execute_script("""document.querySelectorAll("[data-cookiebanner='accept_button']")[0].click()""")
    sleep(2)

    button_submit = driver.find_element(by=By.NAME, value="login")
    button_submit.click()

    sleep(5)
    driver.refresh()

    print("")
    print(f"{Fore.LIGHTGREEN_EX}Connexion to Facebook : OK. {Style.RESET_ALL}")

    # Navigation vers les groupes
    driver.get("https://m.facebook.com/groups_browse/your_groups/")
    sleep(3)


def pub_iteration(current, long, scroll_flag, ignored_groups, picture_flag, selected_file):
    """ Function calling itself allowing to enter
    and post in the different groups of the list """

    while current < long:
        current_group_number = int(((current + 2) // 2) + 0.5)
        date_time = datetime.datetime.now() + timedelta(hours=2)
        format_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        ignore = False

        print("")
        print(f"Group N° {current_group_number} in progress / Total number of loaded groups : {long // 2}")
        print("")
        
        if scroll_flag > 0:
            for x in range(1, scroll_flag):
                driver.execute_script("""window.scrollTo(0,document.querySelector("body").scrollHeight)""")
                sleep(2)

        sleep(5)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_7hkg')))
        groups = driver.execute_script("return document.getElementsByClassName('_7hkg')")

        sleep(5)

        current_url_group = driver.execute_script(f"""return document.getElementsByClassName("_7hkg")[{current}].attributes[1].textContent""")
        current_url_group = current_url_group.split('/')[2]

        # Checks if the current group is one of the groups to ignore
        if len(ignored_groups) > 0:
            for i in ignored_groups:
                try:
                    if i.split('/')[4] == current_url_group:
                        ignore = True
                except:
                    ignore = False
        else:
            ignore = False

        current_group_name = driver.execute_script(f"""return document.getElementsByClassName("_7hkg")[{current}].text""")

        if not ignore:
            groups[current].click()

            sleep(4)
            print(f"Target group : {current_group_name}")
            print('')

            # try block for the few groups on which it is not possible to post (missing fields, group restrictions..)
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[onclick]')))
                write_post = driver.find_element(by=By.CSS_SELECTOR, value="div[onclick]")
                sleep(2)
                write_post.click()
            except:
                print(f"{Fore.LIGHTRED_EX}{format_time} : Text fields unavailable.{Style.RESET_ALL}")        

            else:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[aria-label]')))
                input_text = driver.find_element(by=By.CSS_SELECTOR, value="textarea[aria-label]")
                sleep(2)

                input_text.send_keys(pub_text)
                sleep(1)

                if picture_flag:
                    input_picture = driver.find_element(by=By.ID, value="photo_input")
                    sleep(2)

                    input_picture.send_keys(os.path.abspath(selected_file))
                    #input_picture.clear()
                    sleep(3)

                driver.execute_script("document.getElementsByClassName('_54k8 _52jg _56bs _26vk _56b_ _56bw _56bv')[1].click()")
                sleep(5)

                #alert = driver.switch_to.alert
                #alert.accept()

                print("")
                print(f"{Fore.LIGHTGREEN_EX}{format_time} : Ad posted successfully.{Style.RESET_ALL}")
                print("")

                log_save('facebookGroups', format_time, None, current_group_name, current_url_group, None)

                sleep(10)
                sleep(time_supplement)

            sleep(3)
            driver.execute_script("window.history.go(-1)")
        else:
            print("")
            print(f"{Fore.LIGHTYELLOW_EX}The group : {current_group_name[:84]}(...) was ignored as stipulated in the parameters.{Style.RESET_ALL}")

        current += 2

    driver.execute_script("""window.scrollTo(0,document.querySelector("body").scrollHeight)""")
    sleep(2)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_7hkg')))
    groups = driver.execute_script("return document.getElementsByClassName('_7hkg')")
    scroll_flag += 2

    pub_iteration(current, len(groups), scroll_flag, ignored_groups, picture_flag, selected_file)

    driver.close()


################################# EXECUTION #################################


while True:
    facebook_groups_chrome_core(email_input, password_input)

    sleep(5+time_supplement)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_7hkg')))
    groups = driver.execute_script("return document.getElementsByClassName('_7hkg')")
    long = len(groups)

    pub_iteration(current, long, scroll_flag, ignored_groups, picture_flag, selected_file)