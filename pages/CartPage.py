import traceback
from time import sleep

from urllib3.util import retry

from utilities.appium_util import AppiumUtil
import requests
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from utilities.configReader import readConfig
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from utilities.WiremockClient import WiremockClient
from selenium.webdriver.support.ui import WebDriverWait
import config
from pages.HomePage import HomeView
import json



class Cart:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.homeView = HomeView(self.driver)
        self.wc = WiremockClient()
        self.appiumutill = AppiumUtil(self.driver)

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

    def scrollToIDByUiautomator(self, target_element_resource_id):
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                 f'new UiScrollable((new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().resourceId("{target_element_resource_id}").instance(0))')

    def remove_item_from_cart(self):
        self.wait.until(EC.visibility_of_element_located(
            (MobileBy.XPATH, readConfig(("Cart-Locator", "Xpath_deduct_qnty_btn"))))).click()

    def get_cms_view_cart_data(self):
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")
            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()
                for entry in recorded_requests['requests']:
                    request = entry['request']
                    response = entry['response']
                    # print("vew_cart_url", request['url'])
                    if "cl-user/view-cart-cms" in request['url']:
                        if 'Content-Encoding' in response['headers'] and response['headers'][
                            'Content-Encoding'] == 'gzip':
                            decode_response_body = self.homeView.decode_gzip_response_body(
                                response['bodyAsBase64'])
                            return decode_response_body
            else:
                print("Falied to retrieve recorded requets")
        except Exception as e:
            print("Error:", e)

    def is_view_cart(self):
        cart_items = []
        view_cart = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text = 'View Cart']")))
        if view_cart.is_displayed():
            view_cart.click()
            print("clicked on cart page")

    def get_qty_from_view_cart(self):
        total_cart_products = None
        get_qty_cart = self.wait.until(
            EC.visibility_of_element_located((MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Items')]")))
        try:
            if get_qty_cart.is_displayed():
                total_cart_products = get_qty_cart.text
            else:
                total_cart_products = 0
        except Exception as e:
            print("cart empty", e)
        return total_cart_products

    def add_products_from_sku_list(self):
        cms_data = self.homeView.get_cms_data()
        data_items = cms_data["data"].get("list_items", [])
        idx = 0
        list_items = []

        for item in data_items:
            if item.get("asset_type") == "SKU_LIST" and item.get('horizontal') == True:
                products = item.get("products", [])
                const_element_size = None

                for line_item_index in range(len(products)):
                    add_button = None
                    line_item = products[line_item_index]
                    list_items.append(line_item)
                    asset_id = line_item["asset_id"]
                    asset_parent_id = line_item["asset_parent_id"]
                    element_id = f"testid-{asset_parent_id}-{asset_id}"
                    product_element = self.get_element_by_id(element_id)
                    print(f"element_found", {product_element})

                    if product_element:
                        if line_item_index == 0:
                            const_element_size = product_element.size
                        if not const_element_size:
                            const_element_size = product_element.size
                        element_percentage = self.homeView.percentage_element_visible(const_element_size,
                                                                                      product_element.size)
                        if element_percentage < 70:
                            product_element = None

                    if product_element:
                        try:
                            add_button = product_element.find_element('xpath',
                                                                      "//android.widget.TextView[@text ='ADD']")
                            add_button.click()
                            print(f"Item Added to Cart. Current Cart Size {self.get_qty_from_view_cart()}\n")
                        except Exception as e:
                            print(f"Add Button Not Present\n", e)
                            continue
                    else:
                        self.homeView.left_Scroll_line_items(list_items, const_element_size, line_item_index)

                    idx += 1
                    total_cart_products = self.get_qty_from_view_cart()
                    if int(total_cart_products.split(" ")[0]) >= 6:
                        print("Number of products in cart ", self.get_qty_from_view_cart())
                        return
            self.homeView.scroll_vertical_screen()

    def generate_impressions_lookup(self, impression_data):
        impressions_lookup = {}
        for impression in impression_data:
            asset_type = impression.get("asset_type")
            vertical_rank = impression.get("vertical_rank")
            horizontal_rank = impression.get("horizontal_rank")
            screen_name = impression.get("screen_name")
            action = impression.get("action")
            asset_parent_id = impression.get("asset_parent_id")
            asset_parent_type = impression.get("asset_parent_type")
            source = impression.get("source")
            asset_id = impression.get("asset_id")
            key = (asset_id, asset_type, vertical_rank, horizontal_rank,
                   screen_name, action, asset_parent_id, asset_parent_type, source)
            impressions_lookup[key] = impression

        return impressions_lookup

    def load_cart_list(self):
        sleep(7)
        view_cart_data = self.get_cms_view_cart_data()
        cart_cms_data = view_cart_data["cartPage"]
        sleep(3)
        is_valid_impression = {}

        product = None
        const_el_size = None
        base_lookup_keys = ("SKU", "PlaceOrder", "IMPRESSION", "cart_items", "cart_items", "Home")

        for item in cart_cms_data:
            if item.get('type') == "cartItemsByEdd":
                for sub_items in item["items"]:
                    sub_item = sub_items['items']
                    for item_index in range(len(sub_item)):
                        item_id = sub_item[item_index]['sku_id']
                        # item_name = sub_item[item_index]['short_name_hi']
                        element_id = f"testid-cart_items-{item_id}"
                        try:
                            product = self.get_element_by_id(element_id)
                            if item_index == 0:
                                const_el_size = product.size
                        except Exception as e:
                            print("Product possibly not loaded completely. No element returned", e)
                        finally:
                            if product:
                                element_percentage = self.homeView.percentage_element_visible(const_el_size,
                                                                                              product.size)
                                if element_percentage < 70:
                                    product = None
                            else:
                                self.homeView.scroll_vertical_screen()
                                product = self.get_element_by_id(element_id)

        impression_data = self.homeView.getImpressionData()
        impression_list = []
        for impression in impression_data:
            if impression["screen_name"] == "PlaceOrder" and impression["asset_parent_type"] == "cart_items":
                impression_list.append(impression)

        impressions_lookup = self.generate_impressions_lookup(impression_list)

        for key in list(impressions_lookup.keys()):
            comp_key = (key[1], key[4], key[5], key[6], key[7], key[8])
            # import pdb; pdb.set_trace()
            if all(a == b for a, b in zip(base_lookup_keys, comp_key)):
                is_valid_impression[key] = "VALID"
            else:
                is_valid_impression[key] = "INVALID"

        is_valid_impression = dict((str(k), v) for k, v in is_valid_impression.items())
        print("\n\n", json.dumps(is_valid_impression, indent=2))

    @staticmethod
    def get_cms_item_data_api(key, value=None):
        """get you_may_like CMSdata on cartPage"""
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")

            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()

                for entry in recorded_requests['requests']:
                    request = entry['request']
                    response = entry['response']

                    if "api/cms-v2/v1/item" in request['url']:
                        if 'Content-Encoding' in response['headers'] and response['headers'][
                            'Content-Encoding'] == 'gzip':
                            decoded_response_body = HomeView.decode_gzip_response_body(response['bodyAsBase64'])
                            response_title_ref = decoded_response_body["data"].get(key, None)
                            if value is None or (value is not None and response_title_ref == value):
                                return decoded_response_body

            else:
                print("Failed to retrieve recorded requests")
        except Exception as e:
            print("Error: ", e)

    def wait_till_yml_parentID_visible(self):
        # if idx < len(list_items) - 1:
        #     next_list_item = list_items[idx]
        cart_you_may_like = self.get_cms_item_data_api('title_ref', 'you-may__sku_list')
        while True:
            asset_parent_id = cart_you_may_like["data"]["cms_item_id"]
            parent_id = f"testid-{asset_parent_id}"
            next_element = self.get_element_by_id(parent_id)
            if next_element:
                print("parent_id found")
                break  # Break the loop when the parent ID is found
            self.homeView.scroll_vertical_screen()

    def left_Scroll_line_items(self, products: [], element_size, item_length_index):
        list_data = products
        prev_line_item = list_data[item_length_index - 1]
        cart_you_may_like = self.get_cms_item_data_api('title_ref', 'you-may__sku_list')
        prev_asset_parent_id = cart_you_may_like["data"]["cms_item_id"]

        prev_cms_item_id = prev_line_item["sku_id"]

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
            sleep(5)

    def validate_you_may_like_cartPage(self):
        """validate yml_impression data for you_may_like"""
        is_valid = True
        const_element_size = None
        has_tested_horizontal = False
        line_item_index = 0
        product_data = None
        list_items = []
        asset_parent_id = None
        impression_list = []
        is_valid_impression = {}
        base_lookup_keys = ("SKU", "PlaceOrder", "IMPRESSION", "YOU_MAY_ALSO_LIKE_CART", "CART")
        cart_you_may_like = self.get_cms_item_data_api('title_ref', 'you-may__sku_list')
        if cart_you_may_like:
            print("cart_you_may_like_cms: is persent")
            products = cart_you_may_like["data"]["products"]
            self.wait_till_yml_parentID_visible()
            for line_item_index in range(len(products)):
                line_item = products[line_item_index]
                list_items.append(line_item)
                asset_id = line_item["sku_id"]
                asset_parent_id = cart_you_may_like["data"]["cms_item_id"]

                element_id = f"testid-{asset_parent_id}-{asset_id}"
                product_element = self.get_element_by_id(element_id)

                if product_element:
                    if line_item_index == 0:
                        const_element_size = product_element.size
                    if not const_element_size:
                        const_element_size = product_element.size
                    element_percentage = self.homeView.percentage_element_visible(const_element_size,
                                                                                  product_element.size)

                    if element_percentage < 90:
                        product_element = None

                if product_element:
                    try:
                        add_button = product_element.find_element('xpath',
                                                                  "//android.widget.TextView[@text ='ADD']")
                        add_button.click()
                        print(f"Item Added to Cart. Current Cart Size {self.get_qty_from_view_cart()}\n")
                    except Exception as e:
                        print(f"Add Button Not Present\n", e)
                        continue

                else:
                    self.left_Scroll_line_items(list_items, const_element_size, line_item_index)
                """ATC MOI 8"""
                total_cart_products = self.get_qty_from_view_cart()
                if int(total_cart_products.split(" ")[0]) >= 10:
                    print("Number of products in cart ", self.get_qty_from_view_cart())
                    break
        sleep(5)
        impression_data = self.homeView.getImpressionData()
        print("impression")
        for impression in impression_data:
            if impression["screen_name"] == "PlaceOrder" and impression[
                "asset_parent_type"] == "YOU_MAY_ALSO_LIKE_CART":
                impression_list.append(impression)
        impression_lookup = self.generate_impressions_lookup(impression_list)
        for key in list(impression_lookup.keys()):
            com_key = (key[1], key[4], key[5], key[7], key[8])
            if all(a == b for a, b in zip(base_lookup_keys, com_key)):
                is_valid_impression[key] = "Valid"
            else:
                is_valid_impression[key] = "INVALID"
        is_valid_impression = dict((str(k), v) for k, v in is_valid_impression.items())
        print("Yml impression", "\n\n", json.dumps(is_valid_impression, indent=2))

    def get_cms_wishlist_data(self):
        try:
            wiremock_base_url = f"{config.WIREMOCK_URL}/__admin/"
            recorded_requests_response = requests.get(wiremock_base_url + "requests")
            if recorded_requests_response.status_code == 200:
                recorded_requests = recorded_requests_response.json()
                for entry in recorded_requests['requests']:
                    request = entry['request']
                    response = entry['response']
                    # print("vew_cart_url", request['url'])
                    if "cl-user/view-wishlist" in request['url']:
                        req_headers_data = request['headers']
                        url = request['absoluteUrl']
                        response = requests.get(url, headers=req_headers_data)
                        JsonResponse = response.json()
                        return JsonResponse
            else:
                print(f"Fail to Wiremock bae URL with status code: {recorded_requests_response.status_code}")
        except Exception as e:
            print("Error:", e)

    def validate_wishlist_cms_data_for_cartPage(self):
        wishlist_data = self.get_cms_wishlist_data()
        # print(wishlist_data)
        const_el_size = None
        product = None
        sku_list = []
        wishlist_products = wishlist_data['products']
        for line_item_index in range(len(wishlist_products)):
            line_item = wishlist_products[line_item_index]
            asset_id = line_item['sku_id']
            sku_list.append(asset_id)
            element_id = f"testid-cart_page_wishlist_modal-{asset_id}"

            try:
                product = self.get_element_by_id(element_id)
                if line_item_index == 0:
                    const_el_size = product.size
            except Exception as e:
                print("Product possibly not loaded completely. No element returned", e)
            finally:
                if product:
                    element_percentage = self.homeView.percentage_element_visible(const_el_size,
                                                                                  product.size)
                    if element_percentage < 70:
                        product = None
                else:
                    self.homeView.scroll_vertical_screen()
                    product = self.get_element_by_id(element_id)

        impresssion_lookup = self.homeView.get_impressions_lookup()
        print("impression")
        is_impression_valid = True
        for item in sku_list:
            asset_id = item
            if impresssion_lookup is None:
                print("refetching impression!!")
            matching_impression = impresssion_lookup.get(asset_id)

            if matching_impression:
                is_impression_valid = False
                print(f"impression found for sku_id: {asset_id}")
            else:
                if not matching_impression:
                    if retry:
                        print(f"retrying impression for asset_id : {asset_id}")
                        sleep(2)
                    print(f"No Impression found for cms_item_id: {asset_id}")

    def get_wishlist_popup_element(self, element_id, infinite_load=False):
        try:
            # import pdb;pdb.set_trace()
            elementXPath = f"//android.widget.ScrollView[contains(@resource-id, '{element_id}']"
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
                assert element.is_displayed(), "Popup is not found or not visible"
                print("Popup appeared on the screen")
                return element

        except TimeoutException:
            # print(f"Element with ID '{element_id}' not found within the specified timeout.")
            return None
        except Exception:
            # print(f"Element with ID '{element_id}' not found on the page.")
            traceback.print_exc()
            return None

    def wishlist_popup_modal(self):
        """click on move_to_cart_from_wishlist link on cart page"""
        while True:
            try:
                move_to_cart_from_wishlist = self.wait.until(EC.visibility_of_element_located(
                    (MobileBy.XPATH, readConfig("Cart-Locator", "Xpath_mtcFw"))))
                move_to_cart_from_wishlist.click()
                print("Clicked on move_to_cart_from_wishlist")
                assert True, "move_to_cart_from_wishlist click was not successful"
                break
            except Exception as e:
                # when the element is not found, and continue scrolling
                print(e, "wishlist_popup_not_found")
                self.homeView.scroll_vertical_screen()
        sleep(3)
        # popup_elementId = 'testid-cart_page_wishlist_modal'
        # popup_ele = self.get_wishlist_popup_element(popup_elementId)
        #
        # # Assert that the popup element is displayed
        # assert popup_ele.is_displayed(), "Popup element is not displayed"
        print("Popup element found and displayed")

    def press_back_button(self):
        # 4 is the keycode for KEYCODE_BACK
        self.driver.press_keycode(4)


