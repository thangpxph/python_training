import requests
from bs4 import BeautifulSoup

wp_login = 'http://45.79.43.178/source_carts/wordpress/wp-login.php'
wp_admin = 'http://45.79.43.178/source_carts/wordpress/wp-admin/'
username = 'admin'
password = '123456aA'

with requests.Session() as s:
    datas={'log':username, 'pwd':password}
    s.post(wp_login, data=datas)
    resp = s.get(wp_admin)
    soup = BeautifulSoup(resp.text, 'html.parser')
print("name: " + soup.find(class_='display-name').text)