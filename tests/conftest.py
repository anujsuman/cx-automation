import pytest
from appium import webdriver
from time import sleep
import json
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
import config
import warnings


class capabilities_launchApp:
    appium_service = AppiumService()
    appium_service.start()

    # Desired capabilities for your Android device and app
    capabilities = dict(
        deviceName=config.DEVICENAME,
        platformName=config.PLATFORMNAME,
        automationName=config.AUTOMATIONNAME,
        # platformVersion=config.PLATFORMVERSION,
        appPackage=config.APPPACKAGE,
        appActivity=config.APPACTIVITY,
        autoGrantPermissions=config.AUTOGRANTPERMISSIONS,
        app=config.APP,
        isHeadless=True,
    )
    def setup(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self.driver = webdriver.Remote(config.WD_URL, self.capabilities)
        # self.driver.remove_app('live.citymall.customer.prod')

    def teardown(self):
        self.driver.quit()
        self.appium_service.stop()

# Define a pytest fixture to set up the driver before each test and tear it down after each test
@pytest.fixture(scope='session')
def app_driver():
    app = capabilities_launchApp()
    app.setup()
    yield app.driver  # The test will run here
    app.teardown()

