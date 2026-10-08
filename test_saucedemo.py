import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuración para SauceDemo ---
BASE_URL = "https://www.saucedemo.com"
USUARIO = "standard_user"
CLAVE = "secret_sauce"

PRODUCTO = (By.CSS_SELECTOR, ".inventory_item")
NOMBRE_PRODUCTO = (By.CSS_SELECTOR, ".inventory_item_name")
BOTON_AGREGAR = (By.CSS_SELECTOR, "button.btn_inventory")
CONTADOR_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")
ENLACE_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link")
ITEM_CARRITO = (By.CSS_SELECTOR, ".cart_item")
NOMBRE_ITEM_CARRITO = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    yield drv
    drv.quit()


def login(driver, wait):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(USUARIO)
    driver.find_element(By.ID, "password").send_keys(CLAVE)
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory"))


def test_agregar_primer_producto_y_verificar_en_carrito(driver):
    wait = WebDriverWait(driver, 10)
    login(driver, wait)

    # 1. Agregar el primer producto
    primer_producto = wait.until(EC.presence_of_all_elements_located(PRODUCTO))[0]
    nombre_esperado = primer_producto.find_element(*NOMBRE_PRODUCTO).text.strip()
    primer_producto.find_element(*BOTON_AGREGAR).click()

    # 2. Verificar que el contador se incrementa
    wait.until(EC.text_to_be_present_in_element(CONTADOR_CARRITO, "1"))
    assert driver.find_element(*CONTADOR_CARRITO).text.strip() == "1"

    # 3. Navegar al carrito
    driver.find_element(*ENLACE_CARRITO).click()
    wait.until(EC.url_contains("cart"))

    # 4. Verificar el ítem en el carrito
    items = wait.until(EC.presence_of_all_elements_located(ITEM_CARRITO))
    assert len(items) == 1
    assert driver.find_element(*NOMBRE_ITEM_CARRITO).text.strip() == nombre_esperado
