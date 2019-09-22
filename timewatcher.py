#!/usr/bin/python
# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
import sys
import os
import json
import time

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
ABSENCE_CELL_NUMBER = -5
DAY_TYPE_NUMBER = 1
FREE_DAYS = [u'שישי', u'שבת', u'ערב חג', u'חג']


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

def wait_for_document_ready(driver):
    while driver.execute_script('return document.readyState;') != 'complete':
        time.sleep(0.001)

def fill_timewatch(driver):
    config = get_config(CONFIG_PATH)
    entrance_hour_hour, entrance_hour_minute = config['entrance_hour'].split(':')
    leaving_hour_hour, leaving_hour_minute = config['leaving_hour'].split(':')

    fill_form_script = "$('input#ehh0').val('%s');$('input#emm0').val('%s');$('input#xhh0').val('%s');$('input#xmm0').val('%s');$('input[type=image]').click()"
    fill_form_script = fill_form_script % (entrance_hour_hour, entrance_hour_minute, leaving_hour_hour, leaving_hour_minute)

    has_day_name = True
    days_links_len = len(driver.find_elements_by_class_name('tr'))
    # Missing "Shem Yom" (day name)
    if len(driver.find_elements_by_class_name('tr')[0].find_elements_by_css_selector('td')) == 13:
        has_day_name = False

    for link_num in xrange(days_links_len):
        link = driver.find_elements_by_class_name('tr')[link_num]
        # pass weekends (or any other "Yom Menucha")
        if has_day_name and u'יום מנוחה' in link.text:
            continue
        elif has_day_name == False and link.find_elements_by_css_selector('td')[DAY_TYPE_NUMBER].text.strip() in FREE_DAYS:
            continue
        # pass days that have excuse for absence pre-filled (usually holidays)
        if link.find_elements_by_css_selector('td')[ABSENCE_CELL_NUMBER].text.strip():
            continue
        link.click()
        driver.switch_to.window(driver.window_handles[-1])
        # There's a glitch here, probably because of the window changing.
        # therefore we need to wait for document load manully.
        wait_for_document_ready(driver)
        driver.execute_script(fill_form_script)
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
    entrance_hour = raw_input("Please enter your entrance hour. leave empty for default (11:00): ")
    if not entrance_hour:
        entrance_hour = '11:00'
    leaving_hour = raw_input("Please enter your leaving hour. leave empty for default (20:00): ")
    if not leaving_hour:
        leaving_hour = '20:00'

    config = {'company_id': company_id, 'user_id': user_id, 'password': password, 'entrance_hour': entrance_hour, 'leaving_hour': leaving_hour}
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(config))

if __name__ == '__main__':
    if not os.path.exists(CONFIG_PATH):
        print 'Config file "%s" does not exist. generating for next time...' % CONFIG_PATH
        generate_config()

    main()
