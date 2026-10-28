# Sistema de Inventario Interactivo (Google Colab)

Este proyecto es un sistema básico de gestión de inventario adaptado para ejecutarse nativamente en Google Colab. Utiliza `ipywidgets` para renderizar una interfaz gráfica directamente en la celda de ejecución, permitiendo gestionar productos sin depender de ventanas de escritorio.

## Características
- **Interfaz Integrada:** Formularios, botones y tablas dinámicas HTML directamente dentro del cuaderno.
- **Gestión de Stock:** Capacidad para agregar, eliminar y registrar la venta de productos en tiempo real.
- **Exportación en la Nube:** Generación y descarga automática de reportes de inventario en formato `.csv` utilizando `google.colab.files`.
- **Código Estandarizado:** Variables y métodos estructurados bajo la convención `camelCase`.

## Tecnologías Utilizadas
- Python 3
- Google Colab
- `ipywidgets` & `IPython.display`
- Módulo nativo `csv`

## Uso
1. Abre un nuevo cuaderno en Google Colab.
2. Pega el script principal en una celda.
3. Ejecuta la celda para desplegar la interfaz gráfica interactiva y comenzar a gestionar el inventario.
