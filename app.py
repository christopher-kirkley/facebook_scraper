from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options  
from time import sleep

import urllib.request

from random import randint

from config import USER, PASSWORD

def randsleep():
    sleeptime = randint(4,9)
    sleep(sleeptime)

def get_friend(source_friend):
    driver.get(source_friend)

def find_friends():
    """Go to friends page to see friends"""
    friends_page = driver.find_element_by_xpath("//div[@id='root']//a[text()='Friends']").get_attribute('href')
    driver.get(friends_page)
    sleep(2)
    friends = driver.find_element_by_xpath("//div[@id='root']/div[1]/div[2]")
    friend_links = friends.find_elements_by_xpath("div/table/tbody/tr/td[2]/a")
    friend_list = []
    for friend in friend_links:
        friend_list.append((friend.text, friend.get_attribute("href")))
    return friend_list

def check_has_public_friends(friends):
    if len(friends) == 0:
        public = Falsef
    else:
        public = True
    return public

def get_profile_pic(i):
    profile_pic_link = driver.find_element_by_xpath("//div[@id='root']/div/div/div/a").get_attribute("href")
    driver.get(profile_pic_link)
    sleep(1)
    pic = driver.find_element_by_xpath("//img[@class='img']").get_attribute("src")
    urllib.request.urlretrieve(pic, f"file{i}.jpg")

def pick_new_friend(friend_list):
    number_of_friends = len(friend_list)
    friend_to_pick = randint(4, number_of_friends-1)
    friend_link = friend_list[friend_to_pick][1]
    driver.get(friend_link) 
    sleep(3)
    return friend_link


options = Options()
options.preferences.update({"javascript.enabled": False})
driver = Firefox(executable_path = '/Users/ck/python/geckodriver/geckodriver', options=options)

driver.get('https://m.facebook.com')

sleep(1)

username_box = driver.find_element_by_name('email')
username_box.send_keys(USER)
sleep(1)
password_box = driver.find_element_by_name('pass')
password_box.send_keys(PASSWORD)
sleep(1)
login_box = driver.find_element_by_name('login')
login_box.click()

sleep(2)

# click the OK button
ok_button = driver.find_element_by_class_name('bk')
ok_button.click()

sleep(3)

# go to seed account
source_friend = 'https://m.facebook.com/rdxriazul.roy'
get_friend(source_friend)
randsleep()
i = 0

while True:
    friend_links = find_friends()
    randsleep()
    check = check_has_public_friends(friend_links)
    randsleep()
    while check == False:
        break
        randsleep()
        friend_list = find_friends()
        randsleep()
        check = check_has_public_friends(friend_links)
    get_profile_pic(i)
    randsleep()
    get_friend(source_friend)
    randsleep()
    friend_links = find_friends()
    source_friend = pick_new_friend(friend_links)
    randsleep()
    i += 1


