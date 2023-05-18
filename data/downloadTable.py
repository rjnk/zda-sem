# Import Library
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# setup
driver = webdriver.Firefox()
driver.get('https://statis.msmt.cz/statistikyvs/uchazecVS.aspx')
driver.maximize_window()

# bakalarske studium
driver.find_element(By.CSS_SELECTOR,'#ContentPlaceHolder1_og5_1').click()

# cleneni
Select(driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_DropDownList2a')).select_by_index(2)

for year in range(2001, 2023):
    # rok
    Select(driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_DropDownList1')).select_by_value(str(year))

    # vypis
    time.sleep(0.3)
    driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_Button1').click()

    # vytvoreni tabulky
    df = pd.read_html(driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_GridView1a"]').get_attribute('outerHTML'))[0]
    df.insert(loc=0, column='Rok', value=str(year))
    if year == 2001:
        df.to_csv('./uchazeci.csv', index=False)
    else:
        df.to_csv('./uchazeci.csv', mode='a', index=False, header=False)
