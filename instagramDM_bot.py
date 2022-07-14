import datetime
from datetime import timedelta
from time import sleep
from getpass import getpass

from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from functions import *


selem_("KLDZ")

print("")
print(f"{Fore.LIGHTYELLOW_EX}Program start ... ")
print("")
print("")


#################################### INITIALIZATION ##########################################


print(f"{Fore.LIGHTMAGENTA_EX}Please enter an Instagram account")
print("")

email_input = input(f"{Fore.LIGHTCYAN_EX}Instagram account name (email) : ")
password_input = getpass(f"Instagram password (hidden) : ")
print("")


url_group =  input(f"{Fore.LIGHTCYAN_EX}Please enter group URL : ")
print("")

print(f"{Fore.LIGHTMAGENTA_EX}Do you want to load the texts used during your last use?")
doyouload = input(f"If yes press Y otherwise enter any other key : {Style.RESET_ALL}")
print("")

if doyouload.lower() == "y":
    try:
        fichier = open("data/save_instaDM.txt", "r")
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
    fichier_save = open("data/save_instaDM.txt", "w")

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


########################################### SETTINGS ############################################
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

current = 0
mssg_success = 0
mssg_fail = 0

wait_values = [300, 250, 280, 295, 320, 330, 350, 210, 310, 200]
big_wait_values = [200, 250, 130, 220, 210, 200, 205]
time_supplement = 5
#################################################################################################


def instagram_dm_chrome_core(email_input, password_input):
    " Launching the page and navigating to groups "

    global driver

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options) 
    driver.get("https://www.instagram.com/")

    print("")
    print(f"{Fore.LIGHTGREEN_EX}Parameters : OK. {Style.RESET_ALL}")
    print("")
    print(f"{Fore.LIGHTYELLOW_EX}Connexion to Instagram : In progress ... {Style.RESET_ALL}")

    sleep(5+time_supplement)

    driver.execute_script("document.getElementsByClassName('aOOlW bIiDR')[0].click()")
    sleep(3+time_supplement)

    #driver.execute_script("""document.getElementsByClassName("sqdOP")[1].click()""")
    #sleep(2+time_supplement)

    email = driver.find_element(by=By.NAME, value="username")
    mdp = driver.find_element(by=By.NAME, value="password")
    email.send_keys(email_input)
    mdp.send_keys(password_input)

    sleep(2+time_supplement)
    driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']").click()

    print("")
    print(f"{Fore.LIGHTGREEN_EX}Connexion to Instagram : OK. {Style.RESET_ALL}")

    db_connection()

    sleep(5+time_supplement)
    driver.get(url_group)
    sleep(6+time_supplement)

    try:
        driver.execute_script("document.getElementsByClassName('_ac2a')[1].click()")
    except JavascriptException:
        print("")
        print(f"{Fore.LIGHTRED_EX}Unable to display member list. Try Again ..{Style.RESET_ALL}")

    sleep(5+time_supplement)


def pub_iteration(first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, scroll_flag):
    """ Function calling itself allowing to enter
    and post in the different groups of the list """

    global current, mssg_success, mssg_fail

    if scroll_flag > 0:
        for x in range(1, scroll_flag):
            driver.execute_script("""document.getElementsByClassName('_aano')[0].scrollTo(0,document.getElementsByClassName('_aano')[0].scrollHeight)""")
            sleep(5+time_supplement)

    while True:
        already_done = False
        date_time = datetime.datetime.now() + timedelta(hours=2)
        format_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

        person_group = driver.execute_script(f"""return document.getElementsByClassName("_aacl _aaco _aacw _aacx _aad7 _aade")""")
        long_person = len(person_group)

        print("")
        print("Member number on the current scroll list : " + str(current))
        print("Total number of loaded members : " + str(long_person))
        print("Scroll flag n° : " + str(scroll_flag))

        ######## followers list ########
        ################################

        try:
            for_try = person_group[current]
            username = person_group[current].text

            is_solvable = verification_name(username, 'INSTAGRAMDM', True)

            if is_solvable:
                already_done = True
            else:
                driver.execute_script("window.open('https://www.instagram.com/direct/new/','_blank');")
                sleep(3)
                driver.switch_to.window(driver.window_handles[1])

                verification_name(username, 'INSTAGRAMDM')

        ######## Scroll for loading the member list ########
        ####################################################

        except IndexError:
            scroll_flag = scroll_flag + 2 

            for x in range(1, scroll_flag):
                driver.execute_script("""document.getElementsByClassName('_aano')[0].scrollTo(0,document.getElementsByClassName('_aano')[0].scrollHeight)""")
                sleep(5+time_supplement)

            sleep(3+time_supplement)
            person_group = driver.execute_script(f"""return document.getElementsByClassName("_aacl _aaco _aacw _aacx _aad7 _aade")""")
            long_person = len(person_group)
            sleep(2+time_supplement)

            try:
                for_try = person_group[current]
                username = person_group[current].text

                is_solvable = verification_name(username, 'INSTAGRAMDM', True)

                if is_solvable:
                    already_done = True
                else:
                    driver.execute_script("window.open('https://www.instagram.com/direct/new/','_blank');")
                    sleep(3)
                    driver.switch_to.window(driver.window_handles[1])

                    verification_name(username, 'INSTAGRAMDM')

            # End of program
            except IndexError:
                recap_logs(mssg_success, mssg_fail, 'finish', format_time, scroll_flag)
                break

            except ElementClickInterceptedException:
                sleep(2+time_supplement)
                username = driver.execute_script(f"return document.getElementsByClassName('_aacl _aaco _aacw _aacx _aad7 _aade')[{current + 1}].textContent")
                is_solvable = verification_name(username, 'INSTAGRAMDM', True)

                if is_solvable:
                    already_done = True
                else:
                    driver.execute_script("window.open('https://www.instagram.com/direct/new/','_blank');")
                    sleep(3)
                    driver.switch_to.window(driver.window_handles[1])

                    verification_name(username, 'INSTAGRAMDM')

        print(f"@{username}")
        print("")

        ######### CONTACT #########
        ###########################
         
        if already_done:
            mssg_fail = mssg_fail + 1
            print("")
            print(f"{Fore.LIGHTMAGENTA_EX}{format_time} : The bot has already been on this account previously !{Style.RESET_ALL}")

        else:
            sleep(4+time_supplement)
            try:
                input_research = driver.find_element(by=By.NAME, value="queryBox")
                input_research.send_keys(username)

                sleep(6)

                driver.execute_script("document.getElementsByClassName('_abl-')[3].click()")
                sleep(3)
                driver.execute_script("document.getElementsByClassName('_acan _acao _acas _acav')[0].click()")

                sleep(5+time_supplement)

                state = send_instagram_dm(current, username, format_time, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, driver)
                if state:
                    mssg_success = mssg_success + 1
                    log_save('Instagram', format_time, current, username, url_group, scroll_flag)
                else:
                    mssg_fail = mssg_fail + 1

            except:
                print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{current + 1}.{Style.RESET_ALL}")

            sleep(4)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            sleep(8+time_supplement)
        
        current = current + 1


################################# EXECUTION #################################


while True:
    try:
        instagram_dm_chrome_core(email_input, password_input)
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