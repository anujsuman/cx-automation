import time
import os
from traceback import print_stack
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait

import logging


# noinspection PyBroadException
class AppiumUtil:
    # log = logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def get_web_title(self):
        """
        Used for web testing, if app opens Safari/Chrome?
        """
        return self.driver.title

    def take_screenshot(self, resultMessage):
        """
        Takes a screenshot of the current open view
        Called normally upon test failure
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenShotDirectory = "../screenshots/"
        relativeFileName = screenShotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)  # gets current file and dir of current file
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenShotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            print("Screenshot saved to directory: " + destinationFile)
        except:
            print("### Exception Occurred")
            print_stack()

    def vertical_swipe_iOS(self, direction):
        """
        Swipes the app in the direction passed in.
        Does not scroll to determined coordinates
        :param direction: "up" or "down"
        """
        self.driver.execute_script("mobile: swipe", {"direction": direction})

    def wait_for_element_to_be_clickable(self, locator, locatorType="accessibilityid",
                                         timeout=10, pollFrequency=0.5):
        """
        Waits for an element based on expected conditions (to be clickable)
        :param locator: Locator string (Ex: "id_name")
        :param locatorType: See 'getByType' for arguments (Ex: "accessibilityid"
        :param timeout: Int in seconds
        :param pollFrequency: Int in seconds
        :return: returns clickable element once the element is clickable if timeout does not expire
        """
        element = None
        try:
            byType = self.get_by_type(locatorType)
            print("Waiting for element with locator: '" + locator + "' to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
        except:
            print("Timeout expired waiting for element with locator: '" + locator + "' to be clickable")
            print_stack()
        return element

    def wait_for_element_to_appear(self, locator, locator_type="accessibilityid",
                                   timeout=10, pollFrequency=0.5):
        """
        Waits for an element based on expected conditions (to be clickable)
        :param locator: Locator string (Ex: "id_name")
        :param locator_type: See 'getByType' for arguments (Ex: "accessibilityid"
        :param timeout: Int in seconds
        :param pollFrequency: Int in seconds
        :return: returns clickable element once the element is clickable if timeout does not expire
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            print("Waiting for element with locator: '" + locator + "' to appear")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
        except:
            print_stack()
        return element

    def get_by_type(self, locator_type):
        """
        Takes a short-hand string and returns the By.LOCATORTYPE
        :param locator_type: String
        :return: By.LOCATORTYPE
        """
        locator_type = locator_type.lower()
        if locator_type == "accessibilityid":
            # iOS: accessibility-id
            # Android: content-desc
            return MobileBy.ACCESSIBILITY_ID
        elif locator_type == "classname":
            # iOS: full name of the XCUI element and begins with XCUIElementType
            # Android: full name of the UIAutomator2 class (e.g.: android.widget.TextView)
            return By.CLASS_NAME
        elif locator_type == "id":
            # Native element identifier. resource-id for android; name for iOS.
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "image":
            return MobileBy.IMAGE
        elif locator_type == "uiautomator":
            # UIAutomator2 only
            return MobileBy.ANDROID_UIAUTOMATOR
        elif locator_type == "viewtag":
            # Espresso only
            return MobileBy.ANDROID_VIEWTAG
        elif locator_type == "datamatcher":
            # Espresso only
            return MobileBy.ANDROID_DATA_MATCHER
        elif locator_type == "classchain":
            # iOS only
            return MobileBy.IOS_CLASS_CHAIN
        elif locator_type == "linktext":
            return By.LINK_TEXT
        else:
            print("Locator type not supported - or check the argument you passed in")
        return False

    def get_element(self, locator, locator_type="accessibilityid"):
        """
        Queries for an element
        """
        element = None
        try:
            # byType = self.getByType(locatorType)
            # element = self.driver.find_element(byType, locator)
            element = self.wait_for_element_to_appear(locator=locator, locator_type=locator_type)
            print("Element found with locator: '" + locator + "'")
        except:
            print("Element not found with locator: '" + locator + "'")
        return element

    def get_element_list(self, locator, locator_type="accessibilityid"):
        """
        Queries for a list of elements
        """
        element_list = None
        try:
            by_type = self.get_by_type(locator_type)
            element_list = self.driver.find_elements(by_type, locator)
            if len(element_list) == 1:
                print("Only one element in list. Consider using the singular `get_element` method instead")
            elif len(element_list) > 0:
                print("Element list found, num of elements: " + str(len(element_list)))
            else:
                print("Element list is empty. Used locator: '" + locator + "'")
        except:
            print("Invalid arguments passed into 'get_element_list' method")
        return element_list

    def click_element(self, locator="", locator_type="accessibilityid", element=None):
        """
        Clicks on an element
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.click()
            print("Clicked on element with locator: '" + locator + "'")
        except:
            print(
                "Cannot click on the element with locator: '" + locator + "'")
            print_stack()

    def send_text(self, text, locator="", locator_type="accessibilityid", element=None):
        """
        Sends text to an element
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(text)
            print("Sent keys to element with locator: '" + locator + "'")
        except:
            print(
                "Cannot send keys to element with locator: '" + locator + "'")
            print_stack()

    def get_text(self, locator="", locator_type="accessibilityid", element=None, info=""):
        """
        Get 'Text' from an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                print("In locator condition")
                element = self.get_element(locator, locator_type)
            print("Before finding text")
            text = element.text
            print("After finding element, size is: " + str(len(text)))
            if len(text) != 0:
                print("Getting text on element :: " + info)
                print("The text is :: '" + text + "'")
                text = text.strip()
        except:
            print("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def clear_field(self, locator="", locator_type="accessibilityid", element=None):
        """
        Clear an element field
        """
        if locator:
            element = self.get_element(locator, locator_type)
        element.clear()
        print("Clear field with locator: '" + locator + "'")

    def is_element_present(self, locator="", locator_type= "", element=None):
        """
        Checks for the presence of an element and returns a bool value.
        """
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                print("Element with locator: '" + locator + "' is present")
                return True
            else:
                return False
        except:
            print("Element with locator: '" + locator + "' is not present")
            return False

    def element_list_presence(self, locator, locator_type="accessibilityid"):
        # plural elements, returns bool like isElementPresent()
        try:
            elementsList = self.get_element_list(locator, locator_type)
            if len(elementsList) > 0:
                print("\nNumber of elements found: " + str(len(elementsList)))
                return True
            else:
                return False
        except:
            print("\nElement(s) are not present")
            return False

    def is_element_displayed(self, locator="", locator_type="", element=None):
        isDisplayed = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                isDisplayed = element.is_displayed()
                print("Element is displayed with locator: '" + locator + "'")
            else:
                print("Element is not displayed with locator: '" + locator + "'")
            return isDisplayed
        except:
            print("Exception on 'is_element_displayed'")
            return False

    def is_enabled(self, locator, locator_type="accessibilityid", element=None):
        enabled = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            enabled = element.is_enabled()
            if enabled:
                print("Element is enabled")
            else:
                print("Element is not enabled")
        except:
            print("Element state could not be found")
        return enabled

    def is_disabled(self, locator, locator_type="accessibilityid", element=None):
        enabled = self.is_enabled(locator, locator_type, element)
        return not enabled
