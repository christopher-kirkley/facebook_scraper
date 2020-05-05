from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options  
from selenium.common.exceptions import NoSuchElementException
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import urllib.request

from random import randint

from config import USER, PASSWORD

engine = create_engine('sqlite:///facebook.db')
Base = declarative_base()

class Profiles(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    city = Column(String(100))
    link = Column(String(300))

Base.metadata.bind = engine
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()


def randsleep():
    sleeptime = randint(7,11)
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
        new_entry = Profiles(link=link,
                            name=name,
                            city=city,
                            )
        session.add(new_entry)
        session.commit()
        
    def go_to_friends_page(self):
        friends_page = self.driver.find_element_by_xpath("//div[@id='root']//a[text()='Friends']").get_attribute('href')
        self.driver.get(friends_page)

    def add_friends_to_list(self, friend_list):
        friends = self.driver.find_element_by_xpath("//h3[contains(text(),'Friends')]/following-sibling::div")
        friend_links = friends.find_elements_by_xpath("div/table/tbody/tr/td[2]")
        for friend_link in friend_links:
            link = friend_link.find_element_by_xpath("a").get_attribute("href")
            friend_list.append(link)
        randsleep()
        if len(friend_list) < 100:
            try:
                self.driver.find_element_by_xpath("//span[text()='See More Friends']").click()
            except NoSuchElementException:
                return friend_list
            randsleep()
            return self.add_friends_to_list(friend_list)
        return friend_list

    def create_friend_list(self):
        friend_list = []
        try:
            friend_list = self.add_friends_to_list(friend_list)
            return friend_list
        except NoSuchElementException:
            return []

    def get_profile_pic(self):
        try:
            profile_pic_link = self.driver.find_element_by_xpath("//div[@id='root']/div/div/div[2]/div/div/div/a").get_attribute("href")
            self.driver.get(profile_pic_link)
            sleep(1)
            pic = self.driver.find_element_by_xpath("//div[@id='root']//img").get_attribute("src")
            urllib.request.urlretrieve(pic, f"file{self.i}.jpg")
        except NoSuchElementException:
            pass

    def check_friend_in_db(self, source_friend):
        db_friend_links = [link[0] for link in session.query(Profiles.link).all()]
        if source_friend in db_friend_links:
            return True
        else:
            return False

    def pick_new_friend(self, friend_list):
        number_of_friends = len(friend_list)
        friend_to_pick = randint(0, number_of_friends-1)
        friend_link = friend_list[friend_to_pick]
        check = self.check_friend_in_db(friend_link)
        while True:
            if check == True:
                if friend_list == []:
                    return ''
                friend_list.remove(friend_link)
                return self.pick_new_friend(friend_list)
            else:
                break
        self.driver.get(friend_link) 
        sleep(3)
        return friend_link

    def check_can_access_friend_page(self):
        try:
            randsleep()
            self.go_to_friends_page()
            return True
        except NoSuchElementException:
            return False
    
    def check_has_public_friends(self):
        friends = self.driver.find_element_by_xpath("//h3[contains(text(),'Friends')]/following-sibling::div")
        friend_links = friends.find_elements_by_xpath("div/table/tbody/tr/td[2]")
        if len(friend_links) <= 1:
            return False
        else:
            return True
    
    
    def find_verified_friend(self, friend_links):
        while True:
            source_friend = self.pick_new_friend(friend_links)
            check_can_access_friend_page = self.check_can_access_friend_page()
            if check_can_access_friend_page == True:
                check_has_public_friends = self.check_has_public_friends()
            if check_can_access_friend_page == False or check_has_public_friends == False:
                randsleep()
                friend_links.remove(source_friend)
                if friend_links == []:
                    return ''
                else:
                    pass
            else:
                randsleep()
                self.i += 1
                break
        return source_friend



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
        source_friend = driver.find_verified_friend(friend_links)

if __name__ == '__main__':
    main()
