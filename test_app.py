import pytest

from app import Driver, engine, Session, Profiles
from time import sleep


@pytest.fixture(scope="module")
def browser():
    driver = Driver()
    driver.login()
    yield driver
    driver.driver.quit()

@pytest.fixture(scope="module")
def connection():
    connection = engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def db_session(connection):
    transaction = connection.begin()
    db_session = Session(bind=connection)
    yield db_session
    db_session.close()
    transaction.rollback()

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
    friend_list = browser.create_friend_list()
    new_friend = browser.pick_new_friend(friend_list)
    assert new_friend in friend_list

def test_check_has_public_friends(browser):
    page = 'https://m.facebook.com/christopher.kirkley/friends'
    browser.driver.get(page)
    check = browser.check_has_public_friends()
    assert check == True
    page = 'https://m.facebook.com/coachtunde/friends'
    browser.driver.get(page)
    check = browser.check_has_public_friends()
    assert check == False

def test_can_access_friend_page(browser):
    page = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(page)
    check = browser.check_can_access_friend_page()
    assert check == True
    page = 'https://m.facebook.com/coachtunde/'
    browser.driver.get(page)
    check = browser.check_can_access_friend_page()
    assert check == False

def test_db_can_save_and_retrieve(db_session):
    test_profile = Profiles()
    test_profile.name = 'Tom'
    test_profile.link = 'google.com'
    test_profile.city = 'New York'
    db_session.add(test_profile)
    db_session.commit()
    result = db_session.query(Profiles).first()
    assert result.name == 'Tom' 
    assert result.link == 'google.com' 
    assert result.city == 'New York' 
    

def test_can_save_to_database(browser, db_session):
    page = 'https://m.facebook.com/christopher.kirkley'
    browser.driver.get(page)
    browser.save()
    result = db_session.query(Profiles).first()
    assert result.name == 'Christopher Kirkley' 
    assert result.link == 'https://m.facebook.com/christopher.kirkley' 
    assert result.city == '' 
    
    





