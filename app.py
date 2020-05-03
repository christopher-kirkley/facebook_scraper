from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options  
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import urllib.request

from random import randint

from config import USER, PASSWORD

def randsleep():
    sleeptime = randint(4,9)
    sleep(sleeptime)

class Driver:
    def __init__(self):
        options = Options()
        options.preferences.update({"javascript.enabled": False})
        self.driver = Firefox(options=options)
        self.profiles = []
        self.i = 0
    
    def login(self):
        self.driver.get('https://m.facebook.com')
        sleep(1)
        username_box = self.driver.find_element_by_name('email')
        username_box.send_keys(USER)
        sleep(1)
        password_box = self.driver.find_element_by_name('pass')
        password_box.send_keys(PASSWORD)
        sleep(1)
        login_box = self.driver.find_element_by_name('login')
        login_box.click()
        sleep(2)
        # click the OK button
        ok_button = self.driver.find_element_by_class_name('bk')
        ok_button.click()
        sleep(3)

    def save(self):
        link = self.driver.current_url
        name = self.driver.find_element_by_xpath("//div[@id='root']/div/div/div[2]/div/span/div").text
        try:
            city = self.driver.find_element_by_xpath("//span[text()='Current City']//ancestor::td/following-sibling::td").text
        except NoSuchElementException:
            city = ''
        entry = {
                'link': link,
                'name': name,
                'city': city,
                }
        self.profiles.append(entry)
        
        
    def go_to_friends_page(self):
        friends_page = self.driver.find_element_by_xpath("//div[@id='root']//a[text()='Friends']").get_attribute('href')
        self.driver.get(friends_page)

    def create_friend_list(self):
        try:
            friends = self.driver.find_element_by_xpath("//h3[contains(text(),'Friends')]/following-sibling::div")
            friend_links = friends.find_elements_by_xpath("div/table/tbody/tr/td[2]")
            friend_list = []
            for friend_link in friend_links:
                link = friend_link.find_element_by_xpath("a").get_attribute("href")
                friend_list.append(link)
            return friend_list
        except NoSuchElementException:
            return []

    def get_profile_pic(self):
        # profile_pic_link = self.driver.find_element_by_xpath("//div[@id='root']/div/div/div/a").get_attribute("href")
        profile_pic_link = self.driver.find_element_by_xpath("//div[@id='root']/div/div/div[2]/div/div/div/a").get_attribute("href")
        self.driver.get(profile_pic_link)
        sleep(1)
        pic = self.driver.find_element_by_xpath("//div[@id='root']//img").get_attribute("src")
        urllib.request.urlretrieve(pic, f"file{self.i}.jpg")

    def pick_new_friend(self, friend_list):
        number_of_friends = len(friend_list)
        friend_to_pick = randint(0, number_of_friends-1)
        friend_link = friend_list[friend_to_pick]
        self.driver.get(friend_link) 
        # check that friend is valid, if YES return link, else repeat
        sleep(3)
        return friend_link

    def check_can_access_friend_page(self, source_friend):
        try:
            randsleep()
            self.go_to_friends_page()
            return True
        except NoSuchElementException:
            return False
    
    def check_has_public_friends(self, source_friend):
        friend_list = self.create_friend_list()
        if len(friend_list) <= 1:
            return False
        else:
            return True
    
    def check_new_friend(self, source_friend):
        # make sure they are not in stored list
        pass


def main():
    print("Initializing...")
    driver = Driver()
    print("Logging in...")
    driver.login()
    source_friend = 'https://m.facebook.com/christopher.kirkley'
    randsleep()

    while True:
        print("Finding new friend.")
        driver.driver.get(source_friend)
        randsleep()
        driver.go_to_friends_page()
        friend_links = driver.create_friend_list()
        randsleep()
        driver.driver.get(source_friend)
        driver.save() # Save entry
        driver.get_profile_pic() # Get profile pic
        print(f"Addeded {driver.profiles[driver.i]}")
        randsleep()
        while True:
            source_friend = driver.pick_new_friend(friend_links)
            check_can_access_friend_page = driver.check_can_access_friend_page(source_friend)
            check_has_public_friends = driver.check_has_public_friends(source_friend)
            if check_can_access_friend_page == False or check_has_public_friends == False:
                randsleep()
                pass
            else:
                randsleep()
                driver.i += 1
                break

if __name__ == '__main__':
    main()
