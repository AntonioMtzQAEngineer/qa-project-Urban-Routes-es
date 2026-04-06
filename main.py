import time
import data
from selenium import webdriver
from selenium.webdriver import Keys
from pages import UrbanRoutesPage
from selenium.webdriver.common.by import By

class TestUrbanRoutes:
    driver = None
    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_element(routes_page.from_field)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        time.sleep(5)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_fare(self):
        self.driver.get(data.urban_routes_url)
        select_comfort = UrbanRoutesPage(self.driver)

        select_comfort.wait_for_element(select_comfort.from_field)
        select_comfort.set_route(data.address_from, data.address_to)

        select_comfort.wait_for_element(select_comfort.button_round)
        select_comfort.click_take_taxi()
        select_comfort.wait_for_element(select_comfort.btn_comfort)
        select_comfort.select_comfort()
        assert select_comfort.wait_for_element(select_comfort.btn_comfort)

    def test_fill_phone(self):
        self.driver.get(data.urban_routes_url)
        fill_phone = UrbanRoutesPage(self.driver)

        fill_phone.wait_for_element(fill_phone.from_field)
        fill_phone.set_route(data.address_from, data.address_to)
        fill_phone.wait_for_element(fill_phone.button_round)
        fill_phone.click_take_taxi()
        fill_phone.wait_for_element(fill_phone.btn_comfort)
        fill_phone.select_comfort()

        fill_phone.click_btn_number()
        fill_phone.wait_for_element(fill_phone.set_number)
        fill_phone.send_number()
        fill_phone.get_code()
        phone_field = self.driver.find_element(*fill_phone.set_number)
        assert phone_field.get_attribute("value") == data.phone_number

    def test_set_card(self):
        self.driver.get(data.urban_routes_url)
        set_card = UrbanRoutesPage(self.driver)

        set_card.wait_for_element(set_card.from_field)
        set_card.set_route(data.address_from, data.address_to)
        set_card.wait_for_element(set_card.button_round)
        set_card.click_take_taxi()
        set_card.wait_for_element(set_card.btn_comfort)
        set_card.select_comfort()
        set_card.click_btn_number()
        set_card.wait_for_element(set_card.set_number)
        set_card.send_number()
        set_card.get_code()
        set_card.set_debit_card()

        assert set_card.is_card_selected()

    def test_send_message(self):
        self.driver.get(data.urban_routes_url)
        send_message = UrbanRoutesPage(self.driver)

        send_message.wait_for_element(send_message.from_field)
        send_message.set_route(data.address_from, data.address_to)
        send_message.wait_for_element(send_message.button_round)
        send_message.click_take_taxi()
        send_message.wait_for_element(send_message.btn_comfort)
        send_message.select_comfort()
        send_message.click_btn_number()
        send_message.wait_for_element(send_message.set_number)
        send_message.send_number()
        send_message.get_code()
        send_message.set_debit_card()
        send_message.send_comment()
        comment_value = self.driver.find_element(*send_message.comment)
        assert comment_value.get_attribute("value") == data.message_for_driver

    def test_select_request(self):
        self.driver.get(data.urban_routes_url)
        select_request = UrbanRoutesPage(self.driver)

        select_request.wait_for_element(select_request.from_field)
        select_request.set_route(data.address_from, data.address_to)
        select_request.wait_for_element(select_request.button_round)
        select_request.click_take_taxi()
        select_request.wait_for_element(select_request.btn_comfort)
        select_request.select_comfort()
        select_request.click_btn_number()
        select_request.wait_for_element(select_request.set_number)
        select_request.send_number()
        select_request.get_code()
        select_request.set_debit_card()
        select_request.send_comment()

        initial_value = select_request.toggle_blanket_selected()
        select_request.select_request()
        final_value = select_request.toggle_blanket_selected()
        assert initial_value != final_value

    def test_select_ice(self):
        self.driver.get(data.urban_routes_url)
        select_ice = UrbanRoutesPage(self.driver)
        select_ice.wait_for_element(select_ice.from_field)
        select_ice.set_route(data.address_from, data.address_to)
        select_ice.wait_for_element(select_ice.button_round)
        select_ice.click_take_taxi()
        select_ice.wait_for_element(select_ice.btn_comfort)
        select_ice.select_comfort()
        select_ice.click_btn_number()
        select_ice.wait_for_element(select_ice.set_number)
        select_ice.send_number()
        select_ice.get_code()
        select_ice.set_debit_card()
        select_ice.send_comment()
        select_ice.select_request()

        initial_count = select_ice.initial_count_gelato()
        select_ice.order_gelato()
        final_count = select_ice.initial_count_gelato()
        assert final_count == initial_count + 2

    def test_wait_driver(self):
        self.driver.get(data.urban_routes_url)
        wait_driver = UrbanRoutesPage(self.driver)
        wait_driver.wait_for_element(wait_driver.from_field)
        wait_driver.set_route(data.address_from, data.address_to)
        wait_driver.wait_for_element(wait_driver.button_round)
        wait_driver.click_take_taxi()
        wait_driver.wait_for_element(wait_driver.btn_comfort)
        wait_driver.select_comfort()
        wait_driver.click_btn_number()
        wait_driver.wait_for_element(wait_driver.set_number)
        wait_driver.send_number()
        wait_driver.get_code()
        wait_driver.set_debit_card()
        wait_driver.send_comment()
        wait_driver.select_request()
        wait_driver.order_gelato()

        wait_driver.wait_driver()
        driver_text = self.driver.find_element(By.XPATH, "//div[starts-with(text(), 'driver.name')]").text
        assert "driver.name" in driver_text

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()