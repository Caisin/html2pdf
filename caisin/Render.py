from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Render:
    def __init__(self):
        self.driver_path = "D:/software/geckodriver/chromedriver.exe"
        self.option = Options()
        self.option.add_argument('--headless')
        self.option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.option)
        self.driver.implicitly_wait(60)  # 隐性等待，最长等30秒

    def get_html(self, url):
        self.driver.get(url)
        sleep(1)
        return self.driver.page_source


    def __del__(self):
        # self.driver.quit()
        print('User 对象被回收---')


if __name__ == '__main__':
    url = "https://lingcoder.gitee.io/onjava8/#/sidebar"
    render = Render()
    print(render.get_html(url))
# driver_path = "D:/software/geckodriver/chromedriver.exe"
# url = "https://lingcoder.gitee.io/onjava8/#/sidebar"
# option = Options()
# option.add_argument('--headless')
# option.add_argument('--disable-gpu')
# driver = webdriver.Chrome(executable_path=driver_path, options=option)
# driver.implicitly_wait(60)  # 隐性等待，最长等30秒
# # 禁止加载图片
#
# driver.get(url)
# try:
#     # WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
#     # print(driver.page_source)
#     sleep(0.1)
#     print(driver.page_source)
# finally:
#     driver.close()
#     driver.quit()
