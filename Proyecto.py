"""
Caso de prueba de navegación: página de inventario de https://www.saucedemo.com
Requisitos:  pip install selenium pytest
Ejecución:   pytest -v -s test_inventory_navegacion.py
             (-s permite ver en consola el nombre/precio del primer producto)
"""
import re

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
TIMEOUT = 10


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # descomentar para CI
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, TIMEOUT)


@pytest.fixture
def inventory_page(driver, wait):
    """Precondición: login exitoso y página de inventario cargada."""
    driver.get(BASE_URL)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(USERNAME)
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
    wait.until(EC.url_contains("/inventory.html"))
    return driver


def test_titulo_pagina_inventario(inventory_page, wait):
    driver = inventory_page

    # Título de la pestaña del navegador
    wait.until(EC.title_is("Swag Labs"))
    assert driver.title == "Swag Labs", f"Título de pestaña inesperado: {driver.title!r}"

    # Título visible de la sección
    title = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']"))
    )
    assert title.text == "Products", f"Título de sección inesperado: {title.text!r}"


def test_productos_visibles_y_primer_producto(inventory_page, wait):
    driver = inventory_page

    # Espera a que haya al menos un producto visible
    first_item = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='inventory-item']"))
    )
    items = driver.find_elements(By.CSS_SELECTOR, "[data-test='inventory-item']")
    assert len(items) >= 1, "No se encontraron productos en la página"
    print(f"\nProductos encontrados: {len(items)}")

    # Nombre y precio del primer producto
    name = first_item.find_element(By.CSS_SELECTOR, "[data-test='inventory-item-name']").text
    price = first_item.find_element(By.CSS_SELECTOR, "[data-test='inventory-item-price']").text

    assert name.strip(), "El nombre del primer producto está vacío"
    assert re.fullmatch(r"\$\d+\.\d{2}", price), f"Formato de precio inesperado: {price!r}"

    print(f"Primer producto -> Nombre: {name} | Precio: {price}")


def test_elementos_interfaz_presentes(inventory_page, wait):
    driver = inventory_page

    elementos = {
        "Menú hamburguesa": (By.ID, "react-burger-menu-btn"),
        "Logo Swag Labs": (By.CLASS_NAME, "app_logo"),
        "Carrito": (By.CSS_SELECTOR, "[data-test='shopping-cart-link']"),
        "Filtro de ordenamiento": (By.CSS_SELECTOR, "[data-test='product-sort-container']"),
        "Contenedor de productos": (By.ID, "inventory_container"),
        "Footer": (By.CSS_SELECTOR, "[data-test='footer']"),
    }

    for nombre, locator in elementos.items():
        elemento = wait.until(
            EC.visibility_of_element_located(locator),
            message=f"No se encontró visible: {nombre}",
        )
        assert elemento.is_displayed(), f"{nombre} no está visible"

    # El filtro debe ofrecer opciones de ordenamiento
    opciones = driver.find_elements(
        By.CSS_SELECTOR, "[data-test='product-sort-container'] option"
    )
    assert len(opciones) >= 4, f"Se esperaban >= 4 opciones de orden, hay {len(opciones)}"

    # El menú se despliega al hacer clic
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    wait.until(EC.visibility_of_element_located((By.ID, "logout_sidebar_link")))


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-v", "-s", __file__]))