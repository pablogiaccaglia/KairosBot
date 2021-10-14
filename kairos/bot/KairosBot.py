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
        self.driver = self.__initDriver()
        self.courseNamesList = []

    def __initDriver(self):
        # chromedriver setup
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        path = relativeToAbsPath("chromedriver")
        return Chrome(executable_path=path, options=chrome_options)

    def __goToBookableLessons(self):

        try:
            self.driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&from=prenotalezione&from_include=prenotalezione_home&_lang=it")

            privacySliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[3]/div[2]/label/span'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, privacySliderXPath)))
            self.__click(privacySliderXPath)

            accessSliderXPath = '//*[@id="main-content"]/div[4]/div[2]/div[2]/div/div[4]/div[2]/label/span'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, accessSliderXPath)))
            self.__click(accessSliderXPath)

            loginButtonXPath = '//*[@id="oauth_btn"]'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, loginButtonXPath)))
            self.__click(loginButtonXPath)

            usernameInputXPath = '//*[@id="username"]'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, usernameInputXPath)))
            usernameWebElement = self.driver.find_element(By.XPATH, usernameInputXPath)
            self.__fillData(usernameWebElement, self.username)

            passwordInputXPath = '//*[@id="password"]'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, passwordInputXPath)))
            passwordWebElement = self.driver.find_element(By.XPATH, passwordInputXPath)
            self.__fillData(passwordWebElement, self.password)

            accessoButtonXPath = '/html/body/div/div/div/div[1]/form/div[5]/button'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, accessoButtonXPath)))
            self.__click(accessoButtonXPath)

            self.driver.get(
                "https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it")

        except Exception as e:
            raise e

    def scrapeCourseNames(self):

        courseNamesList = []

        try:
            self.__goToBookableLessons()
            mainContainerXPath = '// *[ @ id = "prenotazioni_container"]'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, mainContainerXPath)))
            mainContainerWebElement = self.driver.find_element(By.XPATH, mainContainerXPath)
            WebDriverWait(mainContainerWebElement, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "box-header-big")))
            boxContainersList = mainContainerWebElement.find_elements(By.CLASS_NAME, "box-header-big")

            for dateBox in boxContainersList:
                coloredBox = dateBox.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                coloredBoxSection1 = coloredBox.find_element(By.CLASS_NAME, "colored-box-section-1")
                classSectionList = coloredBoxSection1.find_elements(By.CLASS_NAME, "libretto-course-name")
                for selection in classSectionList:
                    if selection.text not in courseNamesList:
                        courseNamesList.append(selection.text)

            for name in courseNamesList:
                print(name)

        except Exception as e:
            raise e

    def book(self, dateToBook):

        try:

            self.__goToBookableLessons()
            mainContainerXPath = '// *[ @ id = "prenotazioni_container"]'
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, mainContainerXPath)))
            mainContainerWebElement = self.driver.find_element(By.XPATH, mainContainerXPath)
            WebDriverWait(mainContainerWebElement, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "box-header-big")))
            boxContainersList = mainContainerWebElement.find_elements(By.CLASS_NAME, "box-header-big")

            dateFound = False

            for dateBox in boxContainersList:
                dateObject = getDateTimeObjectFromItalianText(dateBox.text).date()
                if dateObject == dateToBook:
                    dateFound = True

                    coloredBox = dateBox.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                    coloredBoxSection1 = coloredBox.find_element(By.CLASS_NAME, "colored-box-section-1")
                    # classSectionList = coloredBoxSection1.find_elements_by_class_name("libretto-course-name")
                    WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "only-1-click")))
                    lessonBookLinksList = coloredBoxSection1.find_elements(By.CLASS_NAME, "only-1-click")

                    for link in lessonBookLinksList:
                        WebDriverWait(self.driver, 5).until(EC.visibility_of(link))
                        link.click()

                        WebDriverWait(self.driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="popup_conferma_title"]/span[2]')))
                        bookingInfo = self.driver.find_element(By.XPATH, '//*[@id="popup_conferma_title"]/span[2]')
                        self.bookingInfoList.append(bookingInfo.text)

                        closePopupButtonXpath = '//*[@id="popup_conferma_buttons_row"]/button'
                        WebDriverWait(self.driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, closePopupButtonXpath)))
                        self.__click(closePopupButtonXpath)

            if not dateFound:
                raise Exception("Date not found")

            self.driver.quit()

            if len(self.bookingInfoList) == 0:
                raise Exception("No available lessons to book")

            for info in self.bookingInfoList:
                self.bookingInfoDicts.append(parseBookingInfo(info))

        except Exception as e:
            if self.driver is not None:
                self.driver.quit()
            raise e

    def __click(self, XPath):
        button = self.driver.find_element(By.XPATH, XPath)
        button.click()

    def __fillData(self, XPath, data):
        # clear + autofill dei campi (clear con key_down(Keys.CONTROL).send_keys('a') )
        ActionChains(self.driver) \
            .move_to_element(XPath) \
            .click().key_down(Keys.CONTROL) \
            .send_keys('a') \
            .key_up(Keys.CONTROL) \
            .send_keys(data) \
            .perform()


# if __name__ == '__main__':
#    bo = KairosBot("7028112", "Vannoni-1")
#    bo.scrapeCourseNames()
