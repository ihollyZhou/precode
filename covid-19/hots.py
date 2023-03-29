from selenium.webdriver import Chrome, ChromeOptions
import time


url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'

brower = Chrome()
# brower = Chrome()
brower.get(url)


time.sleep(1)  # 爬虫与反爬，模拟人等待1秒
c = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')
for i in c:
    print(i.text)