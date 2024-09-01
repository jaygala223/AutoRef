from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from pynput.keyboard import Key, Controller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread


def fill_workday_form_using_selenium(referrer_email:str, name:str, email:str, country_name:str, phone_number:str, job_req_id:str, resume_path, form_link:str, chrome_driver_path="", headless:bool=False):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(executable_path = chrome_driver_path, chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path = "C:/Users/jgala/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe", chrome_options=chrome_options)
    
    # driver.get('https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d/reprocess?ctx=rQQIARAA42KwkskoKSmw0tcvLy_XK88vyk5JrNRLzs_Vz8wrSc0pEuISOCNrZC3S8suhKazpQIixKcMqRgOQlmKontxKDF36OfnpmXm6xYm5OXoZJbk5KYcYVeONLJOMk1JSLXVTDBLNdU0MUix1Lc1TEnWNTSzMki3S0pJSjVMuMDK-YGS8xcQaDNRqtIlZxcQs2dIixcJCN9XYxETXJDXFRNfCxNIMxDI3NzRKNTI1TbnAwvODhXERK9Cpv7zYud4xH3PdtGfaApEb8QynWPUjfdONCjMC9U1ctA2d86vKki0LK1OCzLMjUwq9XYqNsyKTHMtKPUOy00ItbM2tDCew8Z5iY_jAxtjBzjCLneEAJ-MBXoYffHdf3_61b_rGdx6v-HUMHCv98qpC0jwc9SvcLYtMKrWT8zICisxT9LP8TQr9DCvcTILLnZyKXMw8bTcIMDwQYAAA0')

    driver.get(form_link)

    time.sleep(5)

    for i in [2,3,1]:
        report1 = driver.find_element_by_xpath(f'''//*[@id="tilesHolder"]/div[{i}]/div/div/div/div[2]''')
        if referrer_email in report1.text:
            break

    report1.click()

    time.sleep(5)

    driver.implicitly_wait(10)

    driver.get("https://www.myworkday.com/intel/d/task/2997$6500.htmld")

    time.sleep(5)


    # name
    text_field = driver.find_element(By.ID, "56$551056--uid12-input")
    text_field.clear()
    text_field.send_keys(name)
    time.sleep(1.5)

    #mobile field
    mobile_type = driver.find_element(By.ID, "56$637284--uid20-input")
    mobile_type.clear()
    mobile_type.send_keys("Mobile")
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(3)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(2)

    #country code
    country = driver.find_element(By.ID, "56$525428--uid21-input")
    country.clear()
    country.send_keys(country_name)
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
    mobile_field.send_keys(phone_number)
    time.sleep(1)

    # email
    email_field = driver.find_element(By.ID, "56$259108--uid24-input")
    email_field.clear()
    email_field.send_keys(email)
    time.sleep(1)

    # job id
    job_id = driver.find_element(By.ID, "56$492757--uid27-input")
    job_id.clear()
    job_id.send_keys(job_req_id)
    time.sleep(3)
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
    keyboard.type(str(resume_path))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(5) # wait for resume to be uploaded

    # submit form
    # submit = driver.find_element(By.CSS_SELECTOR, '''.WCUM.WGAO.WCHN.WGVM.WGUM''').click()
    # time.sleep(100)
    driver.close()

def run_in_thread(referrer_email, name, email, country_name, phone_number, job_req_id, resume_path):
    thread = Thread(target=fill_workday_form_using_selenium, args=(referrer_email, name, email, country_name, phone_number, job_req_id, resume_path))
    thread.start()

# if __name__ == "__main__":
#     fill_form_using_selenium("jay gala", "jaygala260@gmail.com", "india", "9004942831", "JR0264259", "C:\\Users\\jgala\\OneDrive - Intel Corporation\\Jay personal\\autofill_referral_from_resume\\Dev-Patel-Resume-Intel.pdf")