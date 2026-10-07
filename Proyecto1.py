"""
Automatización de login en https://www.saucedemo.com
Requisitos:  pip install selenium pytest
Ejecución:   pytest -v test_login_saucedemo.py
             (o: python test_login_saucedemo.py)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
TIMEOUT = 10  # segundos para las esperas explícitas


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # descomentar para CI
    drv = webdriver.Chrome(options=options)  # Selenium Manager gestiona el driver
    yield drv
    drv.quit()


def test_login_exitoso(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    # 1. Navegar a la página de login
    driver.get(BASE_URL)

    # 2. Ingresar credenciales válidas (esperas explícitas)
    user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user_input.clear()
    user_input.send_keys(USERNAME)

    pass_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    pass_input.clear()
    pass_input.send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    # 3. Validar redirección a la página de inventario
    wait.until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url, (
        f"URL inesperada tras el login: {driver.current_url}"
    )

    # 4. Validar textos "Swag Labs" (logo del header) y "Products" (título de la página)
    logo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "app_logo")))
    assert logo.text == "Swag Labs", f"Logo inesperado: {logo.text!r}"

    title = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']"))
    )
    assert title.text == "Products", f"Título inesperado: {title.text!r}"

    # Verificación extra: el contenedor de productos está presente
    wait.until(EC.visibility_of_element_located((By.ID, "inventory_container")))


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-v", __file__]))