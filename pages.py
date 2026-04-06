import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_round = (By.XPATH, "//button[@class = 'button round']")
    btn_comfort = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    btn_number = (By.XPATH, "//div[@class = 'np-text' and text() = 'Número de teléfono']")
    set_number = (By.ID, 'phone')
    btn_next = (By.XPATH, "//div[@class = 'section active']//button[@type = 'submit']")
    code_msm = (By.ID, "code")
    button_confirm = (By.XPATH, "//button[text()='Confirmar']")
    btn_method_pay = (By.CLASS_NAME, "pp-text")
    btn_add_card = (By.CSS_SELECTOR, "div.pp-row.disabled")
    fill_number_card = (By.ID, 'number')
    fill_number_code = (By.ID, 'code')
    btn_AGREGAR = (By.XPATH, "//button[text()='Agregar']")
    card_checkbox = (By.ID, "card-1")
    close_btn = (By.CSS_SELECTOR, "div.payment-picker.open div.modal div.section.active button.close-button.section-close")
    comment = (By.ID, "comment")
    slider_round_mant = (By.XPATH,"//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']//span[@class='slider round']")
    checkbox_mant = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div//input[@type='checkbox']")
    counter_value = (By.XPATH,"//div[contains(., 'Helado') and @class='r-counter-container']//div[@class='counter-value']")
    counter_plus = (By.XPATH,"//div[contains(., 'Helado') and @class='r-counter-container']//div[@class='counter-plus']")
    btn_get_taxi = (By.CLASS_NAME, "smart-button-main")
    flag_driver = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'Buscar automóvil')]")


    def __init__(self, driver):
        self.driver = driver
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)
#Para validar que estén bien escritos
    def wait_for_element(self, locator,timeout=10):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.visibility_of_element_located(locator))
    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable(locator))
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')
    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
    def click_take_taxi(self):
        self.driver.find_element(*self.button_round).click()
    def select_comfort(self):
        self.driver.find_element(*self.btn_comfort).click()
    def click_btn_number(self):
        self.driver.find_element(*self.btn_number).click()
    def send_number(self):
        self.driver.find_element(*self.set_number).send_keys(data.phone_number)
        self.driver.find_element(*self.btn_next).click()
    def get_code(self):
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.code_msm).send_keys(code)
        self.wait_for_element(self.button_confirm)
        self.driver.find_element(*self.button_confirm).click()

    def set_debit_card(self):
        self.driver.find_element(*self.btn_method_pay).click()
        self.wait_for_element(self.btn_add_card)
        self.driver.find_element(*self.btn_add_card).click()

        card_field = self.driver.find_element(*self.fill_number_card)
        card_field.send_keys(data.card_number)
        card_field.send_keys(Keys.TAB+data.card_code+Keys.TAB)

        self.wait_clickable(self.btn_AGREGAR).click()
        self.wait_for_element(self.close_btn).click()

    def is_card_selected(self):
        return self.driver.find_element(*self.card_checkbox).is_selected()

    def send_comment(self):
        comment_field = self.driver.find_element(*self.comment)
        comment_field.send_keys(data.message_for_driver)


    def select_request(self):
        element = self.driver.find_element(*self.slider_round_mant)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.find_element(*self.slider_round_mant).click()

    def toggle_blanket_selected(self):
        checkbox = self.driver.find_element(*self.checkbox_mant)
        return checkbox.is_selected()

    def initial_count_gelato(self):
        cnt = self.driver.find_element(*self.counter_value).text
        counter = int(cnt)
        return counter

    def order_gelato(self):
        while True:
            cnt = self.driver.find_element(*self.counter_value).text
            counter = int(cnt)

            if counter == 2:
                break
            self.driver.find_element(*self.counter_plus).click()

    def wait_driver(self):
        self.driver.find_element(*self.btn_get_taxi).click()
        WebDriverWait(self.driver, 50).until_not(expected_conditions.visibility_of_element_located(self.flag_driver))
