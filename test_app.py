import pytest

import os

os.environ['TESTDB_URI'] = 'sqlite:///test_facebook.db'

from app import Driver, engine, Session, Profiles, Base
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

testprofile_no_picture = 'https://m.facebook.com/azza.argawy.5'
testprofile_no_picture_link = 'https://www.facebook.com/birch.cooper.3'

@pytest.fixture(scope="module")
def browser():
    driver = Driver()
    driver.login()
    yield driver
    driver.driver.quit()

@pytest.fixture(scope="module")
def session():
    Base.metadata.bind = engine
    Base.metadata.create_all()
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    connection.close()


"""Tests"""

def test_can_load_user(browser):
    source = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(source)
    assert browser.driver.title == 'Christopher Kirkley'

def test_can_go_to_friends_page(browser):
    browser.go_to_friends_page()
    friends = browser.driver.find_element_by_xpath("//h3[contains(text(),'Friends')]").text
    assert 'Friends' in friends

def test_can_create_friend_list(browser):
    page = 'https://m.facebook.com/christopher.kirkley/friends'
    browser.driver.get(page)
    friend_list = browser.create_friend_list()
    assert type(friend_list) is list
    assert len(friend_list) > 100
    
def test_can_pick_new_friend(browser):
    friend_list = ['https://m.facebook.com/christopher.kirkley', 'https://m.facebook.com/coachtunde']
    new_friend = browser.pick_new_friend(friend_list)
    assert new_friend in friend_list

def test_friend_in_db_fails(browser):
    friend_list = ['https://m.facebook.com/christopher.kirkley']
    browser.driver.get('https://m.facebook.com/christopher.kirkley')
    browser.save()
    new_friend = browser.pick_new_friend(friend_list)
    assert new_friend == ''

    
    
    

def test_check_has_public_friends(browser):
    page = 'https://m.facebook.com/christopher.kirkley/friends'
    browser.driver.get(page)
    check = browser.check_has_public_friends()
    assert check == True
    page = 'https://m.facebook.com/coachtunde/friends'
    browser.driver.get(page)
    check = browser.check_has_public_friends()
    assert check == False

def test_check_can_access_friend_page(browser):
    public_friend_page = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(public_friend_page)
    check = browser.check_can_access_friend_page()
    assert check == True
    private_friend_page = 'https://m.facebook.com/profile.php?id=100035967198582'
    browser.driver.get(private_friend_page)
    check = browser.check_can_access_friend_page()
    assert check == False

def test_check_has_profile_picture(browser):
    check = browser.get_profile_pic(testprofile_no_picture)
    assert check == False

def test_check_has_profile_picture_link(browser):
    check = browser.get_profile_pic(testprofile_no_picture_link)
    assert check == False

def test_verified_friend(browser):
    friend_links = ['https://m.facebook.com/christopher.kirkley']
    source_friend = browser.find_verified_friend(friend_links)
    assert source_friend == 'https://m.facebook.com/christopher.kirkley'

def test_non_verified_friend(browser):
    friend_links = ['https://m.facebook.com/profile.php?id=100035967198582', 'https://m.facebook.com/coachtunde/friends']
    source_friend = browser.find_verified_friend(friend_links)
    assert source_friend == ''

def test_check_friend_in_db(session):
    test_profile = Profiles()
    test_profile.name = 'Tom Jones'
    test_profile.link = 'google.com'
    test_profile.city = 'New York'
    session.add(test_profile)
    session.commit()
    links = [link[0] for link in session.query(Profiles.link).all()]
    assert ('google.com' in links) == True

def test_added_to_db_and_check(browser):
    source_friend = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(page)
    browser.save()
    check = browser.check_friend_in_db(source_friend)
    assert check == True
    
    










def test_db_can_save_and_retrieve(session):
    test_profile = Profiles()
    test_profile.name = 'Tom'
    test_profile.link = 'google.com'
    test_profile.city = 'New York'
    session.add(test_profile)
    session.commit()
    result = session.query(Profiles).first()
    assert result.name == 'Tom' 
    assert result.link == 'google.com' 
    assert result.city == 'New York' 
    

def test_can_save_to_database(browser, session):
    page = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(page)
    browser.save()
    result = session.query(Profiles).first()
    assert result.name == 'Christopher Kirkley' 
    assert result.link == 'https://m.facebook.com/christopher.kirkley' 
    assert result.city == '' 
    
    





