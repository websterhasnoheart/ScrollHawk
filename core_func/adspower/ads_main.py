import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

ads_id = "user_g2421o2"
open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()
http://127.0.0.1:20725/?id=j5tqp77&acc_id=1&sys_id=903529&invite_code=g2421o2&company_id=324344&is_free_company=0&batch=Ungrouped&comment=&name=--&time=2023-03-30%2021%3A26%3A23&soft=other&soft_type=http&port=50100&ip=103.80.86.201&ipc=us&ipr=il&ipy=chicago&ip_auto_proxy=country%2Cregion%2Ccity%2Casn%2ClastIp&base_url=https%3A%2F%2Fapi-global.adspower.net%2F&lang=en-US&version=v2.6.2.0&tz_auto=1&tz=America%2FChicago&geo_switch=1&tz_geo=0&browser_name=London&browser_head=1&set_cookie=1&proxyStep=undefined&failNum=0&p_url=&flow_de_page=0&longitude=-87.629882&latitude=41.878124&step=over
chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
print(driver.title)
driver.get("https://www.baidu.com")
time.sleep(5)
driver.quit()
requests.get(close_url)
