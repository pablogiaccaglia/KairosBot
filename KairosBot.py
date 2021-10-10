from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

import botutils


class KairosBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bookingInfoList = []

    def book(self, dateToBook):

        # chromedriver setup
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(executable_path="/Users/pablo/Desktop/chromedriver", options=chrome_options)
        time.sleep(1)

        try:
            driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&from=prenotalezione&from_include=prenotalezione_home&_lang=it")

            privacySliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[3]/div[2]/label/span'
            self.__click(driver, privacySliderXPath)

            accessSliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[4]/div[2]/label/span'
            self.__click(driver, accessSliderXPath)

            loginButtonXPath = '//*[@id="oauth_btn"]'
            self.__click(driver, loginButtonXPath)

            usernameInputXPath = '//*[@id="username"]'
            usernameWebElement = driver.find_element_by_xpath(usernameInputXPath)
            self.__fillData(driver, usernameWebElement, self.username)

            passwordInputXPath = '//*[@id="password"]'
            passwordWebElement = driver.find_element_by_xpath(passwordInputXPath)
            self.__fillData(driver, passwordWebElement, self.password)

            accessoButtonXPath = '/html/body/div/div/div/div[1]/form/div[5]/button'
            self.__click(driver, accessoButtonXPath)

            driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it")

            mainContainerXPath = '// *[ @ id = "prenotazioni_container"]'
            mainContainerWebElement = driver.find_element_by_xpath(mainContainerXPath)

            boxContainersList = mainContainerWebElement.find_elements_by_class_name("box-header-big")

            dateFound = False
            for dateBox in boxContainersList:
                dateObject = botutils.getDateTimeObjectFromItalianText(dateBox.text).date()
                if dateObject == dateToBook:
                    dateFound = True
                    coloredBox = dateBox.find_element_by_xpath("./..").find_element_by_xpath("./..")
                    coloredBoxSection1 = coloredBox.find_element_by_class_name("colored-box-section-1")
                    # classSectionList = coloredBoxSection1.find_elements_by_class_name("libretto-course-name")
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "only-1-click")))
                    lessonBookLinksList = coloredBoxSection1.find_elements_by_class_name("only-1-click")
                    for link in lessonBookLinksList:
                        WebDriverWait(driver, 5).until(EC.visibility_of(link))
                        link.click()
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="popup_conferma_title"]/span[2]')))
                        bookingInfo = driver.find_element_by_xpath('//*[@id="popup_conferma_title"]/span[2]')
                        self.bookingInfoList.append(bookingInfo.text)
                        closePopupButtonXpath = '//*[@id="popup_conferma_buttons_row"]/button'
                        self.__click(driver, closePopupButtonXpath)

            if not dateFound:
                raise Exception("Date not found")

            driver.quit()

        except Exception as e:
            print(str(e))
            if driver is not None:
                driver.quit()
            raise e

    def __click(self, driver, XPath):
        button = driver.find_element_by_xpath(XPath)
        button.click()

    def __fillData(self, driver, XPath, data):
        # clear + autofill dei campi (clear con key_down(Keys.CONTROL).send_keys('a') )
        ActionChains(driver) \
            .move_to_element(XPath) \
            .click().key_down(Keys.CONTROL) \
            .send_keys('a') \
            .key_up(Keys.CONTROL) \
            .send_keys(data) \
            .perform()
