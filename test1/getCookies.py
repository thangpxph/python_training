from selenium import webdriver
import time
def get_cookies(url,name, email, passwod):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)
    browser.find_element_by_link_text('Log in').click()
    time.sleep(2)
    browser.find_element_by_id('shop_domain').send_keys(name)
    browser.find_element_by_class_name('ui-button.ui-button--primary.ui-button--size-large').click()
    time.sleep(3)
    browser.find_element_by_id('account_email').send_keys(email)
    browser.find_element_by_class_name('ui-button.ui-button--primary.ui-button--size-large.captcha__submit').click()
    time.sleep(2)
    browser.find_element_by_id('account_password').send_keys(passwod)
    browser.find_element_by_class_name('ui-button.ui-button--primary.ui-button--size-large.captcha__submit').click()
    cookies = browser.get_cookies()
    return cookies