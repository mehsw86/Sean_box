from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

main_url = 'https://www.instagram.com/explore/tags/동물/'
image_list =[]

# 드라이버 로드
driver = wd.Chrome(executable_path='./chromedriver')

# 사이트 접속 (get)
driver.get(main_url)
driver.implicitly_wait(10)

imageItems = driver.find_elements_by_class_name('FFVAD')

for image in imageItems:
    temp = image.get_attribute('srcset').split(' ')
    image_list.append(temp[0])

# 종료
driver.close()
driver.quit()
import sys
sys.exit()


