from selenium import webdriver

driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
def site_login(): 
	driver.get ('http://45.79.43.178/source_carts/wordpress/wp-admin/')
	driver.find_element_by_id('user_login').send_keys('admin')
	driver.find_element_by_id ('user_pass').send_keys('123456aA')
	driver.find_element_by_id('wp-submit').click()
site_login()
print("name: " + driver.find_element_by_class_name('display-name').text)

