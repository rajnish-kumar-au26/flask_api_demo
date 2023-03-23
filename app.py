from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import gspread
# import sys, subprocess
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gspread'])
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.headless = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

app = Flask(__name__)


@app.route('/scrape')
def scrape():
    username = "sankum@gmail.com"
    password = "navyug@123"
    driver.get('https://app.salesrobot.co/login')

    driver.find_element(By.XPATH, "//*[@id='email']").send_keys(username)
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys(password)
    # login = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='sign-in-button']")))
    # login.click()
    # dashboard = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='root']/div/div[1]/div[2]/nav/ul/li[2]/ul/li[1]/span/div/div/a")))
    # dashboard.click()
    driver.find_element(By.XPATH,"//div[@class='sign-in-button']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[1]/div[2]/nav/ul/li[2]/ul/li[1]/span/div/div/a").click()
    
    time.sleep(5)

    total_campaigns = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div/div[1]").text

    total_campaigns_number = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div/div[2]/span/span").text

    running_campaigns = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[3]/div/div[1]").text

    running_campaigns_number = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[3]/div/div[2]/span/span").text

    total_connected = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]").text

    total_connected_number = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/span/span").text

    linkedin_replies = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[3]/div/div/div/div[2]/div/div[1]").text

    linkedin_replies_number = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[3]/div/div/div/div[2]/div/div[2]/span/span").text

    email_replies = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[4]/div/div/div/div[2]/div/div[1]").text

    email_replies_number = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[4]/div/div/div/div[2]/div/div[2]/span/span").text

    data = {
        total_campaigns: total_campaigns_number, running_campaigns: running_campaigns_number, total_connected: total_connected_number, linkedin_replies: linkedin_replies_number, email_replies: email_replies_number
    }

 

    sa = gspread.service_account(filename="./credentials.json")

    sh = sa.open("sales_data")

    sheet = sh.worksheet("Sheet1")
    sheet.update('A1:E2', [[total_campaigns, running_campaigns, total_connected, linkedin_replies,  email_replies], [
                 total_campaigns_number, running_campaigns_number, total_connected_number, linkedin_replies_number, email_replies_number]])
       # Close the driver
    driver.quit()
    # Return the  JSON
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(debug=True)
