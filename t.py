def create_friend_list():
    friends = driver.driver.find_element_by_xpath("//h3[contains(text(),'Friends')]/following-sibling::div")
    friend_links = friends.find_elements_by_xpath("div/table/tbody/tr/td[2]")
    friend_list = []
    for friend_link in friend_links:
        if 'mutual friend' in friend_link.find_element_by_xpath("div").text:
            pass
        else:
            name = friend_link.find_element_by_xpath("a").text
            link = friend_link.find_element_by_xpath("a").get_attribute("href")
            friend_list.append((name, link))
            return friend_list
    if len(friend_list) < 10:
        randsleep()
        driver.driver.find_element_by_xpath("//span[text()='See More Friends']").click()
        randsleep()
        create_friend_list()
    return friend_list

