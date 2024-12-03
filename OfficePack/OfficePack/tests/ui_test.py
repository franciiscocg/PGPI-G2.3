import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase

class UITests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-offline-load-stale-cache")
        chrome_options.add_argument("--disk-cache-size=0")
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_realizar_pedido(self):
        self.driver.get(f'{self.live_server_url}/catalogo/')
        self.driver.find_element(By.CSS_SELECTOR, ".product-item:nth-child(1) button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".product-item:nth-child(2) button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".product-item:nth-child(3) button").click()
        self.driver.find_element(By.LINK_TEXT, "🗑").click()
        self.driver.find_element(By.LINK_TEXT, "Ver cesta").click()
        self.driver.find_element(By.LINK_TEXT, "Realizar Pedido").click()
        self.driver.find_element(By.ID, "direccion").click()
        self.driver.find_element(By.ID, "direccion").send_keys("Calle Random, 25")
        self.driver.switch_to.frame(1)
        self.driver.find_element(By.NAME, "cardnumber").click()
        self.driver.find_element(By.NAME, "cardnumber").send_keys("4242 4242 4242 4242")
        self.driver.find_element(By.NAME, "exp-date").send_keys("12 / 34")
        self.driver.find_element(By.NAME, "cvc").send_keys("556")
        self.driver.find_element(By.NAME, "postal").send_keys("41010")
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, "submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Rastrear Pedido").click()
        self.driver.find_element(By.ID, "pedido_id").click()
        self.driver.find_element(By.ID, "pedido_id").send_keys("6")
        self.driver.find_element(By.CSS_SELECTOR, "button").click()

if __name__ == '__main__':
    unittest.main()