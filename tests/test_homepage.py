import pytest
from appium import webdriver
# from pages.HomeView import HomeView
from pages.HomePage import HomeView
from pages.LoginPage import LoginView
from utilities.WiremockClient import WiremockClient
import config
from time import sleep
import unittest
from utilities import impression_util


# Test functions using the Appium server fixture and driver
class TestHomePage:
    @pytest.fixture(autouse=True, scope='class')
    def classSetup(self, app_driver):
        # print(self.driver)
        num = config.PHONE_NUMBER
        self.driver = app_driver
        self.wc = WiremockClient()
        self.login = LoginView(self.driver)

        # self.wc.reset_wiremock()
        self.wc.stop_recording()
        sleep(2)
        self.wc.delete_all_mapping()
        sleep(2)
        self.wc.start_recording()
        sleep(2)
        self.login.add_wiremock_mappings()
        self.wc.delete_all_request(None)
        
        # self.login.add_wiremock_mappings()
        # self.wc.save_mapping()
        self.login.enter_number(num)
        self.login.verify_getotp(num)
        self.login.click_getOtp()
        sleep(10)

    @pytest.fixture(autouse=True)
    def navigate_to_home_page(self, app_driver):
        self.home = HomeView(app_driver)
        self.home.navigate_to_home()

    def test_home_page_loaded(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.verify_hamburger() is True

    
    # passed
    def test_validate_yml_from_sku_list_all(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_yml_from_sku_list_view_all() is True
    #
    # failed
    def test_validate_pdp_from_sku_list_all(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_pdp_from_sku_list_view_all() is True

    # failed
    def test_validate_pdp_from_sku_list_only(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_pdp_from_sku_list() is True

    # passed
    def test_validate_category_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_category_banner() is True

    # # failed
    def test_validate_women_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_women_banner() is True

    def test_validate_men_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_men_banner() is True

    def test_validate_cms_data(self,app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_Home_page() is True
        # sleep(10)


    # def test_banner_list_horizontal(self, app_driver):
    #     self.home = HomeView(app_driver)
    #     self.home_page_data = self.home.get_cms_data()
    #     idx = 0
    #     home_list_items = self.home_page_data["data"].get("list_items", [])
    #     for item in home_list_items:
    #         if item.get("type") == "BANNER_LIST_HORIZONTAL":
    #             if idx == 1:
    #                 print("break")
    #                 break
    
    #             all_horizontal_impression_found = self.home.validate_horizontal_banner(item)
    
    #             if all_horizontal_impression_found:
    #                 print(f"All required Horizontal impressions found. {idx}")
    #             else:
    #                 print(f"Not all required impressions found. {idx}")
    #             assert all_horizontal_impression_found == True
    #             idx += 1

    # def test_duplicate_impression_horizontal(self, app_driver):    
    #     self.home = HomeView(app_driver)        
    #     no_duplicate_horizontal_impression = self.home.validate_no_new_horizontal_impressions()

    #     print(f"{no_duplicate_horizontal_impression}")
    #     if no_duplicate_horizontal_impression:
    #         print("Duplicate impressions found.")
    #     else:
    #         print("No Duplicate Horizontal impressions found.")
    #     assert no_duplicate_horizontal_impression == True

    #     all_vertical_impression_found = self.home.validate_vertical_products()
    #     print(f"{all_vertical_impression_found}")
    #     if all_vertical_impression_found:
    #         print("All required Vertical impressions found.")
    #     else:
    #         print("Not all required impressions found.")
    
    # passed
    def test_validate_yml_from_sku_list_all(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_yml_from_sku_list_view_all() is True
        sleep(10)
    #
    # failed
    def test_validate_pdp_from_sku_list_all(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_pdp_from_sku_list_view_all() is True

    # failed
    def test_validate_pdp_from_sku_list_only(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_pdp_from_sku_list() is True

    # passed
    def test_validate_category_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_category_banner() is True

    # # failed
    def test_validate_women_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_women_banner() is True

    def test_validate_men_banner(self, app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_men_banner() is True

    def test_validate_cms_data(self,app_driver):
        self.home = HomeView(app_driver)
        assert self.home.validate_Home_page() is True
        # sleep(10)
