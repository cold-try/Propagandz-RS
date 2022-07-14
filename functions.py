from random import shuffle
from time import sleep
from colorama import Fore, Style
from selenium.common.exceptions import NoSuchElementException, WebDriverException, JavascriptException
from selenium.webdriver.common.by import By
import psycopg2


time_supplement = 2
wait_values = [100, 40, 70, 20, 30, 60, 55, 80, 90, 40]
conn = None
cur = None


def db_connection():
    global conn, cur
    conn = psycopg2.connect('##### YOUR DB #####', sslmode='require')
    cur = conn.cursor()
    print('')
    print(f"{Fore.LIGHTGREEN_EX}Database connection successful.{Style.RESET_ALL}")
    print('')


def db_deconnexion():
    global conn, cur
    cur.close()
    conn.close()


def send_twitter_dm(name, format_time, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, driver, total_current_members):
    sleep(8+time_supplement)

    ready_to_send = mssg_format(name, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg)
    verif_doublon = driver.execute_script("""return document.querySelectorAll("[class='css-1dbjc4n r-obd0qt r-1wbh5a2']")""")

    if not verif_doublon:
        if len(verif_doublon) == 0:
            try:
                driver.execute_script("""document.getElementsByClassName("DraftEditor-root")[0].click()""")
                sleep(1)
                span_msg = driver.find_element(by=By.CSS_SELECTOR, value='[data-text="true"]')

                try:
                    span_msg.send_keys(ready_to_send)
                except WebDriverException:
                    # Special characters not supported
                    span_msg.send_keys(mssg_format(False, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg))

                sleep(3+time_supplement)
                driver.execute_script("""document.querySelector("[aria-label='Send']").click()""")

                print(f"{Fore.LIGHTGREEN_EX}{format_time} : Message n°{total_current_members} sent.{Style.RESET_ALL}")
                shuffle(wait_values)
                sleep(wait_values[0])
                return True

            except JavascriptException:
                try: 
                    driver.execute_script("""document.querySelector("[aria-label='Envoyer']").click()""")
                    print(f"{Fore.LIGHTGREEN_EX}{format_time} : Message n°{total_current_members} sent.{Style.RESET_ALL}")
                    shuffle(wait_values)
                    sleep(wait_values[0])
                    return True

                except NoSuchElementException:
                    print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{total_current_members}.{Style.RESET_ALL}")
                    return False
        else:
            print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{total_current_members}, a message has already been sent.{Style.RESET_ALL}")
            return False

    else:
        print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{total_current_members}, a message has already been sent.{Style.RESET_ALL}")
        return False


def send_instagram_dm(current, name, format_time, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg, driver):
    username = name.split()
    ready_to_send = mssg_format(username[0], first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg)

    sleep(5)

    try:
        text_area = driver.find_elements_by_tag_name("textArea")[0]
        text_area.send_keys(ready_to_send)

        sleep(5)

        input_research = driver.execute_script("""return document.getElementsByClassName('_acan _acao _acas')""")
        index_button_send = len(input_research)-1

        sleep(1)
        
        driver.execute_script(f"document.getElementsByClassName('_acan _acao _acas')[{index_button_send}].click()")

        print(f"{Fore.LIGHTGREEN_EX}{format_time} : Message n°{current} sent.{Style.RESET_ALL}")

        shuffle(wait_values)
        sleep(wait_values[0])
        return True

    except NoSuchElementException:
        print(f"{Fore.LIGHTRED_EX}{format_time} : Unable to send message n°{current}.{Style.RESET_ALL}")
        return False


def log_save(mode, format_time, current, name, url, scroll_flag):
    if mode == 'Twitter':
        with open('data/twitter_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n {format_time} : Message n°{current} sent to {name}')
            f.write(f'\n List URL : {url} // Scroll Flag n°{scroll_flag}')
            f.write(f'\n')

    if mode == 'Instagram':
        with open('data/instagram_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n {format_time} : Message n°{current} sent to {name}')
            f.write(f'\n List URL : {url} // Scroll Flag n°{scroll_flag}')
            f.write(f'\n')
    
    elif mode == 'Facebook':
        with open('data/facebook_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n {format_time} : Message n°{current} sent to {name}')
            f.write(f'\n List URL : {url} // Scroll Flag n°{scroll_flag}')
            f.write(f'\n')

    elif mode == 'facebookGroups':
        with open('data/fcbkgroup_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n {format_time} : Message n°{current} sent to {name}')
            f.write(f'\n List URL : {url} // Scroll Flag n°{scroll_flag}')
            f.write(f'\n')


def mssg_format(name, first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg):
    " Draw of the message to be sent + formatting "

    messages_possibilities = [first_mssg, second_mssg, third_mssg, fourth_mssg, five_mssg]
    #salutations_possibilities = [salutation_first, salutation_second, salutation_third, salutation_fourth]
    shuffle(messages_possibilities)
    #shuffle(salutations_possibilities)
    if name:
        selectionned = messages_possibilities[0].replace("[RECEPTIVE]", name)
        #selectionned = selectionned.replace("[SALUTATION]", salutations_possibilities[0])
    else:
        selectionned = messages_possibilities[0].replace("[RECEPTIVE]", "")
        #selectionned = selectionned.replace("[SALUTATION]", salutations_possibilities[0])

    return selectionned


def recap_logs(success, fails, etat, format_time, scroll_flag):
    if etat == "finish":
        print("")
        print(f"{Fore.LIGHTYELLOW_EX}{format_time} : Program completed !{Style.RESET_ALL}")
        print("")
        print(f"{Fore.LIGHTGREEN_EX}Sent message : {success}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTRED_EX}Messages not sent : {fails}{Style.RESET_ALL}")
        print("")
    elif etat == "actif":
        print("")
        print(f"{Fore.LIGHTGREEN_EX}Sent message : {success}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTRED_EX}Messages not sent : {fails}{Style.RESET_ALL}")
        print("")
    else:
        print("")
        print(f"{Fore.LIGHTYELLOW_EX}{format_time} : Daily message limit reached !")
        print(f"{Fore.LIGHTYELLOW_EX}Relaunch your program in 24 hours from the scroll flag n°{Style.RESET_ALL}{scroll_flag}")
        print("")
        print(f"{Fore.LIGHTGREEN_EX}Sent message : {success}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTRED_EX}Messages not sent : {fails}{Style.RESET_ALL}")
        print("")


def verification_name(name, rs, verif=False):
    " Checking the presence of the target username in the db "

    sql_add_name = f"INSERT INTO {rs} VALUES ('{name}');"
    sql_get_names = f"SELECT NAME FROM {rs};"
    same = False

    if not verif:
        cur.execute(sql_add_name)
        conn.commit()
    else:
        cur.execute(sql_get_names)
        follower_list = cur.fetchall()

        for follower_name in follower_list:
            if follower_name[0] == name:
                same=True
    return same


def selem_(signature):
    " Display of logo and signature "

    l = 20
    h = 11
    t = signature
    carac = [
        " .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. ",
        "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |",
        "| |      __      | || |   ______     | || |     ______   | || |  ________    | || |  _________   | || |  _________   | || |    ______    | || |  ____  ____  | || |     _____    | || |     _____    | || |  ___  ____   | || |   _____      | || | ____    ____ | || | ____  _____  | || |     ____     | || |   ______     | || |    ___       | || |  _______     | || |    _______   | || |  _________   | || | _____  _____ | || | ____   ____  | || | _____  _____ | || |  ____  ____  | || |  ____  ____  | || |   ________   | || |    ______    | |",
        "| |     /  \     | || |  |_   _ \    | || |   .' ___  |  | || | |_   ___ `.  | || | |_   ___  |  | || | |_   ___  |  | || |  .' ___  |   | || | |_   ||   _| | || |    |_   _|   | || |    |_   _|   | || | |_  ||_  _|  | || |  |_   _|     | || ||_   \  /   _|| || ||_   \|_   _| | || |   .'    `.   | || |  |_   __ \   | || |  .'   '.     | || | |_   __ \    | || |   /  ___  |  | || | |  _   _  |  | || ||_   _||_   _|| || ||_  _| |_  _| | || ||_   _||_   _|| || | |_  _||_  _| | || | |_  _||_  _| | || |  |  __   _|  | || |   / _ __ `.  | |",
        "| |    / /\ \    | || |    | |_) |   | || |  / .'   \_|  | || |   | |   `. \ | || |   | |_  \_|  | || |   | |_  \_|  | || | / .'   \_|   | || |   | |__| |   | || |      | |     | || |      | |     | || |   | |_/ /    | || |    | |       | || |  |   \/   |  | || |  |   \ | |   | || |  /  .--.  \  | || |    | |__) |  | || | /  .-.  \    | || |   | |__) |   | || |  |  (__ \_|  | || | |_/ | | \_|  | || |  | |    | |  | || |  \ \   / /   | || |  | | /\ | |  | || |   \ \  / /   | || |   \ \  / /   | || |  |_/  / /    | || |  |_/____) |  | |",
        "| |   / ____ \   | || |    |  __'.   | || |  | |         | || |   | |    | | | || |   |  _|  _   | || |   |  _|      | || | | |    ____  | || |   |  __  |   | || |      | |     | || |   _  | |     | || |   |  __'.    | || |    | |   _   | || |  | |\  /| |  | || |  | |\ \| |   | || |  | |    | |  | || |    |  ___/   | || | | |   | |    | || |   |  __ /    | || |   '.___`-.   | || |     | |      | || |  | '    ' |  | || |   \ \ / /    | || |  | |/  \| |  | || |    > `' <    | || |    \ \/ /    | || |     .'.' _   | || |    /  ___.'  | |",
        "| | _/ /    \ \_ | || |   _| |__) |  | || |  \ `.___.'\  | || |  _| |___.' / | || |  _| |___/ |  | || |  _| |_       | || | \ `.___]  _| | || |  _| |  | |_  | || |     _| |_    | || |  | |_' |     | || |  _| |  \ \_  | || |   _| |__/ |  | || | _| |_\/_| |_ | || | _| |_\   |_  | || |  \  `--'  /  | || |   _| |_      | || | \  `-'  \_   | || |  _| |  \ \_  | || |  |`\____) |  | || |    _| |_     | || |   \ `--' /   | || |    \ ' /     | || |  |   /\   |  | || |  _/ /'`\ \_  | || |    _|  |_    | || |   _/ /__/ |  | || |    |_|       | |",
        "| ||____|  |____|| || |  |_______/   | || |   `._____.'  | || | |________.'  | || | |_________|  | || | |_____|      | || |  `._____.'   | || | |____||____| | || |    |_____|   | || |  `.___.'     | || | |____||____| | || |  |________|  | || ||_____||_____|| || ||_____|\____| | || |   `.____.'   | || |  |_____|     | || |  `.___.\__|  | || | |____| |___| | || |  |_______.'  | || |   |_____|    | || |    `.__.'    | || |     \_/      | || |  |__/  \__|  | || | |____||____| | || |   |______|   | || |  |________|  | || |    (_)       | |",
        "| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |",
        "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |",
        " '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' "
    ]
    print('')
    print('')
    for x in range(h):
        row = carac[x]
        res='' 
        for i in range(len(t)):
            if t[i].isalpha():
                cursor = ord(t[i])-65
                res+=row[cursor*l:cursor*l+l]
            else:
                res+=row[len(row)-l:len(row)]
        print(res)
    print('@uthor : Rachid.A - Twitter : @blank_cold')