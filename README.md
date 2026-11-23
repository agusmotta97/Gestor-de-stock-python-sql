

# Gestor de Stock y Alertas de Reposición (Python + SQLite)

Sistema de control de inventario por consola desarrollado en **Python** y **SQLite** para administrar entradas y salidas de mercadería, prevenir quiebres de stock y generar reportes automáticos de reposición.

## Problema comercial que resuelve
En comercios, depósitos y operaciones de distribución, llevar el inventario sin validaciones automáticas provoca dos pérdidas directas: vender mercadería sin disponibilidad física (stock negativo) y quedarse sin artículos de alta rotación por falta de alertas tempranas. Este sistema centraliza el control de unidades y calcula sugerencias de compra según el punto de pedido de cada producto.

## Funcionalidades principales
* **Inventario en tiempo real:** Muestra el listado completo de productos con su stock actual, stock mínimo definido y estado operativo (`OK` o `REPONER URGENTE`).
* **Registro de ventas con validación de negocio:** Descuenta unidades al registrar una salida y bloquea la operación automáticamente si la cantidad solicitada supera el stock disponible.
* **Ingreso de mercadería:** Permite sumar unidades al inventario cuando se recibe mercadería de proveedores.
* **Reporte de alertas de reposición:** Filtra mediante consulta SQL (`WHERE stock_actual <= stock_minimo`) los artículos en estado crítico y sugiere la cantidad exacta a pedir para recuperar margen operativo.
* **Control de errores:** Implementación de bloques `try / except` para manejar ingresos inválidos (`ValueError`) y excepciones de base de datos (`sqlite3.Error`) sin interrumpir la ejecución.

## Estructura de la Base de Datos
El sistema crea y gestiona la base de datos local `inventario_stock.db` con la siguiente tabla:

| Campo | Tipo de dato | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Identificador único del producto |
| `nombre` | `TEXT` | `NOT NULL` | Descripción del artículo |
| `stock_actual` | `INTEGER` | `NOT NULL` | Cantidad física disponible en depósito |
| `stock_minimo` | `INTEGER` | `NOT NULL` | Punto de pedido que dispara la alerta de compra |

## Tecnologías y buenas prácticas aplicadas
* **Lenguaje:** Python 3
* **Base de datos:** SQLite3 (librería estándar `sqlite3`)
* **Seguridad:** Consultas SQL parametrizadas (`?`) para evitar inyección SQL.
* **Arquitectura:** Programación estructurada modular con control de flujo mediante variables bandera.

## Cómo ejecutar el proyecto
1. Asegurate de tener instalado **Python 3** en tu computadora.
2. Descargá o cloná este repositorio.
3. Abrí una terminal en la carpeta del proyecto y ejecutá:
   ```bash
   python actualizar-stock.py
   ```
