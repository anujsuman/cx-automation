import pytest
from appium import webdriver
from pages.SignupPage import Signup
from utilities.WiremockClient import WiremockClient
import config
# Test functions using the Appium server fixture and driver
class Test_001_signup:
    loc= "unitech cyber park Tower -B"

    def test_signup(self,app_driver):
        driver = app_driver
        self.sp = Signup(app_driver)
        self.wc = WiremockClient()
        deleteAllReq = self.wc.delete_all_request(None)
        print(f"{deleteAllReq}")
        recordingStatus = self.wc.check_recording(None)
        print(f"{recordingStatus}")
        # if recordingStatus.status != 'Recording':
        self.wc.start_recording()
        num=config.PHONE_NUMBER
        # num = self.sp.generate_signup_number()
        
        self.sp.enter_number(num)
        
        self.sp.verify_getotp(num)
        self.sp.click_getOtp()

        self.sp.input_otp()
        self.sp.clickContinue()
        # self.sp.get_location_permission()
        self.sp.clickChangelocation()
        self.sp.search_location(self.loc)
        self.sp.click_firstSugestion()
        self.sp.click_enterLocation()
        self.sp.verify_hamburger()
        totalRequest = self.wc.get_request_count({})
        print(f"{totalRequest}")
        totalImpression = self.wc.get_request_count({"urlPathPattern": "/analytics/add-impression/.*"})
        print(f"{totalImpression}")
        self.sp.scroll_homepage()
        totalImpression = self.wc.get_request_count({"urlPathPattern": "/analytics/add-impression/.*"})
        print(f"{totalImpression}")
        totalRequest = self.wc.get_request_count({})
        print(f"{totalRequest}")

        impressionsData = self.wc.get_request({"urlPathPattern": "/analytics/add-impression/.*"})
        impressions = self.sp.parse_impressions(impressionsData)
        is_valid = self.sp.validate_impressions(impressions)
        print(f"{is_valid}")
        if is_valid:
            print("All required impressions found.")
        else:
            print("Not all required impressions found.")
