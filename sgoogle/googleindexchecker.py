#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Mai Xuan Trang
# 
#

import time
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BTN_XPATH = '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'
Q_XPATH = '//*[@id="lst-ib"]'
TITLE_XPATH = '//div[@class="rc"]/h3/a'

class URLIdexed(object):
    def __init__(self, url, indexed):
        self.url = url
        self.indexed = indexed

class IndexChecker(object):
    def __init__(self, urls, use_proxy=True, tld="com"):
        self.urls = urls
        self.tld = tld
        self.use_proxy = use_proxy
    
    def init_driver(self, driver_type=0):
        if driver_type % 2 == 0:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://127.0.0.1:8123')
            driver = webdriver.Chrome(executable_path="/Users/trang/WebDriver/chromedriver", chrome_options=chrome_options)
            driver.wait = WebDriverWait(driver, 5)
            driver.get("http://www.google.com")
        else:
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference("network.proxy.type", 1)
            firefox_profile.set_preference("network.proxy.http", "localhost")
            firefox_profile.set_preference("network.proxy.http_port", 8123)
            firefox_profile.set_preference("network.proxy.no_proxies_on", "")
            firefox_profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile=firefox_profile)
            driver.wait = WebDriverWait(driver, 5)
            driver.get("http://www.google.com")
            ibox = driver.wait.until(EC.presence_of_element_located((By.NAME, 'q')))
            ibox.send_keys("start")
            ibutton = driver.wait.until(EC.element_to_be_clickable((By.NAME, 'btnK')))
            ibutton.click()
        return driver


    def init_driver_remote(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("network.proxy.type", 1)
        firefox_profile.set_preference("network.proxy.http", "localhost")
        firefox_profile.set_preference("network.proxy.http_port", 8123)
        firefox_profile.set_preference("network.proxy.no_proxies_on", "")
        firefox_profile.update_preferences()
        remoteHost="http://localhost:4444/wd/hub"
        driver = webdriver.Remote(command_executor=remoteHost, desired_capabilities=DesiredCapabilities.FIREFOX)
        driver.wait = WebDriverWait(driver, 5)
        driver.get("http://www.google.com")
        return driver
    
    
    def check_solenium_remote(self):
        checkedurls = []
        no_url_checked = 1
        no_driver_reset = 0
        sTime = datetime.now()
        driver = self.init_driver_remote()
        print "Start checking URLs"
        for url in self.urls:
            if no_url_checked % 10 == 0:
                driver.quit()
                no_driver_reset = no_driver_reset + 1
                driver = self.init_driver_remote()
            
            if no_url_checked % 100 == 0:
                driver.quit()
                time.sleep(60)
                no_driver_reset = no_driver_reset + 1
                driver = self.init_driver_remote()
  
            startTime = datetime.now()
            print "  Start checking URL: %s" %url
            q = 'info:'+url
            try:
                box = driver.wait.until(EC.presence_of_element_located((By.NAME, 'q')))
                
                #driver.find_element_by_name("q").clear()
                print "    Found box"
                box.clear()
                box.send_keys(q)
                button = driver.wait.until(EC.element_to_be_clickable((By.NAME, 'btnG')))

                print "    Found button"
                button.click()
                print "    Button clicked"
                indexed = 'No'
                try:
                    #e = driver.find_element_by_xpath(TITLE_XPATH)
                    e = driver.wait.until(EC.presence_of_element_located((By.XPATH, TITLE_XPATH)))
                    if e:
                        indexed = 'Yes'
                except Exception as e:
                    print e.message
                    pass
                
                urlindexed = URLIdexed(url, indexed)
                checkedurls.append(urlindexed)
                no_url_checked = no_url_checked + 1
                #time.sleep(randint(3, 5))
                print "     Checked"
            except Exception as e:
                print e.message
                driver.quit()
        print "All URLs are checked"
        driver.quit()

        return checkedurls

    def check_solenium(self):
        checkedurls = []
        no_url_checked = 1
        no_driver_reset = 0
        sTime = datetime.now()
        driver = self.init_driver(1)
        print "Start checking URLs"
        for url in self.urls:
            if no_url_checked % 10 == 0:
                driver.quit()
                no_driver_reset = no_driver_reset + 1
                driver = self.init_driver(no_driver_reset)
            
            if no_url_checked % 100 == 0:
                driver.quit()
                time.sleep(60)
                no_driver_reset = no_driver_reset + 1
                driver = self.init_driver(no_driver_reset)
  
            startTime = datetime.now()
            print "  Start checking URL: %s" %url
            q = 'info:'+url
            try:
                box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
                #driver.find_element_by_name("q").clear()
                box.clear()
                box.send_keys(q)
                button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "btnG")))
                button.click()
                indexed = 'No'
                try:
                    #e = driver.find_element_by_xpath(TITLE_XPATH)
                    e = driver.wait.until(EC.presence_of_element_located((By.XPATH, TITLE_XPATH)))
                    if e:
                        indexed = 'Yes'
                except Exception as e:
                    pass
                
                urlindexed = URLIdexed(url, indexed)
                checkedurls.append(urlindexed)
                no_url_checked = no_url_checked + 1
                #time.sleep(randint(3, 5))
                print "     Checked URL: %s in %f seconds" % (url, (datetime.now() - startTime).total_seconds())
            except Exception:
                print "Box or Button not found in google.com"
                driver.quit()
        print "All URLs are checked in: %f seconds" % ((datetime.now() - sTime).total_seconds())
        driver.quit()

        return checkedurls





