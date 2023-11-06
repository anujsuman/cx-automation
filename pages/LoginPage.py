import json

from appium import webdriver
import os
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException
from utilities.WiremockClient import WiremockClient
import random
import traceback
import requests
import gzip
import json
import base64
from utilities.configReader import readConfig
from appium.webdriver.common.appiumby import AppiumBy


from selenium.webdriver.common.actions.action_builder import ActionBuilder


# Phone_number = '1420026731'
# desired_location= "unitech cyber park Tower -B"
def get_otp():
    otp = input("Please Enter OTP")
    print(f"Your OTP is {otp}")
    return otp


class LoginView:
    # locators
    Input_number_cls = "android.widget.EditText"
    getOtp_xpath = '//*[@text="Get OTP"]'
    Continue_button_xpath = '//android.widget.TextView[@text="Continue"]'
    hamburger_xpath = "//android.view.ViewGroup[@resource-id= 'Hamburger']"

    # [OtpPage - Locator]

    def __init__(self, driver):
        self.driver = driver
        self.wc = WiremockClient()
        self.wait = WebDriverWait(self.driver, 15)

    def add_wiremock_mappings(self, user_type='repeat'):
        response = None
        if user_type =='repeat':
            user_body = "{\"user\":{\"user_id\":\"29697530\",\"user_name\":\"Sanvi\",\"user_phone\":\"8510973876\",\"user_type\":\"app\",\"user_created\":false,\"user_updated\":null,\"tracking_info\":{\"source\":\"organic-google-play\",\"referrer\":{\"installVersion\":\"1.33.9\",\"installReferrer\":{\"utm_medium\":\"organic\",\"utm_source\":\"google-play\"},\"googlePlayInstant\":\"false\",\"installBeginTimestampSeconds\":\"1684162875\",\"referrerClickTimestampSeconds\":\"0\",\"installBeginTimestampServerSeconds\":\"1684162876\",\"referrerClickTimestampServerSeconds\":\"0\"},\"app_store\":\"GOOGLE\",\"ad_partner\":\"\"},\"referral_code\":\"7Yh2Wd8T3yxuTXR2aLDJh9\",\"whatsapp_opted_in\":true,\"promo_opted_in\":false,\"rating_done\":false,\"is_first_login\":false,\"user_image\":\"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png\",\"image\":\"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png\",\"address\":\"10485746\",\"from_user_app\":true,\"one_signal_user_id\":null,\"rzpay_contact_id\":null,\"withdrawals_disabled\":false,\"install_google_ad_campaign\":null,\"advertising_partner\":null,\"advertising_campaign\":null,\"synced_ct\":true,\"version_name\":\"1.35.3check\",\"version_code\":\"149\",\"first_version_code\":\"133\",\"first_version_name\":\"1.33.9\",\"codepush_version\":null,\"last_login\":\"2023-09-14T09:46:46.652Z\",\"dob\":null,\"advertising_set_id\":null,\"advertising_set_name\":null,\"advertising_campaign_id\":null,\"advertising_objective_name\":null,\"advertising_id\":null,\"location_sanity_issues\":null,\"location_sanity_confirmed_by_user\":false,\"signup_code\":null,\"first_order_created_at\":\"2023-06-09T08:24:42.194Z\",\"first_order_id\":\"32134194\",\"msite_tracking_info\":null,\"updated_at\":\"2023-09-15T07:17:03.147Z\",\"signup_source\":\"cx-web\",\"source_utm\":{},\"install_utm\":null,\"language\":\"en\",\"show_cashback_confirmation\":null,\"cx_referral_detected\":null,\"is_suspended\":null,\"user_suspension_ticket_raised\":null,\"suspension_reason\":null,\"original_images\":null,\"is_optimized\":false},\"leader\":{\"id\":\"CITYMALL_OFFICIAL\",\"url\":\"rajat-sahni\",\"name\":\"CityMall\",\"address\":\"39723\",\"address1\":\" B-4-202 second floor KLJ Greens \",\"address2\":\"Sector 77 Faridabad\",\"landmark\":\"\",\"pincode\":\"122003\",\"city\":\"GURGAON\",\"state\":\"Haryana\",\"phone_number\":\"9311413649\"},\"token\":\"fa8f147e-22db-46e7-85c1-78fa7f0c375c\"}"
        else:
            user_body = "{\"user\":{\"user_id\":\"356425533\",\"user_name\":null,\"user_phone\":\"8240250410\",\"user_type\":\"app\",\"user_created\":false,\"user_updated\":null,\"tracking_info\":{\"source\":\"organic-google-play\",\"referrer\":{\"installVersion\":\"1.34.8\",\"installReferrer\":{\"utm_medium\":\"organic\",\"utm_source\":\"google-play\"},\"googlePlayInstant\":\"false\",\"installBeginTimestampSeconds\":\"1692338208\",\"referrerClickTimestampSeconds\":\"0\",\"installBeginTimestampServerSeconds\":\"1692338208\",\"referrerClickTimestampServerSeconds\":\"0\"},\"app_store\":\"GOOGLE\",\"ad_partner\":\"\"},\"referral_code\":\"o7mK7w6otBdzGWbUEH4HfH\",\"whatsapp_opted_in\":false,\"promo_opted_in\":false,\"rating_done\":false,\"is_first_login\":false,\"user_image\":\"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png\",\"image\":\"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png\",\"address\":\"12015321\",\"from_user_app\":true,\"one_signal_user_id\":null,\"rzpay_contact_id\":null,\"withdrawals_disabled\":false,\"install_google_ad_campaign\":null,\"advertising_partner\":null,\"advertising_campaign\":null,\"synced_ct\":true,\"version_name\":\"1.35.2\",\"version_code\":\"148\",\"first_version_code\":\"145\",\"first_version_name\":\"1.35.0\",\"codepush_version\":null,\"last_login\":\"2023-09-10T14:34:29.442Z\",\"dob\":null,\"advertising_set_id\":null,\"advertising_set_name\":null,\"advertising_campaign_id\":null,\"advertising_objective_name\":null,\"advertising_id\":null,\"location_sanity_issues\":null,\"location_sanity_confirmed_by_user\":false,\"signup_code\":null,\"first_order_created_at\":null,\"first_order_id\":null,\"msite_tracking_info\":null,\"updated_at\":\"2023-09-11T13:02:34.024Z\",\"signup_source\":\"cx_app\",\"source_utm\":{},\"install_utm\":null,\"language\":\"en\",\"show_cashback_confirmation\":null,\"cx_referral_detected\":null,\"is_suspended\":null,\"user_suspension_ticket_raised\":null,\"suspension_reason\":null,\"original_images\":null,\"is_optimized\":false},\"leader\":{\"id\":\"CITYMALL_OFFICIAL\",\"url\":\"rajat-sahni\",\"name\":\"CityMall\",\"address\":\"39723\",\"address1\":\" B-4-202 second floor KLJ Greens \",\"address2\":\"Sector 77 Faridabad\",\"landmark\":\"\",\"pincode\":\"122003\",\"city\":\"GURGAON\",\"state\":\"Haryana\",\"phone_number\":\"9311413649\"},\"token\":\"120d8980-72d5-4e11-ad58-a37498a12a59\"}"
        mapping_data_1 = {
            "name": "api_cl-user_auth_get-otp",
            "request": {
                "url": "/api/cl-user/auth/get-otp",
                "method": "POST"
            },
            "response": {
                "status": 200,
                "body": user_body,
                "headers": {
                    "Date": "Mon, 11 Sep 2023 13:04:26 GMT",
                    "Content-Type": "application/json; charset=utf-8",
                    "Vary": "Accept-Encoding",
                    "X-Powered-By": "Express",
                    "RateLimit-Limit": "10",
                    "RateLimit-Remaining": "4",
                    "RateLimit-Reset": "1201",
                    "Set-Cookie": "cluser_sess=120d8980-72d5-4e11-ad58-a37498a12a59; Max-Age=31536000; Path=/; Expires=Tue, 10 Sep 2024 13:04:26 GMT; HttpOnly; Secure",
                    "ETag": "W/\"886-kmrXLJTN4Gl6KXiouiBHvUgzppg\""
                }
            }
        }
        response = self.wc.add_mapping(mapping_data_1)

        # print(f"mapping_data_1 _ {response}")

        # mapping_data_2 = {
        #     "request": {
        #         "method": "ANY"
        #     },
        #     "response": {
        #         "status": 200,
        #         "proxyBaseUrl": "https://citymall.live"
        #     },
        #     "persistent": True
        # }
        
        # response = self.wc.add_mapping(mapping_data_2)


         # print(f"mapping_data_1 _ {response}")

        mapping_data_3 = {
            "request": {
                "urlPathPattern": ".*/api/analytics/add-impression/.*",
                "method": "POST"
            },
            "response": {
                "status": 200,
                "headers": {
                    "Date": "Tue, 10 Oct 2023 10:08:03 GMT",
                    "Content-Type": "text/plain; charset=utf-8",
                    "Content-Length": "7"
                },
                "body": "success"
            }
        }
        response = self.wc.add_mapping(mapping_data_3)


    def enter_number(self, number):
        try:

            element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((MobileBy.CLASS_NAME, self.Input_number_cls)))
            # Perform actions on the element
            element.send_keys(number)
        except TimeoutException:
            print("Element not found within the timeout.")

    def verify_getotp(self, number):
        # number = self.generate_signup_number()
        isEnableContinueBtn = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.getOtp_xpath))).is_enabled()

        if len(str(number)) < 10 and True == isEnableContinueBtn:
            assert True, f"element is enabled, phone character length is {len(str(number))}"
        elif len(str(number)) > 10 and isEnableContinueBtn == False:
            assert False, f"element is not enabled, phone character length is {len(str(number))}"
        else:
            pass

    # click on get otp button
    def click_getOtp(self):
        self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, self.getOtp_xpath))).click()

    def input_otp(self):
        # Loop through each OTP input box and locate by XPath
        otp = get_otp()
        otp_arr = list(otp)
        sleep(3)
        for i, value in enumerate(otp_arr):
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
                (MobileBy.XPATH, f"//android.widget.EditText[@resource-id='otp_input_{i}']"))).send_keys(value)
        sleep(2)

    def clickContinue(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, self.Continue_button_xpath))).click()

    #    Search for the desired location
    
    # Wait for the suggestion list to appear and select the first suggestion from list
    # Wait for the title element to be present
    def verify_hamburger(self):
        home_page_element = self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, self.hamburger_xpath)))
        # Verify that the home page has loaded successfully
        if home_page_element.is_displayed():
            print("Home page loaded successfully.")
        else:
            print("Home page did not load successfully.")
        sleep(10)

    def check_otp_screen(self):
        sp = LoginView(self.driver)

        # ei = Extract_impression(self)
        try:
            is_otp_screen = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((MobileBy.XPATH, readConfig("OTP_Page", "Verify_otp"))))
            if is_otp_screen:
                print("OTP page loaded successfully")
                sp.input_otp()
                sp.clickContinue()
                sp.verify_hamburger()
                print("ID SKU")

            sleep(5)

        except Exception as e:
            print(e)
            sp.verify_hamburger()

        finally:
            print("home screen loaded")

    def scrollToIDByUiautomator(self, my_id, target_element_resource_id):
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().resourceIdMatches("{my_id}" + ".*").scrollable(true).instance(0).scrollIntoView(new UiSelector().resourceId("{target_element_resource_id}").instance(0))')

