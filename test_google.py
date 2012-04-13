from selenium import webdriver
from nose.tools import with_setup

_multiprocess_can_split_ = True

driver = None

ie = webdriver.DesiredCapabilities.INTERNETEXPLORER 
chrome = webdriver.DesiredCapabilities.CHROME
firefox = webdriver.DesiredCapabilities.FIREFOX

def setup_driver(browser):

  global driver
  driver = webdriver.Remote("http://10.8.105.107:4444/wd/hub", browser)       
  driver.implicitly_wait(10)


def teardown_driver():

  global driver

  driver.quit()
  driver = None

def get_google():

  driver.get( "http://www.google.com/" )
  el = driver.find_element_by_name( "q" )

  el.send_keys( "Cheese" )
  el.submit()


@with_setup(lambda: setup_driver(ie), teardown_driver)
def test_ie():
  get_google()


@with_setup(lambda: setup_driver(chrome), teardown_driver)
def test_chrome():
  get_google()

@with_setup(lambda: setup_driver(firefox), teardown_driver)
def test_firefox():
  get_google()
