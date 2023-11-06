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
# import pandas as pd
from urllib.parse import urlparse, parse_qs
from utilities.impression_util import assign_ranks_cms, re_assign_ranks_cms, assign_ranks_items, \
    generate_impressions_lookup, generate_impressions_assetId_parent_id_lookup, assign_ranks_yml_items

from selenium.webdriver.common.actions.action_builder import ActionBuilder
import config


# Phone_number = '1420026731'
# desired_location= "unitech cyber park Tower -B"
def get_otp():
    otp = input("Please Enter OTP")
    print(f"Your OTP is {otp}")
    return otp


class HomeView:
    # locators
    Input_number_cls = "android.widget.EditText"
    getOtp_xpath = '//*[@text="Get OTP"]'
    Continue_button_xpath = '//android.widget.TextView[@text="Continue"]'
    location_permission = "//android.widget.Button[@resource-id= 'com.android.permissioncontroller:id/permission_allow_foreground_only_button']"
    Change_button_xpath = "//android.widget.TextView[@text= 'Change ']"
    location_searchBar_xpath = '//*[@text= "Search area or landmark, min 3 characters"]'
    First_suggestion = "//android.widget.TextView[@text= 'Unitech Cyber Park Tower-B, Netaji Subhash Chandra Bose Road, HUDA, Sector 40, Gurugram, Haryana, 122022, India' ]"
    EnterLocation_xpath = "//hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView"
    hamburger_xpath = "//android.view.ViewGroup[@resource-id= 'Hamburger']"

    current_horizontal_length = None

    # [OtpPage - Locator]

    def __init__(self, driver):
        self.driver = driver
        self.wc = WiremockClient()
        self.wait = WebDriverWait(self.driver, 15)

        # deleteAllReq = self.wc.delete_all_request(None)
        # print(f"{deleteAllReq}")
        #
        # recordingStatus = self.wc.check_recording(None)
        # print(f"{recordingStatus}")
        # if recordingStatus["status"] == 'Recording':
        #     self.wc.start_recording()

    def add_wiremock_mappings(self, user_type='repeat'):
        response = None
        if user_type == 'repeat':
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
        #
        # response = self.wc.add_mapping(mapping_data_2)

    def get_login_number(self):
        number = 1111111111
        return number

    def back_button(self):
        # print(f" Prev Page !!!!!")
        self.driver.press_keycode(4)
        sleep(5)

    def generate_signup_number(self):
        start_with = 121
        # Generate a random 8-digit number (since we want a total of 10 digits)
        eight_digit_number = random.randint(0, 9999999)
        new_number = f"{start_with}{eight_digit_number}"
        return new_number

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

    sleep(30)

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

    def get_location_permission(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.location_permission))).click()

    # CLick on the change location
    def clickChangelocation(self):
        self.wait.until(EC.element_to_be_clickable((MobileBy.XPATH, self.Change_button_xpath))).click()

    #    Search for the desired location
    def search_location(self, desired_location):
        search_location_box = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.location_searchBar_xpath)))
        search_location_box.click()
        search_location_box.send_keys(desired_location)
        sleep(5)

    # Wait for the suggestion list to appear and select the first suggestion from list
    def click_firstSugestion(self):
        self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, self.First_suggestion))).click()

    # Wait and click enter location
    def click_enterLocation(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, self.EnterLocation_xpath))).click()

    # Wait for the title element to be present
    def verify_hamburger(self):
        home_page_element = self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, self.hamburger_xpath)))
        # Verify that the home page has loaded successfully
        if home_page_element.is_displayed():
            print("Home page loaded successfully.")
            return True
        else:
            print("Home page did not load successfully.")
            return False

    def get_element_by_id(self, element_id, infinite_load=False):
        try:
            # import pdb;pdb.set_trace()
            elementXPath = f"//android.view.ViewGroup[@resource-id= '{element_id}']"
            element = self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, elementXPath)))

            if element_id == 'Home':
                return element

            # if infinite_load:
            #     return element

            if element.is_displayed():
                element_location = element.location
                element_size = element.size

                viewport_size = self.driver.get_window_size()

                element_effective_y_location = element_location['y'] + element_size['height']

                max_viewport_height = (viewport_size['height'] * 85 / 100)

                if element_effective_y_location > max_viewport_height:
                    return None

                return element

        except TimeoutException:
            # print(f"Element with ID '{element_id}' not found within the specified timeout.")
            return None
        except Exception:
            # print(f"Element with ID '{element_id}' not found on the page.")
            traceback.print_exc()
            return None

    def get_element_by_parent_id(self, parent_element, element_id):
        element = None
        try:
            if parent_element:
                element = parent_element.find_element('xpath',
                                                      f"//android.view.ViewGroup[@resource-id= '{element_id}']")
            else:
                element = self.get_element_by_id(element_id)
        except Exception as e:
            print("Element Not Found")
        return element

    @staticmethod
    def percentage_element_visible(constant_element_size, element_size):

        constant_element_area = constant_element_size['width'] * constant_element_size['height']

        current_element_area = element_size['width'] * element_size['height']

        percentage_contained = (current_element_area / constant_element_area) * 100

        return percentage_contained

    def scroll_homepage(self):

        start_x = 800
        start_y = 534
        end_x = 215
        end_y = 534
        duration = 1000

        # Swipe up
        for i in range(0, 2):
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)

        for i in range(0, 4):
            self.driver.swipe(start_x, start_y + 300, end_x, end_y + 300, duration)

        sleep(2)

    @staticmethod
    def filter_unique_ranks(impressions):
        unique_ranks = set()
        filtered_impressions = []

        for impression in impressions:
            vertical_rank = impression.get("vertical_rank")
            horizontal_rank = impression.get("horizontal_rank")

            # Check if the combination of vertical_rank and horizontal_rank is unique
            rank_key = (vertical_rank, horizontal_rank)

            if rank_key not in unique_ranks:
                unique_ranks.add(rank_key)
                filtered_impressions.append(impression)

        return filtered_impressions

    @staticmethod
    def parse_impressions(data):
        all_imps = []

        if data and "requests" in data and len(data["requests"]) == 0:
            return all_imps

        for request in data.get("requests", []):
            if "add-impression" in request.get("url", ""):
                body = request.get("body", "")
                try:
                    impressions = json.loads(body).get("impressions", [])
                    all_imps.extend(impressions)
                except json.JSONDecodeError:
                    pass

        return all_imps

    def getImpressionData(self):
        impressionsData = self.wc.get_request({"urlPathPattern": ".*/analytics/add-impression/.*"})
        impressions = self.parse_impressions(impressionsData)
        return impressions

    def get_impressions_lookup(self):
        impression_data = self.getImpressionData()
        impressions_lookup = generate_impressions_lookup(impression_data)
        return impressions_lookup

    def get_impressions_assetId_parent_id_lookup(self):
        impression_data = self.getImpressionData()
        impressions_lookup = generate_impressions_assetId_parent_id_lookup(impression_data)
        return impressions_lookup

    @staticmethod
    def decode_gzip_response_body(response_body):
        decoded_data = base64.b64decode(response_body)
        decompressed_binary = gzip.decompress(decoded_data)
        decompressed_text = decompressed_binary.decode('utf-8')
        decompressed_json = json.loads(decompressed_text)

        return decompressed_json

    @staticmethod
    def get_cms_data():
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")

            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()

                for entry in recorded_requests['requests']:
                    request = entry['request']
                    response = entry['response']

                    if "cms-v2/v1/home" in request['url']:

                        if 'Content-Encoding' in response['headers'] and response['headers'][
                            'Content-Encoding'] == 'gzip':
                            decoded_response_body = HomeView.decode_gzip_response_body(response['bodyAsBase64'])
                            # print("Response Body: ", decoded_response_body)
                            assign_ranks_cms(decoded_response_body)
                            return decoded_response_body

            else:
                print("Failed to retrieve recorded requests")
        except Exception as e:
            print("Error: ", e)

    @staticmethod
    def get_cms_item_data_api(key='id', value=None):
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")

            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()

                for entry in recorded_requests['requests']:
                    request = entry['request']
                    response = entry['response']

                    if "api/cms-v2/v1/item" in request['url']:

                        request_cms_id = json.loads(request['body']).get(key, None)
                        if value is None or (value is not None and request_cms_id == value):

                            if 'Content-Encoding' in response['headers'] and response['headers'][
                                'Content-Encoding'] == 'gzip':
                                decoded_response_body = HomeView.decode_gzip_response_body(response['bodyAsBase64'])
                                # print("Response Body: ", decoded_response_body)
                                return decoded_response_body

            else:
                print("Failed to retrieve recorded requests")
        except Exception as e:
            print("Error: ", e)

    @staticmethod
    def get_cms_item_banner_data(key, value):
        data = HomeView.get_cms_item_data_api(key, value)
        assign_ranks_cms(data, True)
        return data

    @staticmethod
    def get_cms_item_products_data(key, value):
        data = HomeView.get_cms_item_data_api(key, value)
        assign_ranks_items(data)
        return data

    @staticmethod
    def get_cms_item_home_products_data(key, value):
        data = HomeView.get_cms_item_data_api(key, value)
        assign_ranks_items(data, True)
        return data

    @staticmethod
    def get_cms_item_yml_products_data(key, value):
        data = HomeView.get_cms_item_data_api(key, value)
        assign_ranks_yml_items(data)
        return data

    def navigate_to_home(self):

        home_element_id = 'Home'

        while True:
            home_element = self.get_element_by_id(home_element_id)
            if home_element:
                home_element.click()
                # sleep(5)
                home_element.click()
                sleep(5)

                return
            else:
                self.back_button()

    @staticmethod
    def check_impression_diff(item, impression_item):
        impression_keys = ['asset_id', 'asset_type', 'asset_parent_id', 'asset_parent_type', 'action', 'vertical_rank',
                           'horizontal_rank', 'screen_name', 'cms_page_id']

        data = []

        for key in impression_keys:
            value1 = item.get(key)
            value2 = impression_item.get(key)

            if value1 != value2:
                data.append(["", f"  {key}  ", f"{value1}", f"{value2}"])

        if data:
            # Create a DataFrame
            # df = pd.DataFrame(data, columns=["", "key", "actual_data", "expected_data"])

            # # Set the "Key" column as the index
            # df.set_index("key", inplace=True)

            # df_transposed = df.T

            # print(df_transposed)
            pass

    def validate_impression_lookup(self, item, impressions_lookup=None, negative_impression_avail_check=False,
                                   retry=True):
        is_impression_valid = True

        asset_id = item["asset_id"]
        asset_type = item["asset_type"]
        vertical_rank = item["vertical_rank"]
        horizontal_rank = item["horizontal_rank"]
        screen_name = item["screen_name"]
        action = item["action"]
        cms_page_id = item["cms_page_id"]
        asset_parent_id = item["asset_parent_id"]
        asset_parent_type = item["asset_parent_type"]

        

        matching_impression = impressions_lookup.get((asset_id, asset_type, vertical_rank, horizontal_rank,
                                                      screen_name, action, cms_page_id, asset_parent_id,
                                                      asset_parent_type))

        if negative_impression_avail_check:
            if matching_impression:
                is_impression_valid = False

                print(
                    f"Impression Found for cms_item_id: {asset_id}")
                print(
                    f"asset_id : {asset_id} asset_type : {asset_type}, vertical_rank :{vertical_rank} , horizontal_rank:{horizontal_rank},screen_name:{screen_name}, action:{action}, cms_page_id:{cms_page_id}, asset_parent_id:{asset_parent_id},asset_parent_type:{asset_parent_type}")

        else:
            if not matching_impression:

                if retry:
                    print(f"Retrying Impression for asset_id : {asset_id}")
                    sleep(2)
                    impressions_lookup = self.get_impressions_lookup()
                    return self.validate_impression_lookup(item, impressions_lookup, negative_impression_avail_check, False)

                is_impression_valid = False

                impression_asset_id_parent_id_lookup = self.get_impressions_assetId_parent_id_lookup()
                impression_available = impression_asset_id_parent_id_lookup.get(
                    (asset_id, asset_parent_id, screen_name))

                print(f"No Impression found for cms_item_id: {asset_id}")

                if impression_available:
                    self.check_impression_diff(item, impression_available)

        return is_impression_valid

    def scroll_vertical_screen(self):
        viewport_size = self.driver.get_window_size()
        viewport_height = viewport_size['height']
        viewport_width = viewport_size['width']

        vertical_drag = viewport_height * 1.25 / 5

        start_x = viewport_width / 2  # Adjust the value as needed
        start_y = viewport_height - (viewport_height * 2 / 5)
        end_x = start_x  # Adjust the value as needed
        end_y = start_y - vertical_drag

        # print(f"start_x :start_y :end_x:end_y {start_x, start_y, end_x, end_y}")

        duration = 1000

        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        sleep(1.5)

    def scroll_down_vertical_screen(self):
        viewport_size = self.driver.get_window_size()
        viewport_height = viewport_size['height']
        viewport_width = viewport_size['width']

        vertical_drag = viewport_height * 1.25 / 5

        start_x = viewport_width / 2  # Adjust the value as needed
        start_y = viewport_height - (viewport_height * 3 / 5)
        end_x = start_x  # Adjust the value as needed
        end_y = start_y + vertical_drag

        # print(f"start_x :start_y :end_x:end_y {start_x, start_y, end_x, end_y}")

        duration = 1000

        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        sleep(1.5)

    def left_Scroll_line_items(self, list_data: [], element_size, item_length_index):

        prev_line_item = list_data[item_length_index - 1]
        # print(f"prev_line_item _ {prev_line_item}")
        prev_asset_parent_id = prev_line_item["asset_parent_id"]
        prev_cms_item_id = prev_line_item["asset_id"]

        prev_element_id = f"testid-{prev_asset_parent_id}-{prev_cms_item_id}"
        # print(f"prev_element_id_{prev_element_id} ")
        prev_element = self.get_element_by_id(prev_element_id)
        if prev_element:
            element_location = prev_element.location

            viewport_size = self.driver.get_window_size()
            viewport_width = viewport_size['width']

            horizontal_drag = viewport_width * 55 / 100

            # start_x = min((viewport_width * 75 / 100), (3 * element_location['x']/2))  # Adjust the value as needed
            start_x = min(viewport_size['width'] * 70 / 100,
                          element_location['x'] + element_size['width'] / 2)  # Adjust the value as needed
            start_y = element_location['y'] + element_size['height'] / 2
            end_x = start_x - horizontal_drag  # Adjust the value as needed
            end_y = start_y

            duration = 1000

            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            sleep(1.5)

    def right_Scroll_line_items(self, list_data: [], element_size, item_length_index):

        next_line_item = list_data[item_length_index + 1]
        next_asset_parent_id = next_line_item["asset_parent_id"]
        next_cms_item_id = next_line_item["asset_id"]

        next_element_id = f"testid-{next_asset_parent_id}-{next_cms_item_id}"
        # print(f"prev_element_id_{next_element_id} ")
        next_element = self.get_element_by_id(next_element_id)
        if next_element:
            element_location = next_element.location

            viewport_size = self.driver.get_window_size()
            viewport_width = viewport_size['width']

            horizontal_drag = viewport_width * 50 / 100

            start_x = min((viewport_width * 40 / 100),
                          (element_location['x'] + (2 * element_size['width'])))  # Adjust the value as needed
            start_y = element_location['y'] + element_size['height'] / 2
            end_x = start_x + horizontal_drag  # Adjust the value as needed
            end_y = start_y

            # print(f" start_x :start_y :end_x:end_y {start_x, start_y, end_x, end_y}")

            duration = 1000

            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            sleep(2)

    # modular code

    def validate_horizontal_list_impressions(self, list_data: [], has_tested_horizontal):
        impressions_lookup = self.get_impressions_lookup()

        all_impressions_found = True

        if len(list_data) == 0:
            return False

        const_element_size = None
        item_length_index = 0
        item_list_length = min(10, len(list_data))

        line_item = list_data[0]
        asset_parent_id = line_item["asset_parent_id"]
        parent_element = self.get_element_by_id(f"testid-{asset_parent_id}")
        if parent_element:
            print(f"parent_element : {parent_element}")
        while item_length_index < item_list_length:

            line_item = list_data[item_length_index]
            asset_id = line_item["asset_id"]
            asset_parent_id = line_item["asset_parent_id"]

            element_id = f"testid-{asset_parent_id}-{asset_id}"

            # element = self.get_element_by_id(element_id)
            element = self.get_element_by_parent_id(parent_element, element_id)
            print(f" asset_id : {asset_id}, item_length_index : {item_length_index + 1}")

            if element:

                if item_length_index == 0:
                    const_element_size = element.size

                percentage_visible = HomeView.percentage_element_visible(const_element_size, element.size)

                if percentage_visible < 70:
                    no_impressions_found = self.validate_impression_lookup(line_item, impressions_lookup, True)

                    if not no_impressions_found:
                        item_length_index += 1
                        all_impressions_found = False
                        continue

                    element = None

            if element:

                item_length_index += 1

                impressions_found = self.validate_impression_lookup(line_item, impressions_lookup)
                if not impressions_found:
                    all_impressions_found = False

            else:
                print(f"asset_id : {asset_id} not found scrolling !!!")
                if item_length_index == 0:
                    self.scroll_vertical_screen()
                    impressions_lookup = self.get_impressions_lookup()

                else:
                    self.current_horizontal_length = item_length_index

                    if has_tested_horizontal:
                        return all_impressions_found

                    self.left_Scroll_line_items(list_data, const_element_size, item_length_index)
                    sleep(3)
                    impressions_lookup = self.get_impressions_lookup()

        return all_impressions_found

    def validate_horizontal_no_new_impressions(self, list_data: [], has_tested_horizontal):

        no_new_impressions_found = True

        totalImpression = self.wc.get_request_count({"urlPathPattern": ".*/analytics/add-impression/.*"})

        if len(list_data) == 0:
            return False

        const_element_size = None
        item_list_length = min(10, len(list_data))

        if has_tested_horizontal:
            item_list_length = self.current_horizontal_length

        item_length_index = item_list_length - 1

        line_item = list_data[0]
        asset_parent_id = line_item["asset_parent_id"]
        parent_element = self.get_element_by_id(f"testid-{asset_parent_id}")

        while item_length_index >= 0:

            line_item = list_data[item_length_index]
            # Extract relevant information
            asset_id = line_item["asset_id"]
            asset_parent_id = line_item["asset_parent_id"]

            element_id = f"testid-{asset_parent_id}-{asset_id}"

            element = self.get_element_by_parent_id(parent_element, element_id)
            print(f" asset_id : {asset_id}, item_length_index : {item_length_index + 1}")

            if element:
                if item_length_index == item_list_length - 1:
                    const_element_size = element.size

                percentage_visible = HomeView.percentage_element_visible(const_element_size, element.size)

                if percentage_visible < 70:
                    element = None

            if element:

                item_length_index -= 1

                newTotalImpression = self.wc.get_request_count(
                    {"urlPathPattern": ".*/analytics/add-impression/.*"})

                if totalImpression["count"] != newTotalImpression["count"]:
                    print(f"New Impression Found {asset_id} !!!")
                    no_new_impressions_found = False
            else:
                print(f"asset_id : {asset_id} not found scrolling !!!")
                self.right_Scroll_line_items(list_data, const_element_size, item_length_index)

        return no_new_impressions_found

    def validate_vertical_list_impressions(self, list_data: [], infinite_load=False):
        from time import time
        st = time()
        impressions_lookup = self.get_impressions_lookup()
        # if impressions_lookup is None:
        #     sleep(10)
        #     impressions_lookup = self.get_impressions_lookup()

        print(time()-st, 'get impressions_obj')
        all_impressions_found = True

        if len(list_data) == 0:
            return False

        const_element_size = None
        item_length_index = 0
        item_list_length = min(6, len(list_data))

        line_item = list_data[0]
        asset_parent_id = line_item["asset_parent_id"]
        st = time()
        parent_element = self.get_element_by_id(f"testid-{asset_parent_id}", infinite_load)
        print(time()-st, 'get parent elem')
        while item_length_index < item_list_length:
            print(item_length_index, item_list_length)
            line_item = list_data[item_length_index]
            asset_id = line_item["asset_id"]
            asset_parent_id = line_item["asset_parent_id"]
            st = time()
            element_id = f"testid-{asset_parent_id}-{asset_id}"
            element = self.get_element_by_parent_id(parent_element, element_id)
            print(time()-st, 'get child elem')
            print(f" asset_id : {asset_id}, item_length_index : {item_length_index + 1}")

            if element:
                if item_length_index == 0:
                    const_element_size = element.size
                st = time()
                percentage_visible = HomeView.percentage_element_visible(const_element_size, element.size)
                print(time()-st, 'calculate percentage elem', percentage_visible)
                if percentage_visible < 90:
                    no_impressions_found = self.validate_impression_lookup(line_item, impressions_lookup, True)
                    if not no_impressions_found:
                        item_length_index += 1
                        all_impressions_found = False
                        continue
                    element = None

            if element:
                item_length_index += 1
                # Check if there is a matching impression
                impressions_found = self.validate_impression_lookup(line_item, impressions_lookup)
                if not impressions_found:
                    all_impressions_found = False

            else:
                print(f"asset_id : {asset_id} not found scrolling !!!")

                self.scroll_vertical_screen()

                impressions_lookup = self.get_impressions_lookup()

        return all_impressions_found

    def validate_vertical_no_new_impressions(self, list_data: [], infinite_load=False):

        no_new_impressions_found = True

        totalImpression = self.wc.get_request_count({"urlPathPattern": ".*/analytics/add-impression/.*"})

        if len(list_data) == 0:
            return False

        const_element_size = None
        item_list_length = min(6, len(list_data))
        item_length_index = item_list_length - 1

        line_item = list_data[0]
        asset_parent_id = line_item["asset_parent_id"]
        parent_element = self.get_element_by_id(f"testid-{asset_parent_id}", infinite_load)

        from time import time
        st = time()
        while item_length_index >= 0:
            print(time() - st)
            line_item = list_data[item_length_index]

            asset_id = line_item["asset_id"]
            asset_parent_id = line_item["asset_parent_id"]
            element_id = f"testid-{asset_parent_id}-{asset_id}"

            element = self.get_element_by_parent_id(parent_element, element_id)
            print(f" asset_id : {asset_id}, item_length_index : {item_length_index + 1}")

            if element:

                if item_length_index == item_list_length - 1:
                    const_element_size = element.size

                percentage_visible = HomeView.percentage_element_visible(const_element_size, element.size)

                if percentage_visible < 70:
                    element = None

            if element:

                item_length_index -= 1

                newTotalImpression = self.wc.get_request_count(
                    {"urlPathPattern": ".*/analytics/add-impression/.*"})

                if totalImpression["count"] != newTotalImpression["count"]:
                    print(f"New Impression Found  - asset_id : {asset_id} !!!")
                    no_new_impressions_found = False
            else:
                print(f"asset_id : {asset_id} not found scrolling !!!")

                self.scroll_down_vertical_screen()

        return no_new_impressions_found

    def validate_vertical_list(self, list_data: [], infinite_load=False):
        all_vertical_impression_found = self.validate_vertical_list_impressions(list_data, infinite_load)
        # if all_vertical_impression_found:
        #     print(f"All required impressions found. cms_item_id : {asset_id}")
        # else:
        #     print(f"Not all required impressions found. cms_item_id : {asset_id}")

        no_duplicate_vertical_impression = self.validate_vertical_no_new_impressions(list_data, infinite_load)
        # if not no_duplicate_vertical_impression:
        #     print(f"Duplicate impressions found. cms_item_id : {asset_id}")
        # else:
        #     print(f"No Duplicate impressions found. cms_item_id : {asset_id}")

        sleep(2)

        return all_vertical_impression_found and no_duplicate_vertical_impression

    def validate_horizontal_list(self, list_data: [], has_tested_horizontal=False):
        all_horizontal_impression_found = self.validate_horizontal_list_impressions(list_data, has_tested_horizontal)
        # if all_horizontal_impression_found:
        #     print(f"All required impressions found. cms_item_id : {asset_id}")
        # else:
        #     print(f"Not all required impressions found. cms_item_id : {asset_id}")

        no_duplicate_horizontal_impression = self.validate_horizontal_no_new_impressions(list_data,
                                                                                         has_tested_horizontal)
        # if not no_duplicate_horizontal_impression:
        #     print(f"Duplicate impressions found. cms_item_id : {asset_id}")
        # else:
        #     print(f"No Duplicate impressions found. cms_item_id : {asset_id}")

        sleep(2)

        return all_horizontal_impression_found and no_duplicate_horizontal_impression

    def wait_till_list_visible(self, list_items, idx):
        if idx < len(list_items) - 1:
            next_list_item = list_items[idx]

            while True:
                asset_id = next_list_item.get("asset_id")
                next_element_id = f"testid-{asset_id}"
                next_element = self.get_element_by_id(next_element_id)
                if next_element:
                    return
                else:
                    self.scroll_vertical_screen()
        else:
            self.scroll_vertical_screen()

    def validate_pdp_sku_impression(self, line_item):
        asset_id = line_item["asset_id"]

        item = line_item

        item['asset_type'] = "SKU"
        item['vertical_rank'] = None
        item['horizontal_rank'] = None
        item['screen_name'] = 'ProductDetails'
        item['cms_page_id'] = None

        asset_parent_id = line_item["asset_parent_id"]

        element_id = f"testid-{asset_parent_id}-{asset_id}"

        element = self.get_element_by_id(element_id)

        element.click()

        sleep(5)

        impressions_lookup = self.get_impressions_lookup()

        is_valid = self.validate_impression_lookup(item, impressions_lookup)

        self.back_button()

        return is_valid

    def validate_products_pdp(self, item_data):
        is_valid = True
        const_element_size = None

        line_item_index = 0

        while line_item_index < min(4, len(item_data)):
            line_item = item_data[line_item_index]
            asset_id = line_item["asset_id"]

            asset_parent_id = line_item["asset_parent_id"]

            element_id = f"testid-{asset_parent_id}-{asset_id}"

            product_element = self.get_element_by_id(element_id)

            if product_element:

                if not const_element_size:
                    const_element_size = product_element.size

                element_percentage = self.percentage_element_visible(const_element_size, product_element.size)

                if element_percentage < 95:
                    product_element = None

            if product_element:
                line_item_index += 1

                is_pdp_valid = self.validate_pdp_sku_impression(line_item)
                if not is_pdp_valid:
                    is_valid = False

            else:
                self.scroll_vertical_screen()

        return is_valid

    def validate_you_may_like_products(self, item_data):
        is_valid = True
        const_element_size = None
        has_tested_horizontal = False
        line_item_index = 0
        from time import time 
        st = time()
        while line_item_index < len(item_data):
            print(time() - st)
            st = time()
            line_item = item_data[line_item_index]
            asset_id = line_item["asset_id"]

            asset_parent_id = line_item["asset_parent_id"]

            element_id = f"testid-{asset_parent_id}-{asset_id}"

            product_element = self.get_element_by_id(element_id)

            if product_element:

                if not const_element_size:
                    const_element_size = product_element.size

                element_percentage = self.percentage_element_visible(const_element_size, product_element.size)

                if element_percentage < 90:
                    product_element = None

            if product_element:
                line_item_index += 1

                add_button = None

                try:
                    add_button = product_element.find_element('xpath', "//android.widget.TextView[@text ='ADD']")
                except Exception as e:
                    print(f"Add Button Not Present")

                if not add_button:
                    continue

                add_button.click()

                sleep(5)

                you_may_like_data = HomeView.get_cms_item_yml_products_data('cart_sku', asset_id)
                product_data = you_may_like_data["data"].get("products", [])

                if len(product_data) > 0:
                    self.scroll_vertical_screen()
                    is_yml_valid = self.validate_horizontal_list(product_data, has_tested_horizontal)
                    has_tested_horizontal = True
                    return is_yml_valid

            else:
                self.scroll_vertical_screen()

        return is_valid

    def validate_pdp_from_sku_list(self):
        is_valid = True

        cms_data = self.get_cms_data()

        data_items = cms_data["data"].get("list_items", [])
        idx = 0

        for item in data_items:
            self.wait_till_list_visible(data_items, idx)
            idx += 1
            print(idx)
            if item.get("asset_type") == "SKU_LIST" and item.get('horizontal') == True:
                products = item.get("products", [])
                print()
                const_element_size = None

                line_item_index = 0
                from time import time
                
                while line_item_index < min(3, len(products)):
                    st = time()
                    line_item = products[line_item_index]
                    asset_id = line_item["asset_id"]
                    asset_parent_id = line_item["asset_parent_id"]
                    element_id = f"testid-{asset_parent_id}-{asset_id}"
                    product_element = self.get_element_by_id(element_id)

                    if product_element:

                        if not const_element_size:
                            const_element_size = product_element.size

                        element_percentage = self.percentage_element_visible(const_element_size, product_element.size)

                        if element_percentage < 70:
                            product_element = None

                    if product_element:
                        line_item_index += 1

                        is_pdp_valid = self.validate_pdp_sku_impression(line_item)
                        if not is_pdp_valid:
                            is_valid = False

                    else:
                        self.left_Scroll_line_items(products, const_element_size, line_item_index)
                    print("----  line_item_index  --", line_item_index, time() - st)
                return is_valid

    def validate_yml_from_sku_list_view_all(self):
        is_valid = True
        cms_data = self.get_cms_data()

        data_items = cms_data["data"].get("list_items", [])

        idx = 0
        from time import time
        st = time()
        for item in data_items:
            self.wait_till_list_visible(data_items, idx)
            print(time() - st,'wait_till_list_visible')
            idx += 1
            if item.get("asset_type") == "SKU_LIST":
                product_card_element_id = item.get('asset_id')
                st = time()
                product_card_element = self.get_element_by_id(f"testid-{product_card_element_id}")
                print(time() - st,'get_element_by_id')
                st = time()
                view_all_button = product_card_element.find_element('xpath',"//android.widget.TextView[@text ='View all']")
                
                
                print(time() - st,'find_element')
                view_all_button.click()

                sleep(5)
                st = time()
                cms_item_data = HomeView.get_cms_item_products_data('id', product_card_element_id)
                print(time() - st,'cms_item_data')
                product_data = cms_item_data["data"].get("products", [])
                # is_product_list_valid = self.validate_vertical_list(product_data,True)
                # if not is_product_list_valid:
                #     is_valid = False

                is_yml_valid = self.validate_you_may_like_products(product_data)
                if not is_yml_valid:
                    is_valid = False

                return is_valid

    def validate_pdp_from_sku_list_view_all(self):
        is_valid = True

        cms_data = self.get_cms_data()
        data_items = cms_data["data"].get("list_items", [])
        idx = 0

        for item in data_items:

            self.wait_till_list_visible(data_items, idx)
            idx += 1
            if item.get("asset_type") == "SKU_LIST":
                product_card_element_id = item.get('asset_id')
                product_card_element = self.get_element_by_id(f"testid-{product_card_element_id}")

                view_all_button = product_card_element.find_element('xpath',
                                                                    "//android.widget.TextView[@text ='View all']")

                view_all_button.click()

                sleep(5)

                cms_item_data = HomeView.get_cms_item_products_data('id', product_card_element_id)
                product_data = cms_item_data["data"].get("products", [])
                is_product_list_valid = self.validate_vertical_list(product_data, True)
                if not is_product_list_valid:
                    is_valid = False

                is_products_pdp_valid = self.validate_products_pdp(product_data)
                if not is_products_pdp_valid:
                    is_valid = False

                return is_valid

    def validate_banner_impressions(self, list_item):
        is_valid = True
        has_tested_horizontal = False
        asset_id = list_item['asset_id']
        parent_cms_item_id = list_item['asset_parent_id']
        element_id = f"testid-{parent_cms_item_id}-{asset_id}"

        link = list_item['data']['link']
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)
        entity_id = query_params.get('entityId', [])[0]

        element = self.get_element_by_id(element_id)
        element.click()

        sleep(5)

        cms_item_data = HomeView.get_cms_item_data_api('id', entity_id)

        if cms_item_data["data"]["type"] == 'PAGE':
            cms_item_data = HomeView.get_cms_item_banner_data('id', entity_id)

            sub_banner_validated = False

            for list_item in cms_item_data["data"].get("list_items", []):

                if 'products' in list_item:

                    product_data = list_item['products']
                    horizontal_list = list_item.get('horizontal', False)

                    if horizontal_list:
                        is_horiz_products_list_valid = self.validate_horizontal_list(product_data,
                                                                                     has_tested_horizontal)
                        has_tested_horizontal = True
                        if not is_horiz_products_list_valid:
                            is_valid = False

                    else:

                        infinite_load = list_item.get('infinite_load', False)

                        if infinite_load:
                            cms_items_data_id = list_item['asset_id']
                            cms_item_data = HomeView.get_cms_item_products_data('id', cms_items_data_id)
                            product_data = cms_item_data["data"].get("products", [])

                        is_vert_products_list_valid = self.validate_vertical_list(product_data, True)
                        if not is_vert_products_list_valid:
                            is_valid = False

                elif 'list_items' in list_item:
                    data_items = list_item.get("list_items", [])

                    if not sub_banner_validated:
                        if len(data_items) > 1:
                            is_banner_valid = self.validate_banner_impressions(data_items[0])
                            if not is_banner_valid:
                                is_valid = False
                            sub_banner_validated = True

                    if list_item['asset_type'] == 'BANNER_LIST_HORIZONTAL':
                        is_horiz_list_items_valid = self.validate_horizontal_list(data_items, has_tested_horizontal)
                        has_tested_horizontal = True
                        if not is_horiz_list_items_valid:
                            is_valid = False
                    elif list_item['asset_type'] == 'NxM_GRID':
                        is_vert_list_items_valid = self.validate_vertical_list(data_items)
                        if not is_vert_list_items_valid:
                            is_valid = False

        elif cms_item_data["data"]["type"] == 'SKU_LIST':

            cms_item_data = HomeView.get_cms_item_products_data('id', entity_id)
            product_data = cms_item_data["data"].get("products", [])

            is_vert_products_list_valid = self.validate_vertical_list(product_data, True)
            if not is_vert_products_list_valid:
                is_valid = False

        self.back_button()

        return is_valid

    def validate_category_banner(self):
        cms_data = self.get_cms_data()

        for item in cms_data["data"].get("list_items", []):

            if item.get("asset_type") == "BANNER_LIST_HORIZONTAL":
                list_data = item.get("list_items", [])
                list_item = list_data[0]

                return self.validate_banner_impressions(list_item)

    def validate_women_banner(self):
        cms_data = self.get_cms_data()

        idx = 0
        for item in cms_data["data"].get("list_items", []):

            if item.get("asset_type") == "BANNER_LIST_HORIZONTAL":
                if idx == 0:
                    idx += 1
                    continue

                idx += 1

                list_data = item.get("list_items", [])
                list_item = list_data[1]

                return self.validate_banner_impressions(list_item)

    def validate_men_banner(self):
        cms_data = self.get_cms_data()

        idx = 0
        for item in cms_data["data"].get("list_items", []):

            if item.get("asset_type") == "BANNER_LIST_HORIZONTAL":
                if idx == 0:
                    idx += 1
                    continue

                idx += 1

                list_data = item.get("list_items", [])
                list_item = list_data[0]

                return self.validate_banner_impressions(list_item)

    def validate_Home_page(self):
        is_valid = True
        cms_data = self.get_cms_data()

        has_tested_horizontal = False

        while True:
            idx = 0
            list_items_data = cms_data["data"].get("list_items", [])

            for list_item in list_items_data:

                asset_id = list_item["asset_id"]

                self.wait_till_list_visible(list_items_data, idx)

                idx += 1
                print(idx, list_item['asset_type'])
                if 'products' in list_item:

                    product_data = list_item['products']
                    horizontal_list = list_item.get('horizontal', False)

                    if horizontal_list:
                        is_horiz_products_list_valid = self.validate_horizontal_list(product_data,
                                                                                     has_tested_horizontal)
                        has_tested_horizontal = True
                        if not is_horiz_products_list_valid:
                            is_valid = False

                    else:

                        infinite_load = list_item.get('infinite_load', False)

                        # continue
                        if infinite_load:
                            cms_items_data_id = list_item['asset_id']
                            cms_item_data = HomeView.get_cms_item_home_products_data('id', cms_items_data_id)
                            product_data = cms_item_data["data"].get("products", [])

                        is_vert_products_list_valid = self.validate_vertical_list(product_data, True)
                        if not is_vert_products_list_valid:
                            is_valid = is_vert_products_list_valid

                elif 'list_items' in list_item:

                    data_items = list_item.get("list_items", [])

                    if list_item['asset_type'] == 'BANNER_LIST_HORIZONTAL':
                        # print(f"asset_id : {asset_id} - validate_horizontal_list")
                        is_horiz_list_items_valid = self.validate_horizontal_list(data_items, has_tested_horizontal)
                        has_tested_horizontal = True
                        if not is_horiz_list_items_valid:
                            is_valid = is_horiz_list_items_valid
                    elif list_item['asset_type'] == 'NxM_GRID':
                        # print(f"asset_id : {asset_id} - validate_vertical_list")
                        is_vert_list_items_valid = self.validate_vertical_list(data_items)
                        if not is_vert_list_items_valid:
                            is_valid = is_vert_list_items_valid

            canFetchMore = cms_data["canFetchMore"]
            if canFetchMore:
                self.scroll_vertical_screen()
                sleep(5)
                print(" fetching new cms Data !!!!! ")
                new_cms_data = self.get_cms_data()
                re_assign_ranks_cms(cms_data, new_cms_data)

                cms_data = new_cms_data
            else:
                return is_valid

