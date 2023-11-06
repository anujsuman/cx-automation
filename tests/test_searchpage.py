import pytest
from pages.SearchPage import SearchView
from utilities.WiremockClient import WiremockClient
import config
from time import sleep


# Test functions using the Appium server fixture and driver
class TestSearchPage:
    @pytest.fixture(autouse=True, scope="class")
    def classSetup(self, app_driver):
        num = config.PHONE_NUMBER
        self.driver = app_driver
        self.wc = WiremockClient()
        self.search = SearchView(self.driver)

        self.wc.stop_recording()
        sleep(2)
        self.wc.delete_all_mapping()
        sleep(2)
        self.wc.start_recording()
        sleep(2)
        self.search.add_wiremock_mappings()
        self.wc.delete_all_request(None)

        self.search.enter_number(num) 
        self.search.verify_getotp(num)  
        self.search.click_getOtp() 
        sleep(10)
        self.search.clickSearchBar()
        sleep(2)
        # self.search.scroll_horizontal_screen()

    # def test_search_bar(self,app_driver):
    #     self.search = SearchView(app_driver)
    #     self.search.clickSearchBar()

    # def test_click_trending_item(self,app_driver):
    #     self.search = SearchView(app_driver)
    #     self.search.click_Trending()

    # def test_scroll_horizontal_screen(self,app_driver):
    #     self.search = SearchView(app_driver)
    #     self.search.scroll_horizontal_screen()

    def test_validate_pdp_sku_impression(self, app_driver):
        self.search = SearchView(app_driver)
        self.search.scroll_horizontal_screen()
        assert self.search.verify_skus() is True
    
    def test_verify_search_skus(self,app_driver):
        self.search=SearchView(app_driver)
        search_cat = 'Oil'
        self.search.enter_search_product(search_cat)
        self.search.back_button()
        assert self.search.verify_search_skus() is True 
