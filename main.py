import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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
    close_btn = (By.CSS_SELECTOR, "div.payment-picker.open div.modal div.section.active button.close-button.section-close")
    comment = (By.ID, "comment")
    slider_round_mant = (By.XPATH,"//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']//span[@class='slider round']")
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

    def send_comment(self):
        message = "Traiga un aperitivo"
        comment_field = self.driver.find_element(*self.comment)
        comment_field.send_keys(message)

    def select_request(self):
        element = self.driver.find_element(*self.slider_round_mant)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.find_element(*self.slider_round_mant).click()
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






class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
        #capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        #cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
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
        routes_page.wait_for_element(routes_page.button_round)
        routes_page.click_take_taxi()
        routes_page.wait_for_element(routes_page.btn_comfort)
        routes_page.select_comfort()
        routes_page.click_btn_number()
        routes_page.wait_for_element(routes_page.set_number)
        routes_page.send_number()
        routes_page.get_code()
        routes_page.set_debit_card()
        routes_page.send_comment()
        routes_page.select_request()
        routes_page.order_gelato()
        routes_page.wait_driver()

        time.sleep(5)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()