import os, random, time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from stem import Signal
from stem.control import Controller

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType, Popularity, SoftwareName


def user_agent(pops=[Popularity.COMMON.value, Popularity.AVERAGE.value, Popularity.POPULAR.value], hawd=[HardwareType.COMPUTER.value]):
    user_agent_rotator=UserAgent(hardware_types=hawd, popularity=pops, software_names=[SoftwareName.FIREFOX.value], limit=100)
    u_agent=user_agent_rotator.get_random_user_agent()
    
    # lang=re.findall(r'; ([a-z]{1,3}((\-|\_)[a-zA-Z]{1,3})?)(;|\))', u_agent)
    # if lang:
    #     if not "us" in lang[0][0].lower():
    #         u_agent=u_agent.replace("; {}".format(lang[0][0]), "")

    return u_agent

print("""
 _____ ___________                    
|_   _|  _  | ___ \                   
  | | | | | | |_/ /                   
  | | | | | |    /                    
  | | \ \_/ / |\ \                    
  \_/  \___/\_| \_|                   
                                                    
 _    _       _       _               
| |  | |     | |     | |              
| |  | | __ _| |_ ___| |__   ___ _ __ 
| |/\| |/ _` | __/ __| '_ \ / _ \ '__|
\  /\  / (_| | || (__| | | |  __/ |   
 \/  \/ \__,_|\__\___|_| |_|\___|_|   
                                      

Warning: Links file must only contain url's each in a new line.

""")

links_file=input("Path of the file containing the url's: ")
while not os.path.exists(links_file):
    links_file=input("ERROR. Path not found! Enter a valid one: ")

def error_log(err):
    with open("error_log.txt", "a") as f:
        f.write("{} - {}.\n".format(datetime.now().strftime("[%m/%d/%Y, %H:%M:%S]"), str(err)))
def sleep(start, end):
    sleep=random.randint(start,end)+float(str(random.random())[:3])
    time.sleep(sleep)
def get_links():
    with open(links_file) as f:
        links=f.read().strip().split("\n")
    for i in range(len(links)):
        links[i]=links[i].strip()

    return links
def update_file(links_array):
    with open(links_file, "w") as f:
        f.write("\n".join(links_array))
def start_browser():
    profile=webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent())
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", '127.0.0.1')
    profile.set_preference("network.proxy.socks_port", 9150)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    return webdriver.Firefox(firefox_profile=profile)#, executable_path="geckodriver")
def interactions(br):
    try:
        elem=br.find_element_by_tag_name("body")
    except:
        try:
            elem=br.find_element_by_tag_name("html")
        except Exception as e:
            error_log(e)

    sleep(2,10)

    for i in range(random.randint(2,8)):
        elem.sendKeys(Keys.PAGE_DOWN)
        sleep(0,1)
    
    sleep(2,5)

    for i in range(random.randint(1,3)):
        br.sendKeys(Keys.PAGE_UP)
        sleep(0,1)

    sleep(10,25)

    for i in range(random.randint(1,3)):
        br.sendKeys(Keys.PAGE_UP)
        sleep(0,1)


def get_ip(br):
    br.get("https://api.ipify.org/?format=txt")
    ip=(br.find_element_by_tag_name("html").text).strip()

    return ip

def change_ip(br, old_ip):
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    time.sleep(2)

    #print("waiting for the new ip...")
    
    cnt=0
    current_ip=""
    while old_ip==current_ip:
        current_ip=get_ip(br)
        time.sleep(3)

        if cnt==5:
            break
        cnt+=1
    
    if old_ip==current_ip:
        error_log("something is wrong with tor!")
        print("something is wrong with tor!")

        br.quit()
        exit()

links=get_links()
links_save=links

browser=start_browser()
for link in links:
    ip=get_ip(browser)

    browser.get(link)
    time.sleep(5)

    interactions(browser)

browser.quit()

