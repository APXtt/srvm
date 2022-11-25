from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def input_img():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://teachablemachine.withgoogle.com/train/image")

    # Case1 이미지 업로드
    elem = driver.find_element(By.CSS_SELECTOR, "#menu-holder")
    elem.click()

    time.sleep(30)
    driver.quit()


input_img()
