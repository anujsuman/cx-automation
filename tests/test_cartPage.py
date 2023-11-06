import pytest
from pages.LoginPage import LoginView
from utilities.WiremockClient import WiremockClient
import config
from time import sleep
from pages.CartPage import Cart
from pages.HomePage import HomeView


# Test functions using the Appium server fixture and driver
class TestCartPage:
    parent_id_you_may_like = "testid - 3161"
    parent_child_id_Skus = "testid - 3161 - CM0028758"

    # @pytest.fixture(autouse=True)
    # def classSetup(self, app_driver):
    #     num = config.PHONE_NUMBER
    #     self.driver = app_driver
    #     self.wc = WiremockClient()
    #     # self.wc.delete_all_mapping()
    #     # self.wc.save_mapping()
    #     self.wc.start_recording()
    #     self.wc.delete_all_request(None)
    #     self.login = LoginView(app_driver)
    #     # self.login.add_wiremock_mappings()
    #     self.login.enter_number(num)
    #     self.login.verify_getotp(num)
    #     self.login.click_getOtp()
    #     self.login.check_otp_screen()

    #     self.home = HomeView(app_driver)

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

    def test_skuList_cartPage(self, app_driver):
        self.cart = Cart(app_driver)
        self.cart.add_products_from_sku_list()
        self.cart.is_view_cart()
        sleep(7)
        self.cart.load_cart_list()
        sleep(2)
        self.cart.wishlist_popup_modal()
        self.cart.validate_wishlist_cms_data_for_cartPage()
        self.cart.press_back_button()
        sleep(2)
        self.cart.validate_you_may_like_cartPage()



