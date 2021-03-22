import getCookies
import requests


url_ = 'https://shopify.com'
URL = 'https://thang123321.myshopify.com'
shopname = 'thang123321'
user = 'phamthang2508@gmail.com'
password = '123456aA@!'

cookies = getCookies.get_cookies(url_, shopname, user, password)

jar = requests.cookies.RequestsCookieJar()
for cookie in cookies:
    jar.set(cookie['name'], cookie['value'], domain = cookie['domain'], path = cookie['path'])
#get_du_lieu
url_api = "https://thang123321.myshopify.com/admin/products.json"
data = requests.get(url_api, headers = {'Content-type': 'application/json'}, cookies = jar).json()

print(data)