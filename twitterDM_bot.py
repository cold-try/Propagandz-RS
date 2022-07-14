import datetime
from datetime import timedelta

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, WebDriverException, JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from colorama import Fore, Style
from time import sleep
from random import shuffle
from getpass import getpass

from functions import *


selem_("KLDZ")

print("")
print(f"{Fore.LIGHTYELLOW_EX}Program start ... ")
print("")
print("")


#################################### INITIALIZATION ##########################################

print(f"{Fore.LIGHTMAGENTA_EX}Please enter one or two Twitter accounts (a rotation will be made between the two accounts) ;")
print("")

email_input = input(f"{Fore.LIGHTCYAN_EX}Twitter account n°1 (email) : ")
password_input = getpass(f"Twitter password n°1 (caché) : ")
username_input = input(f"Twitter username n°1 (username) : ")
print("")
email_input_2 = input(f"Twitter account n°2 (email) : ")
password_input_2 = getpass(f"Twitter password n°2 (caché) : ")
username_input_2 = input(f"Twitter username n°2 (username) : {Style.RESET_ALL}")

print("")
url_group =  input(f"{Fore.LIGHTCYAN_EX}Please enter group URL : ")
print("")

print("")
print(f"{Fore.LIGHTMAGENTA_EX}Do you want to load the texts used during your last use?")
doyouload = input(f"If yes press Y otherwise enter any other key : {Style.RESET_ALL}")
print("")

if doyouload.lower() == "y":
    try:
        fichier = open("data/save_twitterDM.txt", "r")
        line = fichier.readline()
        data = []

        while line:
            data.append(line)
            line = fichier.readline()
        fichier.close()

        first_mssg = data[0].strip()
        second_mssg = data[1].strip()
        third_mssg = data[2].strip()
        fourth_mssg = data[3].strip()
        five_mssg = data[4].strip()

    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}No backups found.{Style.RESET_ALL}")
        print('')
        doyouload = 'x'
        
if doyouload != "y":
    fichier_save = open("data/save_twitterDM.txt", "w")

    print(f"{Fore.LIGHTMAGENTA_EX}Please enter five different messages, each time you send one of the three messages will be randomly selected (avoid SPAM)")
    print(f"If you wish to send a personalized message with the name of the recipient, write [RECEPTIVE] in the desired place (the square brackets are essential) ;")
    print("")
    first_mssg = input(f"{Fore.LIGHTWHITE_EX}Message n°1 : ")
    fichier_save.write(f"\n{first_mssg}")
    print("")
    second_mssg = input("Message n°2 : ")
    fichier_save.write(f"\n{second_mssg}")
    print("")
    third_mssg = input(f"Message n°3 : ")
    fichier_save.write(f"\n{third_mssg}")
    print("")
    fourth_mssg = input(f"Message n°4 : ")
    fichier_save.write(f"\n{fourth_mssg}")
    print("")
    five_mssg = input(f"Message n°5 : {Style.RESET_ALL}")
    fichier_save.write(f"\n{five_mssg}")
    fichier_save.close()

print("")
print(f"{Fore.LIGHTMAGENTA_EX}Do you want to resume the script at a particular place? ")
reload_script = input(f"{Fore.LIGHTMAGENTA_EX}If yes enter YES otherwise enter any key : ")
print("")

if reload_script.lower() == "yes":
    while True:
        current_number = input(f"{Fore.LIGHTMAGENTA_EX}What is the current scroll flag number? : ")
        try:
            scroll_flag = int(current_number)
            break
        except:
            print("")
            print(f"{Fore.LIGHTRED_EX}Please enter a number.{Style.RESET_ALL}")
            print("")
else:
    scroll_flag = 0

print("")
print(f"{Fore.LIGHTYELLOW_EX}loading ... {Style.RESET_ALL}") 

######################################## SETTINGS ###############################################
options = webdriver.ChromeOptions() 
######################################### NO DETECTION ##########################################
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
#################################################################################################
options.add_argument("--start-maximized")
options.add_argument('--window-size=1920,1080')
options.add_argument("--headless")

current_accouct = 2
current = 1
total_current_members = 1
mssg_success = 0
mssg_fail = 0
signal = False
time_supplement = 0
big_wait_values = [200, 250, 130, 220, 210, 200, 205]
#################################################################################################


def chrome_core(email_input, password_input, username_input):
    " Launching the page and navigating to groups "

    global driver, long_person

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.get("https://twitter.com/login")

    sleep(5)
    print("")
    print(f"{Fore.LIGHTGREEN_EX}Parameters : OK. {Style.RESET_ALL}")
    print("")
    print(f"{Fore.LIGHTYELLOW_EX}Connexion to Twitter : In progress ... {Style.RESET_ALL}")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='text']")))

    email = driver.find_element(by=By.CSS_SELECTOR, value="[name='text']")
    email.send_keys(email_input)
    sleep(2)

    driver.execute_script("""document.querySelectorAll("[role='button']")[2].click()""")
    sleep(4)

    try:
        security = driver.find_element(by=By.CSS_SELECTOR, value="[name='text']")
        security.send_keys(username_input)

        print("")
        print(f"{Fore.LIGHTYELLOW_EX}Additional security required ...{Style.RESET_ALL}")
        print("")

        sleep(2)
        driver.execute_script("""document.querySelectorAll("[role='button']")[1].click()""")
        sleep(4)

    except:
        print("")
        print(f"{Fore.LIGHTGREEN_EX}No additional security {Style.RESET_ALL}")
        print("")

    finally:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='password']")))
        mdp = driver.find_element(by=By.CSS_SELECTOR, value="[name='password']")
        sleep(2)
        mdp.send_keys(password_input)
        sleep(2)
        driver.execute_script("""document.querySelectorAll("[role='button']")[3].click()""")

    print("")
    print(f"{Fore.LIGHTGREEN_EX}Connexion to Twitter : OK. {Style.RESET_ALL}")
    print("")
    print("")
    print(f"{Fore.LIGHTYELLOW_EX}Connecting to database in progress ...{Style.RESET_ALL}")

    db_connection()

    # Navigation to groups
    sleep(5+time_supplement)
    driver.get(url_group+"/followers")
    sleep(7+time_supplement)


def pub_iteration(first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, scroll_flag):
    """ Function calling itself allowing to enter
    and post in the different groups of the list """

    global current, total_current_members, mssg_success, mssg_fail, signal

    already_done = False

    if scroll_flag > 0:
        for x in range(1, scroll_flag):
            driver.execute_script("""window.scrollTo(0,document.querySelector("body").scrollHeight)""")
            sleep(5+time_supplement)

    while True:

        date_time = datetime.datetime.now() + timedelta(hours=2)
        format_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

        if mssg_success % 900 == 0 and signal:
            driver.close()
            signal = False

            if current_accouct == 1:
                current_accouct = 2
                e = email_input
                p = password_input
                u = username_input
            else:
                current_accouct = 1
                e = email_input_2
                p = password_input_2
                u = username_input_2

            print("")
            print(f"{Fore.LIGHTYELLOW_EX}{format_time} : Limit reached on this account, login to next account ... {Style.RESET_ALL}")
            print("")
            chrome_core(e, p, u)
            print("")
            print(f"{Fore.LIGHTGREEN_EX}Reboot successful. {Style.RESET_ALL}")
            print("")

        if mssg_success % 50 == 0 and signal:
            signal = False
            shuffle(big_wait_values)
            print("")
            print(f"{Fore.LIGHTYELLOW_EX}{format_time} : Pausing the program for {big_wait_values[0]} seconds ... (SPAM){Style.RESET_ALL}")
            recap_logs(mssg_success, mssg_fail, "actif", format_time, scroll_flag)
            sleep(big_wait_values[0]) 
            print("")
            print(f"{Fore.LIGHTYELLOW_EX}Resuming the program ..{Style.RESET_ALL}")
            print("")  
        
        if mssg_success % 10 == 0 and signal:
            signal = False
            recap_logs(mssg_success, mssg_fail, "actif", format_time, scroll_flag)

        person_group = driver.execute_script("return document.getElementsByClassName('css-4rbku5 css-18t94o4 css-1dbjc4n r-1niwhzg r-1loqt21 r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu')")
        long_person = len(person_group)
         
        print("")
        print("Member N° " + str(total_current_members) + " in progress.")
        print("Member number on the current scroll list : " + str(current))
        print("Total number of loaded members : " + str(long_person))
        print("Scroll flag n° : " + str(scroll_flag))
        
        ######### Followers list #########
        ################################## 

        sleep(5)

        try:
            for_try = person_group[current]
            user_name = person_group[current].get_attribute('href').split('/')[-1]
            is_solvable = verification_name(user_name, 'TWITTERDM', True)

            if is_solvable:
                already_done = True
            else:
                url_member = f"https://twitter.com/{user_name}"
                driver.execute_script(f"window.open('{url_member}', '_blank')")
                #ActionChains(driver).move_to_element(person_group[current]).key_down(Keys.COMMAND).click(person_group[current]).key_up(Keys.COMMAND).perform()
                sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
                driver.refresh()
                sleep(5)
                #person_group[current].click()
                verification_name(user_name, 'TWITTERDM')

        except IndexError:
            driver.execute_script("window.scrollTo(-5000,document.body.scrollHeight)")
            scroll_flag = scroll_flag + 1

            sleep(6+time_supplement)
            #try:
                #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span')))
            #except:
                #print(f"{Fore.LIGHTRED_EX}{format_time} : Impossible de charger la liste de membres !{Style.RESET_ALL}")

            person_group = driver.execute_script("return document.getElementsByClassName('css-4rbku5 css-18t94o4 css-1dbjc4n r-1niwhzg r-1loqt21 r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu')")
            long_person = len(person_group)

            if scroll_flag >= 1 and long_person < 60:
                current = 5
            else:
                current = 30

            try:
                for_try = person_group[current]
                user_name = person_group[current].get_attribute('href').split('/')[-1]
                is_solvable = verification_name(user_name, 'TWITTERDM', True)

                if is_solvable:
                    already_done = True
                else:
                    url_member = f"https://twitter.com/{user_name}"
                    driver.execute_script(f"window.open('{url_member}', '_blank')")
                    #ActionChains(driver).move_to_element(person_group[current]).key_down(Keys.COMMAND).click(person_group[current]).key_up(Keys.COMMAND).perform()
                    sleep(5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
                    driver.refresh()
                    verification_name(user_name, 'TWITTERDM')

            except ElementClickInterceptedException:
                sleep(3)
                user_name = person_group[current].get_attribute('href').split('/')[-1]
                is_solvable = verification_name(user_name, 'TWITTERDM', True)

                if is_solvable:
                    already_done = True
                else:
                    url_member = f"https://twitter.com/{user_name}"
                    driver.execute_script(f"window.open('{url_member}', '_blank')")
                    #ActionChains(driver).move_to_element(person_group[current]).key_down(Keys.COMMAND).click(person_group[current]).key_up(Keys.COMMAND).perform()
                    sleep(5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
                    driver.refresh()
                    verification_name(user_name, 'TWITTERDM')

            except IndexError:
                recap_logs(mssg_success, mssg_fail, "finish", format_time, scroll_flag)
                break

        except ElementClickInterceptedException:
            try:
                user_name = person_group[current].get_attribute('href').split('/')[-1]
                is_solvable = verification_name(user_name, 'TWITTERDM', True)

                if is_solvable:
                    already_done = True
                else:
                    url_member = f"https://twitter.com/{user_name}"
                    driver.execute_script(f"window.open('{url_member}', '_blank')")
                    sleep(5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
                    driver.refresh()
                    verification_name(user_name, 'TWITTERDM')

            except JavascriptException:
                already_done = True

        except ElementNotInteractableException:
            user_name = person_group[current].get_attribute('href').split('/')[-1]
            is_solvable = verification_name(user_name, 'TWITTERDM', True)

            if is_solvable:
                already_done = True
            else:
                url_member = f"https://twitter.com/{user_name}"
                driver.execute_script(f"window.open('{url_member}', '_blank')")
                sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
                driver.refresh()
                verification_name(user_name, 'TWITTERDM')
        
        ######### Profile #########
        ###########################

        if already_done:
            mssg_fail = mssg_fail + 1

            print("")
            print(f"{Fore.LIGHTMAGENTA_EX}{format_time} : The bot has already been on this account previously !{Style.RESET_ALL}")

        else:  
            sleep(7+ time_supplement)
            try:
                driver.execute_script("""document.querySelector("[aria-label='Message']").click()""")
                sleep(3)

                try:
                    user_name_2 = driver.execute_script("""return document.querySelector("[class='css-1dbjc4n r-1awozwy r-xoduu5 r-18u37iz r-dnmrzs']").innerText""")
                except:
                    user_name_2 = False
                state = send_twitter_dm(user_name_2, format_time, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, driver, total_current_members)
                if state:
                    mssg_success = mssg_success + 1
                    signal = True
                    log_save('Twitter', format_time, current, user_name_2, url_group, scroll_flag)
                    driver.execute_script("window.history.go(-1)")
                else:
                    mssg_fail = mssg_fail + 1
                    driver.execute_script("window.history.go(-1)")

            except JavascriptException:
                try:
                    driver.execute_script("""document.querySelector("[aria-label='Message']").click()""")
                    sleep(3)
                    try:
                        user_name_2 = driver.execute_script("""return document.querySelector("[class='css-1dbjc4n r-1awozwy r-xoduu5 r-18u37iz r-dnmrzs']").innerText""")
                    except:
                        user_name_2 = False
                    state = send_twitter_dm(user_name_2, format_time, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, driver, total_current_members)
                    if state:
                        mssg_success = mssg_success + 1
                        signal = True
                        log_save('Twitter', format_time, current, user_name_2, url_group, scroll_flag)
                        driver.execute_script("window.history.go(-1)")
                    else:
                        mssg_fail = mssg_fail + 1
                        driver.execute_script("window.history.go(-1)")             

                except JavascriptException:
                    print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{total_current_members}.{Style.RESET_ALL}")
                    mssg_fail = mssg_fail + 1

            sleep(2) 
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        already_done = False
        is_solvable = False
        current = current + 1
        total_current_members = total_current_members + 1
        print(user_name)
        sleep(4+time_supplement) 


################################# EXECUTION #################################


while True:
    try:
        chrome_core(email_input, password_input, username_input)
        sleep(5+time_supplement)
        pub_iteration(first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, scroll_flag)
        break
    except WebDriverException:
        print("")
        print(f"{Fore.LIGHTYELLOW_EX}Program crash ... Restart in progress ...{Style.RESET_ALL}")
        print("")
        db_deconnexion()

db_deconnexion()
driver.close()