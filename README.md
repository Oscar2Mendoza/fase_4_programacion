# Sistema Integral de Gestion - Software FJ

Proyecto desarrollado para el componente practico (Fase 4 - Practicas simuladas) del curso de Programacion (Codigo: 213023) de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripcion del Proyecto

El sistema es una solucion de software orientada a objetos desarrollada en Python que simula la gestion integral de **clientes, servicios y reservas** para la empresa *Software FJ*.
La aplicacion opera sin motores de base de datos relacionales o no relacionales; toda la persistencia temporal de datos se maneja mediante estructuras en memoria (objetos y listas internas), 
complementada con un sistema robusto de registro de eventos y errores en archivos de texto plano (logs).

## Arquitectura y Principios de POO aplicados

El codigo implementa de manera rigurosa los pilares de la Programacion Orientada a Objetos y patrones de estabilidad exigidos en la guia de actividades:

* Clases Abstractas: Uso de la libreria `abc` para definir contratos base (`EntidadBase` y `Servicio`).
* Herencia y Polimorfismo: Clases especializadas que heredan de `Servicio` (`ReservaSalas`, `AlquilerEquipos`, `AsesoriaEspecializada`) implementando sus propios calculos de costos.
* Encapsulacion: Atributos privados y propiedades protegidas en la clase `Cliente` para asegurar la integridad de los datos personales.
* Manejo Avanzado de Excepciones: Estructuras robustas utilizando bloques `try / except / else / finally`, excepciones personalizadas (`ErrorSoftwareFJ`,
  `ClienteNoValidoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`)
  y encadenamiento de errores para mantener la aplicacion estable ante fallos operativos.
* Sistema de Logs: Registro automatico de eventos, advertencias y errores criticos en el archivo `sistema_log.txt` con marca de tiempo.

## Estructura del Repositorio

* `pruebas_2.py` (o `main.py`): Archivo principal que contiene todo el modelo de clases, la logica de negocio y la ejecucion de la simulacion.
* `sistema_log.txt`: Archivo de bitacora generado automaticamente durante la ejecucion del programa para auditar eventos y excepciones.

## Requisitos del Sistema

* Python: Version 3.8 o superior instalada en el equipo.
* No requiere la instalacion de librerias externas o de terceros (utiliza unicamente modulos nativos: `abc` y `datetime`).

## Instrucciones de Ejecucion

1. Clona este repositorio o descarga el codigo fuente en tu equipo:
   ```bash
   git clone <enlace-del-repositorio>
