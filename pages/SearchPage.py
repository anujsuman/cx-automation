import json

from time import sleep
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException
from utilities.WiremockClient import WiremockClient
import requests
import gzip
import json
import base64
# import pandas as pd
import logging 
from utilities.impression_util import (
    generate_impressions_lookup,
    generate_impressions_assetId_parent_id_lookup,
)
import config

logging.basicConfig(level=logging.INFO)
# Phone_number = '1420026731'
# desired_location= "unitech cyber park Tower -B"
def get_otp():
    otp = input("Please Enter OTP")
    print(f"Your OTP is {otp}")
    return otp

def back_button(self):
        # print(f" Prev Page !!!!!")
        self.driver.press_keycode(4)
        sleep(5)

class SearchView:
    # locators
    Input_number_cls = "android.widget.EditText"
    getOtp_xpath = '//*[@text="Get OTP"]'
    Continue_button_xpath = '//android.widget.TextView[@text="Continue"]'
    hamburger_xpath = "//android.view.ViewGroup[@resource-id= 'Hamburger']"
    Search_Bar_ID = "//android.view.ViewGroup[@resource-id= 'tap_home_search']"
    Trending_Product_xpath = '//android.widget.TextView[@text="Makeup"]'
    Search_Input_Bar = "//android.widget.EditText[@resource-id= 'seach_text']"


    # [OtpPage - Locator]

    def __init__(self, driver):
        self.driver = driver
        self.wc = WiremockClient()
        self.wait = WebDriverWait(self.driver, 15)

    def add_wiremock_mappings(self, user_type="repeat"):
        response = None
        if user_type == "repeat":
            user_body = '{"user":{"user_id":"29697530","user_name":"Sanvi","user_phone":"8510973876","user_type":"app","user_created":false,"user_updated":null,"tracking_info":{"source":"organic-google-play","referrer":{"installVersion":"1.33.9","installReferrer":{"utm_medium":"organic","utm_source":"google-play"},"googlePlayInstant":"false","installBeginTimestampSeconds":"1684162875","referrerClickTimestampSeconds":"0","installBeginTimestampServerSeconds":"1684162876","referrerClickTimestampServerSeconds":"0"},"app_store":"GOOGLE","ad_partner":""},"referral_code":"7Yh2Wd8T3yxuTXR2aLDJh9","whatsapp_opted_in":true,"promo_opted_in":false,"rating_done":false,"is_first_login":false,"user_image":"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png","image":"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png","address":"10485746","from_user_app":true,"one_signal_user_id":null,"rzpay_contact_id":null,"withdrawals_disabled":false,"install_google_ad_campaign":null,"advertising_partner":null,"advertising_campaign":null,"synced_ct":true,"version_name":"1.35.3check","version_code":"149","first_version_code":"133","first_version_name":"1.33.9","codepush_version":null,"last_login":"2023-09-14T09:46:46.652Z","dob":null,"advertising_set_id":null,"advertising_set_name":null,"advertising_campaign_id":null,"advertising_objective_name":null,"advertising_id":null,"location_sanity_issues":null,"location_sanity_confirmed_by_user":false,"signup_code":null,"first_order_created_at":"2023-06-09T08:24:42.194Z","first_order_id":"32134194","msite_tracking_info":null,"updated_at":"2023-09-15T07:17:03.147Z","signup_source":"cx-web","source_utm":{},"install_utm":null,"language":"en","show_cashback_confirmation":null,"cx_referral_detected":null,"is_suspended":null,"user_suspension_ticket_raised":null,"suspension_reason":null,"original_images":null,"is_optimized":false},"leader":{"id":"CITYMALL_OFFICIAL","url":"rajat-sahni","name":"CityMall","address":"39723","address1":" B-4-202 second floor KLJ Greens ","address2":"Sector 77 Faridabad","landmark":"","pincode":"122003","city":"GURGAON","state":"Haryana","phone_number":"9311413649"},"token":"fa8f147e-22db-46e7-85c1-78fa7f0c375c"}'
        else:
            user_body = '{"user":{"user_id":"356425533","user_name":null,"user_phone":"8240250410","user_type":"app","user_created":false,"user_updated":null,"tracking_info":{"source":"organic-google-play","referrer":{"installVersion":"1.34.8","installReferrer":{"utm_medium":"organic","utm_source":"google-play"},"googlePlayInstant":"false","installBeginTimestampSeconds":"1692338208","referrerClickTimestampSeconds":"0","installBeginTimestampServerSeconds":"1692338208","referrerClickTimestampServerSeconds":"0"},"app_store":"GOOGLE","ad_partner":""},"referral_code":"o7mK7w6otBdzGWbUEH4HfH","whatsapp_opted_in":false,"promo_opted_in":false,"rating_done":false,"is_first_login":false,"user_image":"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png","image":"https://storage.googleapis.com/cm-catalogue-images/1589963078748leader_image.png","address":"12015321","from_user_app":true,"one_signal_user_id":null,"rzpay_contact_id":null,"withdrawals_disabled":false,"install_google_ad_campaign":null,"advertising_partner":null,"advertising_campaign":null,"synced_ct":true,"version_name":"1.35.2","version_code":"148","first_version_code":"145","first_version_name":"1.35.0","codepush_version":null,"last_login":"2023-09-10T14:34:29.442Z","dob":null,"advertising_set_id":null,"advertising_set_name":null,"advertising_campaign_id":null,"advertising_objective_name":null,"advertising_id":null,"location_sanity_issues":null,"location_sanity_confirmed_by_user":false,"signup_code":null,"first_order_created_at":null,"first_order_id":null,"msite_tracking_info":null,"updated_at":"2023-09-11T13:02:34.024Z","signup_source":"cx_app","source_utm":{},"install_utm":null,"language":"en","show_cashback_confirmation":null,"cx_referral_detected":null,"is_suspended":null,"user_suspension_ticket_raised":null,"suspension_reason":null,"original_images":null,"is_optimized":false},"leader":{"id":"CITYMALL_OFFICIAL","url":"rajat-sahni","name":"CityMall","address":"39723","address1":" B-4-202 second floor KLJ Greens ","address2":"Sector 77 Faridabad","landmark":"","pincode":"122003","city":"GURGAON","state":"Haryana","phone_number":"9311413649"},"token":"120d8980-72d5-4e11-ad58-a37498a12a59"}'
        mapping_data_1 = {
            "name": "api_cl-user_auth_get-otp",
            "request": {"url": "/api/cl-user/auth/get-otp", "method": "POST"},
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
                    "ETag": 'W/"886-kmrXLJTN4Gl6KXiouiBHvUgzppg"',
                },
            },
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

    def enter_number(self, number):
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (MobileBy.CLASS_NAME, self.Input_number_cls)
                )
            )
            # Perform actions on the element
            element.send_keys(number)
        except TimeoutException:
            print("Element not found within the timeout.")

    def verify_getotp(self, number):
        # number = self.generate_signup_number()
        isEnableContinueBtn = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.getOtp_xpath))
        ).is_enabled()

        if len(str(number)) < 10 and True == isEnableContinueBtn:
            assert (
                True
            ), f"element is enabled, phone character length is {len(str(number))}"
        elif len(str(number)) > 10 and isEnableContinueBtn == False:
            assert (
                False
            ), f"element is not enabled, phone character length is {len(str(number))}"
        else:
            pass

    # click on get otp button
    def click_getOtp(self):
        self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.getOtp_xpath))
        ).click()

    def input_otp(self):
        # Loop through each OTP input box and locate by XPath
        otp = get_otp()
        otp_arr = list(otp)
        sleep(3)
        for i, value in enumerate(otp_arr):
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (
                        MobileBy.XPATH,
                        f"//android.widget.EditText[@resource-id='otp_input_{i}']",
                    )
                )
            ).send_keys(value)
        sleep(2)

    def clickContinue(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, self.Continue_button_xpath))
        ).click()

    def back_button(self):
        # print(f" Prev Page !!!!!")
        self.driver.press_keycode(4)
        sleep(5)
    #    Search for the desired location

    # Wait for the suggestion list to appear and select the first suggestion from list
    # Wait for the title element to be present
    def verify_hamburger(self):
        home_page_element = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, self.hamburger_xpath))
        )
        # Verify that the home page has loaded successfully
        if home_page_element.is_displayed():
            print("Home page loaded successfully.")
        else:
            print("Home page did not load successfully.")
        sleep(10)

    def clickSearchBar(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, self.Search_Bar_ID))
        ).click()
        sleep(10)

    # def click_Trending(self):
    #     WebDriverWait(self.driver, 30).until(
    #         EC.element_to_be_clickable((MobileBy.XPATH, self.Trending_Product_xpath))).click()
    #     sleep(10)

    def get_element_by_id(self, element_id):
        try:
            # import pdb;pdb.set_trace()
            
            elementXPath = f"//android.view.ViewGroup[@resource-id= '{element_id}']"
            element = self.wait.until(EC.visibility_of_element_located((MobileBy.XPATH, elementXPath)))

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

    def scroll_horizontal_screen(self):
        viewport_size = self.driver.get_window_size()
        viewport_width = viewport_size["width"]
        viewport_height = viewport_size["height"]

        horizontal_drag = viewport_width * 1.25 / 5
        scroll_count = 3  # Adjust the number of scrolls as needed

        duration = 1000

        for _ in range(scroll_count):
            start_x = viewport_width / 2
            start_y = viewport_height / 2
            end_x = start_x - horizontal_drag
            end_y = start_y  # Adjust the value as needed

            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            sleep(1)

    sleep(5)

    def scroll_vertical_screen(self):
        viewport_size = self.driver.get_window_size()
        viewport_width = viewport_size["width"]
        viewport_height = viewport_size["height"]

        vertical_drag = viewport_width * 1.25 / 5
        scroll_count = 2  # Adjust the number of scrolls as needed

        duration = 1000

        for _ in range(scroll_count):
            start_x = viewport_width / 2
            start_y = viewport_height / 2
            end_x = start_x
            end_y = start_y - vertical_drag

            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            sleep(1)

    sleep(5)

    @staticmethod
    def decode_gzip_response_body(response_body):
        decoded_data = base64.b64decode(response_body)
        decompressed_binary = gzip.decompress(decoded_data)
        decompressed_text = decompressed_binary.decode("utf-8")
        decompressed_json = json.loads(decompressed_text)

        return decompressed_json

    @staticmethod
    def get_trending_api_data():
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")

            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()

                for entry in recorded_requests["requests"]:
                    request = entry["request"]
                    response = entry["response"]

                    if "/search/api/v1/search/trending" in request["url"]:

                        if (
                            "content-encoding" in response["headers"]
                            and response["headers"]["content-encoding"] == "gzip"
                        ):
                            decoded_response_body = (
                                SearchView.decode_gzip_response_body(
                                    response["bodyAsBase64"]
                                )
                            )
                            # assigning ranks and asset_type
                            
                                
                            return decoded_response_body

            else:
                print("Failed to retrieve recorded requests")
        except Exception as e:
            print("Error: ", e)


    @staticmethod
    def get_search_api_data():
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")

            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()

                for entry in recorded_requests["requests"]:
                    request = entry["request"]
                    response = entry["response"]

                    if "/search/api/v1/suggest" in request["url"]:

                        if (
                            "content-encoding" in response["headers"]
                            and response["headers"]["content-encoding"] == "gzip"
                        ):
                            decoded_response_body = (
                                SearchView.decode_gzip_response_body(
                                    response["bodyAsBase64"]
                                )
                            )
                            return decoded_response_body

            else:
                print("Failed to retrieve recorded requests")
        except Exception as e:
            print("Error: ", e)


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
        impressionsData = self.wc.get_request(
            {"urlPathPattern": ".*/analytics/add-impression/.*"}
        )
        impressions = self.parse_impressions(impressionsData)
        return impressions

    def get_impressions_lookup(self):
        impression_data = self.getImpressionData()
        impressions_lookup = generate_impressions_lookup(impression_data)
        return impressions_lookup

    def get_impressions_assetId_parent_id_lookup(self):
        impression_data = self.getImpressionData()
        impressions_lookup = generate_impressions_assetId_parent_id_lookup(
            impression_data
        )
        return impressions_lookup

    @staticmethod
    def check_impression_diff(item, impression_item):
        impression_keys = [
            "asset_id",
            "asset_type",
            "asset_parent_id",
            "asset_parent_type",
            "action",
            "vertical_rank",
            "horizontal_rank",
            "screen_name",
            "cms_page_id",
        ]

        data = []

        for key in impression_keys:
            value1 = item.get(key)
            value2 = impression_item.get(key)

            if value1 != value2:
                data.append(["", f"  {key}  ", f"{value1}", f"{value2}"])

        # if data:
        #     # Create a DataFrame
        #     df = pd.DataFrame(data, columns=["", "key", "actual_data", "expected_data"])

        #     # Set the "Key" column as the index
        #     df.set_index("key", inplace=True)

        #     df_transposed = df.T

        #     print(df_transposed)

    def validate_impression_lookup(
        self,
        item,
        impressions_lookup=None,
        negative_impression_avail_check=False,
        retry=True,
    ):
        # item is coming from get trending api
        is_impression_valid = True

        asset_id = item["text"]
        asset_type = item["asset_type"]
        vertical_rank = item["vertical_rank"]
        horizontal_rank = item["horizontal_rank"]
        screen_name = item["screen_name"]
        action = item["action"]
        cms_page_id = item["cms_page_id"]
        asset_parent_id = item["asset_parent_id"]
        asset_parent_type = item["asset_parent_type"]

        max_count = 3

        while max_count:
            if impressions_lookup is None:
                print("Refetching Impressions !!!!")
                impressions_lookup = self.get_impressions_lookup()
                max_count = max_count -1

        matching_impression = impressions_lookup.get(
            (
                asset_parent_id,
                asset_type,
                vertical_rank,
                horizontal_rank,
                screen_name,
                action,
                cms_page_id,
                asset_parent_id,
                asset_parent_type,
            )
        )

        if negative_impression_avail_check:
            if matching_impression:
                is_impression_valid = False

                print(f"Impression Found for cms_item_id: {asset_id}")
                print(
                    f"asset_id : {asset_id} asset_type : {asset_type}, vertical_rank :{vertical_rank} , horizontal_rank:{horizontal_rank},screen_name:{screen_name}, action:{action}, cms_page_id:{cms_page_id}, asset_parent_id:{asset_parent_id},asset_parent_type:{asset_parent_type}"
                )

        else:
            if not matching_impression:
                # if retry:
                #     print(f"Retrying Impression for asset_id : {asset_id}")
                #     sleep(5)
                #     return self.validate_impression_lookup(
                #         item, None, negative_impression_avail_check, False
                #     )

                is_impression_valid = False
                return is_impression_valid
                # impression_asset_id_parent_id_lookup = (
                #     self.get_impressions_assetId_parent_id_lookup()
                # )
                # impression_available = impression_asset_id_parent_id_lookup.get(
                #     (asset_id, asset_parent_id, screen_name)
                # )

                # print(f"No Impression found for cms_item_id: {asset_id}")

                # if impression_available:
                #     self.check_impression_diff(item, impression_available)

        return is_impression_valid

    def verify_skus(self):
        try:
            trending_items = self.get_trending_api_data()

            for idx, item in enumerate(trending_items.get("results", [])):
                item["screen_name"] = "Search"
                item["action"] = "IMPRESSION"
                item["cms_page_id"] = ""
                item["asset_parent_id"] = item.get("text", "")  # Use get() to avoid KeyError
                item["asset_parent_type"] = "Search"
                item["vertical_rank"] = 0
                item["horizontal_rank"] = (idx // 2) + 1
                if idx % 2 == 0:
                    item["asset_type"] = "TRENDING_SEARCH_R1"
                else:
                    item["asset_type"] = "TRENDING_SEARCH_R2"
                
                impressions_data = self.get_impressions_lookup()
                const_element_size = None
                item_list_length = min(10, len(item.get("results", [])))  # Assuming results is a list

                item_length_index = 0

                while item_length_index < item_list_length:
                    line_item = item.get(item_length_index, {})
                    asset_id = line_item.get("asset_id", "")
                    asset_parent_id = line_item.get("asset_parent_id", "")
                    element_id = f"testid-{asset_parent_id}-{asset_id}"

                    element = self.get_element_by_id(element_id)

                    if element:
                        if item_length_index == 0:
                            const_element_size = element.size
                            element_size_visible = 100
                        else:
                            element_size_visible = self.percentage_element_visible(const_element_size, element.size)

                        if element_size_visible > 70:
                            if not self.validate_impression_lookup(item, impressions_lookup=impressions_data):
                                return False

                    item_length_index += 1

            return True
        except:
            logging.error(f"Assertion error occurred: All impressions not found")
        
            self.back_button()

    def enter_search_product(self,search_cat):
        try:
            search_input = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (MobileBy.XPATH, self.Search_Input_Bar)
                )
            )
            # Perform actions on the element
            search_input.clear()
            search_input.send_keys(search_cat)
        except TimeoutException:
            print("Element not found within the timeout.")

    def verify_search_skus(self):
        try:
            search_items = self.get_search_api_data()

            for idx, item in enumerate(search_items.get("results", [])):
                item["screen_name"] = "Search"
                item["action"] = "IMPRESSION"
                item["cms_page_id"] = ""
                item["asset_parent_id"] = item.get("text", "")  # Use get() to avoid KeyError
                item["asset_parent_type"] = "Search"
                item["vertical_rank"] = idx
                item["horizontal_rank"] = ""
                item["vertical_rank"] = idx+1
                item["horizontal_rank"] = ""
                item["asset_type"] = "SEARCH_SUGGESTIONS"
                impressions_data = self.get_impressions_lookup()
                const_element_size = None
                item_list_length = min(10, len(item.get("results", [])))  # Assuming results is a list

                item_length_index = 0

                while item_length_index < item_list_length:
                    line_item = item.get(item_length_index, {})
                    asset_id = line_item.get("asset_id", "")
                    asset_parent_id = line_item.get("asset_parent_id", "")
                    element_id = f"testid-{asset_parent_id}-{asset_id}"

                    element = self.get_element_by_id(element_id)

                    if element:
                        if item_length_index == 0:
                            const_element_size = element.size
                            element_size_visible = 100
                        else:
                            element_size_visible = self.percentage_element_visible(const_element_size, element.size)

                        if element_size_visible > 70:
                            if not self.validate_impression_lookup(item, impressions_lookup=impressions_data):
                                return False

                    item_length_index += 1

            return True
        except:
            logging.error(f"Assertion error occurred: All impressions not found")

