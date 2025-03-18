from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

chrome_driver_path = r"D:\ApexaiQ\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://en.wikipedia.org/wiki/Java_version_history")

time.sleep(3)
table = driver.find_element(By.XPATH, "//table[contains(@class,'wikitable')]")
rows = table.find_elements(By.TAG_NAME, "tr")

table_data = []

for row in rows:
    
    headers = row.find_elements(By.TAG_NAME, "th")
    if headers:  
        row_data = [col.text.strip() for col in headers]
        table_data.append(row_data)
        continue  
    
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text.strip() for col in cols]
    
    if row_data:
        table_data.append(row_data)
        
df = pd.DataFrame(table_data)

df.to_csv("./extracted/Java_versions.csv",index=False)


print('Tables extracted successfully')
driver.quit()
