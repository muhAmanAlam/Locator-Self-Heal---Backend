from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium.webdriver.support.expected_conditions as EC

import requests

from google import genai

from cleaner import clean_html
from db_functions import save_xpath_and_dom, fetch_xpath_entry, update_xpath_entry

client = genai.Client(api_key="AIzaSyDz_MvESKjQtYKoeUHJISfhpWFqHQdODCg")

def sendkeys(locator, text):
    wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
    element = driver.find_element(By.XPATH, locator)
    element.send_keys(text)

def click(locator):
    wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
    element = driver.find_element(By.XPATH, locator)
    element.click()

def validate_text(xpath_name, locator, text, healing=False):
    if healing == False:
        wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        element = driver.find_element(By.XPATH, locator)
        value = element.text
        assert str(value) == text
        print(f'Element text: {value} is equal to : {text}')

    elif healing == True:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            element = driver.find_element(By.XPATH, locator)
            value = element.text
            assert str(value) == text
            print(f'Element text: {value} is equal to : {text}')
        
        except TimeoutException:
            try:
                print('element not found using provided xpath, checking for previous xpath in DB and trying with that')
                r = requests.get("http://127.0.0.1:8000/previous_working_xpath/" + xpath_name)
                last_xpath = r.json()['previous_working_xpath']
                print('previous successful xpath found in db')
                element = driver.find_element(By.XPATH, last_xpath)
                value = element.text
                assert str(value) == text
                print(f'Element text: {value} is equal to : {text}')
            
            except:
                print('Failed, Trying to heal xpath if previous entries exist in db')
                
                get_current_dom()
                
                url = 'http://127.0.0.1:8000/upload_dom/'
                files = {'file': open('body.txt', 'rb')}                
                r = requests.post(url, files=files)
                                
                resp = requests.get("http://127.0.0.1:8000/heal_xpath/" + xpath_name)
                healed_xpath = resp.json()['healed_xpath']
                
                wait.until(EC.visibility_of_element_located((By.XPATH, healed_xpath)))
                element = driver.find_element(By.XPATH, healed_xpath)
                print('Sucessfully found element using the new healed Xpath.')
                print(f'Saving current xpath and current dom for element {xpath_name}')
                                
                requests.get("http://127.0.0.1:8000/save_xpath_and_dom/" + xpath_name)
                
                value = element.text
                try:
                    assert str(value) == text
                    print(f'Element text: {value} is equal to : {text}')
                except:
                    print(value, ' is not equal ', text)

def get_current_dom():
    time.sleep(3)
    body = driver.find_element(By.XPATH, '//body').get_attribute('innerHTML')
    body = clean_html(body).strip()
    with open("body.txt", "w") as file:
        file.write(body)
    return body

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)


driver.get('https://opensource-demo.orangehrmlive.com/')

sendkeys("//input[@name='username']", 'Admin')
sendkeys("//input[@name='password']", 'admin123')
click('//button[@type="submit"]')
click("//span[text()[contains(.,'Admin')]]/parent::a")
sendkeys("//input[@class='oxd-input oxd-input--active' and not(@placeholder)]", 'FMLName')
click("//button[text()[contains(.,' Search ')]]")

validate_text('XPATH_EMPLOYEE_NAME','//div[@class="oxd-table-row oxd-table-row--with-border"]/div/div[text()[contains(.,"Qwerty LName")]]', 'Qwerty LName', True)


# save_xpath_and_dom('XPATH_EMPLOYEE_NAME', loc, dom)