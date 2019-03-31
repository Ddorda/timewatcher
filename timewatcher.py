#!/usr/bin/python
# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
import sys
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
ABSENCE_CELL_NUMBER = -5


def get_config(config_path):
    with open(config_path) as f:
        config = json.loads(f.read())
    return config

def login(driver):
    driver.get('https://checkin.timewatch.co.il/punch/punch.php')
    config = get_config(CONFIG_PATH)
    e = driver.find_element_by_id('compKeyboard')
    e.send_keys(config['company_id'])
    e = driver.find_element_by_id('nameKeyboard')
    e.send_keys(config['user_id'])
    e = driver.find_element_by_id('pwKeyboard')
    e.send_keys(config['password'])
    e = driver.find_element_by_name('B1')
    e.click()


def fill_timewatch(driver):
    days_links_len = len(driver.find_elements_by_class_name('tr'))
    for link_num in xrange(days_links_len):
        link = driver.find_elements_by_class_name('tr')[link_num]
        # pass weekends (or any other "Yom Menucha")
        if u'יום מנוחה' in link.text:
            continue
        # pass days that have excuse for absence pre-filled (usually holidays)
        if link.find_elements_by_css_selector('td')[ABSENCE_CELL_NUMBER].text.strip():
            continue
        link.click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.execute_script("$('input#ehh0').val('11');$('input#emm0').val('00');$('input#xhh0').val('20');$('input#xmm0').val('00');$('input[type=image]').click()")
        driver.switch_to.window(driver.window_handles[-1])


def main():
    driver = webdriver.Chrome()

    login(driver)

    # Enter time watch days table
    driver.find_element_by_name('cpik').find_element_by_partial_link_text('עדכון נתוני נוכחות').click()

    fill_timewatch(driver)

    driver.close()

def generate_config():
    company_id = raw_input("Please enter company id: ")
    user_id = raw_input("Please enter user id: ")
    password = raw_input("Please enter password (probably ID), notice will be stored plain-text: ")

    config = {'company_id': company_id, 'user_id': user_id, 'password': password}
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(config))

if __name__ == '__main__':
    if not os.path.exists(CONFIG_PATH):
        print 'Config file "%s" does not exist. generating for next time...' % CONFIG_PATH
        generate_config()

    main()