# Pruebas automatizadas del carrito de compras - SauceDemo

## Propósito del proyecto

Automatizar con Selenium el flujo básico del carrito de compras de [SauceDemo](https://www.saucedemo.com), un sitio de práctica para pruebas de QA.

El caso de prueba cubre:

1. Iniciar sesión con un usuario válido.
2. Agregar el primer producto al carrito.
3. Verificar que el contador del carrito se incremente a `1`.
4. Navegar al carrito de compras.
5. Comprobar que el producto agregado aparezca en el carrito.

## Tecnologías utilizadas

- **Python 3.9+**
- **Selenium WebDriver**: automatización del navegador
- **Pytest**: framework de pruebas
- **pytest-html**: generación de reportes en HTML
- **Google Chrome**: navegador usado en las pruebas

## Estructura del proyecto

```
.
├── README.md
├── requirements.txt
└── pre-entrega-final/
    └── test_saucedemo.py
```

## Instalación de dependencias

1. Clonar o descargar el proyecto y ubicarse en la carpeta raíz.
2. (Recomendado) Crear y activar un entorno virtual:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

> Requisito: tener Google Chrome instalado. Con Selenium 4.6 o superior, el driver del navegador se descarga automáticamente.

## Ejecución de las pruebas

Desde la carpeta raíz del proyecto:

```bash
pytest pre-entrega-final/test_saucedemo.py -v
```

## Reporte en HTML

Para ejecutar las pruebas y generar el reporte:

```bash
pytest pre-entrega-final/test_saucedemo.py -v --html=reporte.html
```

Al finalizar se crea el archivo `reporte.html` en la carpeta raíz. Se puede abrir con cualquier navegador para ver el resultado de cada prueba.

## Datos de prueba

SauceDemo ofrece credenciales públicas para práctica:

| Usuario         | Contraseña     |
|-----------------|----------------|
| `standard_user` | `secret_sauce` |
