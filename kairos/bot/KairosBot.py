from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from kairos.bot.botutils import getDateTimeObjectFromItalianText, parseBookingInfo
from kairos.utils import relativeToAbsPath


class KairosBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bookingInfoList = []
        self.bookingInfoDicts = []

    def book(self, dateToBook):

        # chromedriver setup
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        path = relativeToAbsPath("chromedriver")
        driver = Chrome(executable_path=path, options=chrome_options)

        try:
            driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&from=prenotalezione&from_include=prenotalezione_home&_lang=it")

            privacySliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[3]/div[2]/label/span'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, privacySliderXPath)))
            self.__click(driver, privacySliderXPath)

            accessSliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[4]/div[2]/label/span'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, accessSliderXPath)))
            self.__click(driver, accessSliderXPath)

            loginButtonXPath = '//*[@id="oauth_btn"]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, loginButtonXPath)))
            self.__click(driver, loginButtonXPath)

            usernameInputXPath = '//*[@id="username"]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, usernameInputXPath)))
            usernameWebElement = driver.find_element_by_xpath(usernameInputXPath)
            self.__fillData(driver, usernameWebElement, self.username)

            passwordInputXPath = '//*[@id="password"]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, passwordInputXPath)))
            passwordWebElement = driver.find_element_by_xpath(passwordInputXPath)
            self.__fillData(driver, passwordWebElement, self.password)

            accessoButtonXPath = '/html/body/div/div/div/div[1]/form/div[5]/button'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, accessoButtonXPath)))
            self.__click(driver, accessoButtonXPath)

            driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it")

            mainContainerXPath = '// *[ @ id = "prenotazioni_container"]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, mainContainerXPath)))
            mainContainerWebElement = driver.find_element_by_xpath(mainContainerXPath)
            WebDriverWait(mainContainerWebElement, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "box-header-big")))
            boxContainersList = mainContainerWebElement.find_elements_by_class_name("box-header-big")

            dateFound = False

            for dateBox in boxContainersList:
                dateObject = getDateTimeObjectFromItalianText(dateBox.text).date()
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

                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="popup_conferma_title"]/span[2]')))
                        bookingInfo = driver.find_element_by_xpath('//*[@id="popup_conferma_title"]/span[2]')
                        self.bookingInfoList.append(bookingInfo.text)

                        closePopupButtonXpath = '//*[@id="popup_conferma_buttons_row"]/button'
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, closePopupButtonXpath)))
                        self.__click(driver, closePopupButtonXpath)

            if not dateFound:
                raise Exception("Date not found")

            driver.quit()

            if len(self.bookingInfoList) == 0:
                raise Exception("No available lessons to book")

            for info in self.bookingInfoList:
                self.bookingInfoDicts.append(parseBookingInfo(info))

        except Exception as e:
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
