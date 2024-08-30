# Used to import the webdriver from selenium
from selenium_autofill import webdriver 
import os

# Get the path of chromedriver which you have install

def startBot(username, password, url):
	path = "C:/Users/jgala/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe"
	
	# giving the path of chromedriver to selenium webdriver
	driver = webdriver.Chrome()
	
	# opening the website in chrome.
	driver.get(url)
	from selenium.webdriver.support.ui import WebDriverWait
	wait = WebDriverWait(driver, 10)
	
	# find the id or name or class of
	# username by inspecting on username input
	from selenium.webdriver.common.by import By
	import time
	time.sleep(10)
	driver.find_element(
		By.CLASS_NAME, "form-control ltr_override input ext-input text-box ext-text-box").send_keys(username)
	
	# # find the password by inspecting on password input
	# driver.find_element_by_name(
	# 	"id/class/name of password").send_keys(password)
	
	# # click on submit
	# driver.find_element_by_css_selector(
	# 	"id/class/name/css selector of login button").click()


# Driver Code
# Enter below your login credentials
username = "jay.gala@intel.com"
password = "Enter your password"

# URL of the login page of site
# which you want to automate login.
# url = "https://www.myworkday.com/intel/d/task/2997$6500.htmld"
url = "https://google.com"

# Call the function
startBot(username, password, url)

# https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d/saml2