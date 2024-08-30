from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from pynput.keyboard import Key, Controller
from selenium import webdriver

driver = webdriver.Chrome(executable_path = "C:/Users/jgala/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe")
driver.get('https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d/reprocess?ctx=rQQIARAA42KwkskoKSmw0tcvLy_XK88vyk5JrNRLzs_Vz8wrSc0pEuISOCNrZC3S8suhKazpQIixKcMqRgOQlmKontxKDF36OfnpmXm6xYm5OXoZJbk5KYcYVeONLJOMk1JSLXVTDBLNdU0MUix1Lc1TEnWNTSzMki3S0pJSjVMuMDK-YGS8xcQaDNRqtIlZxcQs2dIixcJCN9XYxETXJDXFRNfCxNIMxDI3NzRKNTI1TbnAwvODhXERK9Cpv7zYud4xH3PdtGfaApEb8QynWPUjfdONCjMC9U1ctA2d86vKki0LK1OCzLMjUwq9XYqNsyKTHMtKPUOy00ItbM2tDCew8Z5iY_jAxtjBzjCLneEAJ-MBXoYffHdf3_61b_rGdx6v-HUMHCv98qpC0jwc9SvcLYtMKrWT8zICisxT9LP8TQr9DCvcTILLnZyKXMw8bTcIMDwQYAAA0')

# jay.gala@intel.com

# Add a small delay to allow for any page load or response
time.sleep(5)

for i in [2,3,1]:
    report1 = driver.find_element_by_xpath(f'''//*[@id="tilesHolder"]/div[{i}]/div/div/div/div[2]''')
    if "jay.gala@intel.com" in report1.text:
        break

report1.click()

time.sleep(5)

driver.implicitly_wait(10)

driver.get("https://www.myworkday.com/intel/d/task/2997$6500.htmld")

time.sleep(5)


# name
text_field = driver.find_element(By.ID, "56$551056--uid12-input")
text_field.clear()
text_field.send_keys("Dev Patel")
time.sleep(1.5)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


#mobile field
job_id = driver.find_element(By.ID, "56$637284--uid20-input")
job_id.clear()
job_id.send_keys("Mob")
keyboard = Controller()
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(3)
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(2)

#country code
job_id = driver.find_element(By.ID, "56$525428--uid21-input")
job_id.clear()
job_id.send_keys("United States")
keyboard = Controller()
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(3)
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(2)

#mobile number
mobile_field = driver.find_element(By.ID, "56$525427--uid22-input")
mobile_field.clear()
mobile_field.send_keys("6035028747")
time.sleep(1)

# email
email_field = driver.find_element(By.ID, "56$259108--uid24-input")
email_field.clear()
email_field.send_keys("dev42a@gmail.com")
time.sleep(1)

# job id
job_id = driver.find_element(By.ID, "56$492757--uid27-input")
job_id.clear()
job_id.send_keys("JR0264259")
keyboard = Controller()
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

driver.maximize_window() # removes any popups from workday

# ref agreement
# referral_agreement = driver.find_element(By.ID, "56$444619--uid33-input").click()
try:
    referral_agreement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@id="56$444619--uid33"]/div'''))
    )
    driver.execute_script("arguments[0].click();", referral_agreement)
except TimeoutException:
    print("Timeout: Unable to click the referral agreement checkbox")

# referral_agreement = driver.find_element(By.XPATH, """//*[@id="56$444619--uid33-input"]""").click()


# ActionChains(driver).click(referral_agreement).perform()


# resume upload
import os
file_upload = driver.find_element_by_xpath('''//*[@id="wd-FileUploadAwesome-6$53074"]/div[2]''').click()
time.sleep(3)
keyboard = Controller()
keyboard.type("C:\\Users\\jgala\\OneDrive - Intel Corporation\\Jay personal\\autofill_referral_from_resume\\Dev-Patel-Resume-Intel.pdf")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(2)

# submit form
# submit = driver.find_element(By.CSS_SELECTOR, '''.WCUM.WGAO.WCHN.WGVM.WGUM''').click()
