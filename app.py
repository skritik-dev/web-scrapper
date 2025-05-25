from selenium import webdriver  # allow launching browser
from selenium.webdriver.common.by import By  # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait  # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC  # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException  # handling timeout situation
from selenium.webdriver.chrome.service import Service  # required in Selenium 4
import pandas as pd

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")  

# Step 1 : Set path to ChromeDriver
chromedriver_path = "C:/WebDrivers/chromedriver.exe"  

def create_webdriver():
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_option)

# Step 2 : Open the website & start the extraction

browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")
project_name = list()
project_url = list()

for proj in projects:
    project_name.append(proj.text.strip())
    proj_url = proj.find_element(By.TAG_NAME, "a").get_attribute("href")
    project_url.append(proj_url)
browser.quit()
project_data = {"Project Name" : project_name, "References" : project_url}

# Step 3 : Display our data

df = pd.DataFrame(project_data)
df["Username"] = df["References"].apply(lambda url: url.split("/")[3])
print(df)

# Step 4 : saving our extracted data
df.to_csv('project_data.csv')
