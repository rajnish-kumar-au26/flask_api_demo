from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import gspread




app = Flask(__name__)


@app.route('/scrape')
def scrape():
    chrome_path = "chromedriver"
    chrome_binary = "/usr/bin/google-chrome"
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromedriver"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    service= Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)
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
    
    time.sleep(10)

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

    table_data = driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div/div/table/thead/tr/th")
    all_data = []
    
    heading = []
    for title in table_data:
        heading.append(title.text)
    all_data.append(heading)
    
    # print(table_data.text)
    table_body_data = driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div/div/table/tbody/tr")
    
    
    for data in table_body_data:
        get_data = []
        d = data.find_elements(By.XPATH,"./td")
        for value in d:
            get_data.append(value.text)
        all_data.append(get_data)
        
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y %I:%M:%S %p")
    

    all_data.append([total_campaigns, running_campaigns, total_connected, linkedin_replies,  email_replies,"Date"])
    all_data.append([
                 total_campaigns_number, running_campaigns_number, total_connected_number, linkedin_replies_number, email_replies_number,today])
    # print(all_data)
   
    
    
    
    sa = gspread.service_account(filename="./credentials.json")

    sh = sa.open("sales_data")

    sheet = sh.worksheet("Sheet1")
    # sheet.update('A1:I13', [[total_campaigns, running_campaigns, total_connected, linkedin_replies,  email_replies], [
    #              total_campaigns_number, running_campaigns_number, total_connected_number, linkedin_replies_number, email_replies_number]])
    
    # sheet.update('A1:I14',all_data)
    
    
    sheet.append_row(all_data[0])
    sheet.append_row(all_data[1])
    sheet.append_row(all_data[2])
    sheet.append_row(all_data[3])
    sheet.append_row(all_data[4])
    sheet.append_row(all_data[5])
    sheet.append_row(all_data[6])
    sheet.append_row(all_data[7])
    sheet.append_row(all_data[8])
    sheet.append_row(all_data[9])
    sheet.append_row(all_data[10])
    sheet.append_row(all_data[11])
    sheet.append_row(all_data[12])
    sheet.append_row(all_data[13])
    
    #    Close the driver
    driver.quit()
    # Return the  JSON
    return jsonify(all_data)


if __name__ == '__main__':
    app.run(debug=True)
