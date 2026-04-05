\# QA Project Urban Routes



\## Descripción

El objetivo de este proyecto se centra en la automatización para la entrada de datos al pedir un taxi en la aplicación Urban Routes.



\##Estructura del proyecto

* ´main.py´ - archivo principal con las pruebas
* ´data.py´ - Datos de prueba (Direcciones, numero de teléfono y datos de tarjeta)



\## Tecnologías utilizadas

* Python
* pytest



\##Pre-requisitos

* Python 3.x
* pip install selenium
* pip install pytest
* ChomeDriver instalado



\## Ejecución de pruebas

Para ejecutar las pruebas utiliza el siguiente comando en la terminal
pytest main.py



\##Casos de prueba incluidos

* Establecer dirección de origen y destino
* Seleccionar Pedir taxi en "Flash"
* Seleccionar la tarifa comfort
* Añadir un número telefónico
* Introducir el método de pago (tarjeta)
* Añadir un mensaje para el conductor
* Pedir manta y pañuelos
* Pedir 2 helados
* Pedir taxi y esperar la asignación

