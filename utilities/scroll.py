from appium.webdriver.common.appiumby import AppiumBy
class Scroll:
    def __init__(self, driver):
        self.driver = driver

    def scrollToTextByUiautomator(self, text):
        self.driver.find_element_by_android_uiautomator("new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().textContains(\"" + text + "\").instance(0))")
        # resourceIdMatches("{my_id}" + ".*")
    def swipeUp(self,howManySwipes):
            for i in range(1, howManySwipes + 1):
                self.driver.swipe(514, 600, 514, 200, 1000)

    def swipeDown(self, howManySwipes):
        for i in range(1, howManySwipes + 1):
            self.driver.swipe(514, 500, 514, 800, 1000)


    def swipeLeft(self,howManySwipes):
        for i in range(1, howManySwipes + 1):
            self.driver.swipe(900, 600, 200, 600, 1000)

    def swipeRight(self,howManySwipes):
        for i in range(1, howManySwipes + 1):
            self.driver.swipe(200, 600, 900, 600, 1000)

    def scrollToIDByUiautomator(self, my_id, target_element_resource_id):
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                 f'new UiScrollable(new UiSelector().resourceIdMatches("{my_id}" + ".*").scrollable(true).instance(0).scrollIntoView(new UiSelector().resourceId("{target_element_resource_id}").instance(0))')



