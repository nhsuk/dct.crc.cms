# How to register 100 fake users with Paragon
# This would all be much simpler with a devcontainer

# install requirements.txt

# on WSL2/Ubuntu):
#   download Chrome (Ubuntu) wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#   install Chrome sudo apt install ./google-chrome-stable_current_amd64.deb

# on Mac:
#   install regular Chrome from the Chrome download page
#   install wget if necessary with brew install wget (install brew if necessary...)

# download Chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# into a subfolder ./drivers of this folder - chromedriver version must match Chrome version

# on Mac, ensure chromedriver is executable:
#   xattr -d com.apple.quarantine ./drivers/chromedriver

# capture server log output when running this program against a local host in debug mode
# massage log into wget calls for each link and save as script
# execute the script
# massage log into list of the new emails

# as needs be, kill stray Chromes with sudo pkill -9 chrome
# (beware, Electron apps like Teams use Chrome under the hood)

import time
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start a headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options=chrome_options)

def registerAUser ():
    # Fetch CRCV3 home page
    driver.get ("http://localhost:8000/signup")
    current_url = driver.current_url

    #print (driver.title)
    email = "%s@gov.uk" % (uuid4 (),)
    print ("Registering email", email)
    form = driver.find_element_by_id ("signin")
    cookie = driver.find_element_by_name ("csrfmiddlewaretoken").get_attribute ("value")
    #print ("CSRF cookie", cookie)
    driver.execute_script ('document.getElementById("id_first_name").value="John";')
    driver.execute_script ('document.getElementById("id_last_name").value="Smith";')
    driver.execute_script ('document.getElementById("id_postcode").value="W1A 2AA";')
    driver.execute_script ('document.getElementById("id_organisation").value="The Organisation";')
    driver.execute_script ('document.getElementById("id_job_title").value="health";')
    driver.execute_script ('document.getElementById("id_email").value="%s";' % email)
    driver.execute_script ('document.getElementById("id_password").value="Passw0rd??";')
    driver.execute_script ('document.getElementById("id_terms").click ();')
    driver.execute_script ('document.getElementsByTagName("button") [2].click ();')

    #print ("Sent fields")

    # wait for URL to change with 15 seconds timeout
    #time.sleep (10)
    #print (driver.title)

    WebDriverWait(driver, 15).until(EC.title_contains("Password Set"))

    if driver.title.strip () != "Password Set | Campaign Resource Centre":
        print ("Not redirected to confirmation page, instead", driver.title)
    else:
        print (email, "registered")

for i in range(100): registerAUser ()

#driver.quit ()
driver.close ()
