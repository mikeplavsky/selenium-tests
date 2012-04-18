from selenium import webdriver
from nose.tools import eq_,with_setup
from selenium.webdriver.support.ui import WebDriverWait

multiprocess_can_split_ = True

driver = None

ie = webdriver.DesiredCapabilities.INTERNETEXPLORER 
chrome = webdriver.DesiredCapabilities.CHROME
ff = webdriver.DesiredCapabilities.FIREFOX

def get_hub_ip():

  import DNS
  DNS.defaults['server'] = ["ns-92.awsdns-11.com."]

  return DNS.dnslookup( "selenium.quest.com", "A" )[0]

hub_ip = get_hub_ip()

tests_url = None
hem = None

def setup_f(browser):

  import socket

  tests_ip = socket.gethostbyname(socket.gethostname())

  s = socket.socket()
  s.bind(('',0))
  port = s.getsockname()[1]

  del s
  
  global hem
  import subprocess

  import os
  cwd = os.path.dirname(os.path.abspath( __file__ ))
  hem = subprocess.Popen( ("../node_modules/hem/bin/hem", "server", "--port=%s" % port), cwd = cwd )

  global tests_url
  tests_url = "http://%s:%s/test" % (tests_ip,port)
  
  global driver
  driver = webdriver.Remote("http://%s:4444/wd/hub" % hub_ip, browser)       

def teardown_f():

  global driver

  driver.quit()
  driver = None

  global hem

  hem.terminate()
  hem = None

def run():

  driver.get( tests_url )

  finished = lambda x: x.find_element_by_css_selector( ".finished-at" ).text.startswith("Finished")
  WebDriverWait(driver,60).until(finished)

  el = driver.find_element_by_css_selector(".runner")
  eq_( "runner passed", el.get_attribute( "classname" ))

@with_setup(lambda: setup_f(ff), teardown_f)
def test_ff():
  run()

@with_setup(lambda: setup_f(ie), teardown_f)
def test_ie():
  run()

@with_setup(lambda: setup_f(chrome), teardown_f)
def test_chrome():
  run()
