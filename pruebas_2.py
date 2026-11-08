"""
Proyecto: Sistema Integral de Gestion - Software FJ
Curso: Programacion - Fase 4 (UNAD)

Proposito:
Demostrar programacion orientada a objetos y manejo de excepciones
mediante la gestion simulada de clientes, servicios y reservas.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------
# 1. Excepciones personalizadas del proyecto
# ---------------------------------------------------------------------

class ErrorSoftwareFJ(Exception):
    """Excepcion base para los errores propios de Software FJ."""


class ClienteNoValidoError(ErrorSoftwareFJ):
    """Se genera cuando los datos de un cliente no son validos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se genera cuando se intenta reservar un servicio inactivo."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se genera cuando una reserva no cumple las condiciones."""


# ---------------------------------------------------------------------
# 2. Registro de eventos y errores
# ---------------------------------------------------------------------

def registrar_log(tipo, mensaje):
    """Guarda los eventos del sistema en sistema_log.txt."""
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{hora_actual}] [{tipo.upper()}] -> {mensaje}\n"

    try:
        with open("sistema_log.txt", "a", encoding="utf-8") as archivo:
            archivo.write(linea_log)
    except OSError as error:
        # Un problema al escribir el log no debe ocultar el error original.
        print(f"[AVISO] No se pudo escribir en el archivo de registro: {error}")


# ---------------------------------------------------------------------
# 3. Clase abstracta y clase Cliente
# ---------------------------------------------------------------------

class EntidadBase(ABC):
    """Define el metodo que deben implementar las entidades del sistema."""

    @abstractmethod
    def obtener_detalles(self):
        """Devuelve una descripcion de la entidad."""
        raise NotImplementedError


class Cliente(EntidadBase):
    """Representa a un cliente y valida sus datos basicos."""

    def __init__(self, id_cliente, nombre, correo, telefono):
        self.__id_cliente = str(id_cliente).strip()
        self.__nombre = str(nombre).strip()
        self.__correo = str(correo).strip()
        self.__telefono = str(telefono).strip()
        self.__validar_datos_cliente()

    def __validar_datos_cliente(self):
        """Comprueba que los datos obligatorios del cliente sean validos."""
        if not self.__id_cliente or not self.__nombre:
            registrar_log("ERROR", "Cliente rechazado: falta el ID o el nombre.")
            raise ClienteNoValidoError(
                "El ID y el nombre del cliente son obligatorios."
            )

        if "@" not in self.__correo or "." not in self.__correo.split("@")[-1]:
            registrar_log(
                "ERROR",
                f"Cliente rechazado: correo invalido para {self.__nombre}."
            )
            raise ClienteNoValidoError(
                "El correo debe tener un formato valido, por ejemplo nombre@dominio.com."
            )

        if not self.__telefono.isdigit() or len(self.__telefono) < 7:
            registrar_log(
                "ERROR",
                f"Cliente rechazado: telefono invalido para {self.__nombre}."
            )
            raise ClienteNoValidoError(
                "El telefono debe contener al menos 7 digitos."
            )

    def obtener_detalles(self):
        """Devuelve los datos principales del cliente."""
        return (
            f"Cliente: {self.__nombre} (ID: {self.__id_cliente}) | "
            f"Correo: {self.__correo}"
        )

    @property
    def nombre(self):
        """Permite consultar el nombre sin exponer el atributo privado."""
        return self.__nombre


# ---------------------------------------------------------------------
# 4. Clase abstracta Servicio y sus clases especializadas
# ---------------------------------------------------------------------

class Servicio(ABC):
    """Clase base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo, nombre_servicio, tarifa_base):
        if not codigo or not nombre_servicio:
            raise ValueError("El codigo y el nombre del servicio son obligatorios.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base < 0:
            raise ValueError("La tarifa base debe ser un numero igual o mayor que cero.")

        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = float(tarifa_base)
        self.disponible = True

    @abstractmethod
    def calcular_costo(self):
        """Calcula el costo segun el tipo de servicio."""
        raise NotImplementedError

    def obtener_detalles(self):
        """Devuelve la informacion general del servicio."""
        estado = "Activo" if self.disponible else "Inactivo"
        return (
            f"[{self.codigo}] {self.nombre_servicio} - "
            f"Tarifa base: ${self.tarifa_base:.2f} ({estado})"
        )


class ReservaSalas(Servicio):
    """Servicio de reserva de salas por horas."""

    def __init__(self, codigo, tarifa_base, capacidad):
        super().__init__(codigo, "Reserva de Salas", tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def calcular_costo(self, horas=1, descuento=False):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas de reserva deben ser mayores que cero.")

        total = self.tarifa_base * horas
        if descuento:
            total *= 0.90
        return round(total, 2)


class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos por dias."""

    def __init__(self, codigo, tarifa_base, tipo_equipo):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        if not tipo_equipo:
            raise ValueError("Debe indicar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias=1, incluir_seguro=False):
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise ValueError("Los dias de alquiler deben ser mayores que cero.")

        total = self.tarifa_base * dias
        if incluir_seguro:
            total += 20.0
        return round(total, 2)


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria cobrado por numero de sesiones."""

    def __init__(self, codigo, tarifa_base, area):
        super().__init__(codigo, "Asesoria Especializada", tarifa_base)
        if not area:
            raise ValueError("Debe indicar el area de la asesoria.")
        self.area = area

    def calcular_costo(self, sesiones=1):
        if not isinstance(sesiones, (int, float)) or sesiones <= 0:
            raise ValueError("El numero de sesiones debe ser mayor que cero.")
        return round(self.tarifa_base * sesiones, 2)


# ---------------------------------------------------------------------
# 5. Clase Reserva: relaciona un cliente con un servicio
# ---------------------------------------------------------------------

class Reserva:
    """Representa y procesa una reserva."""

    def __init__(self, id_reserva, cliente, servicio, tiempo_cantidad):
        if not id_reserva:
            raise ReservaInvalidaError("La reserva debe tener un identificador.")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe estar asociada a un cliente valido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe estar asociada a un servicio valido.")

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.tiempo_cantidad = tiempo_cantidad
        self.estado = "Pendiente"
        self.costo_final = 0.0

    def procesar_reserva(self):
        """Procesa la reserva y controla los errores que puedan presentarse."""
        try:
            registrar_log(
                "INFO",
                f"Iniciando tramite de reserva ID: {self.id_reserva}."
            )

            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre_servicio}' esta inactivo."
                )

            if isinstance(self.servicio, ReservaSalas):
                costo = self.servicio.calcular_costo(
                    horas=self.tiempo_cantidad,
                    descuento=True
                )
            elif isinstance(self.servicio, AlquilerEquipos):
                costo = self.servicio.calcular_costo(
                    dias=self.tiempo_cantidad,
                    incluir_seguro=True
                )
            elif isinstance(self.servicio, AsesoriaEspecializada):
                costo = self.servicio.calcular_costo(
                    sesiones=self.tiempo_cantidad
                )
            else:
                raise ReservaInvalidaError("El tipo de servicio no es reconocido.")

            self.costo_final = costo

        except (ServicioNoDisponibleError, ReservaInvalidaError, ValueError) as error:
            self.estado = "Fallida"
            registrar_log(
                "ADVERTENCIA",
                f"Reserva {self.id_reserva} rechazada: {error}"
            )
            print(f"   [CONTROLADO] No se pudo realizar la reserva: {error}")

        except Exception as error:
            self.estado = "Error critico"
            registrar_log(
                "CRITICO",
                f"Falla inesperada en reserva {self.id_reserva}: {error}"
            )
            raise RuntimeError(
                "Ocurrio un error inesperado al procesar la reserva."
            ) from error

        else:
            self.estado = "Confirmada"
            registrar_log(
                "EXITO",
                f"Reserva {self.id_reserva} confirmada. Total: ${self.costo_final:.2f}"
            )
            print(
                f"   [EXITO] Reserva confirmada para {self.cliente.nombre}. "
                f"Total: ${self.costo_final:.2f}"
            )

        finally:
            registrar_log(
                "INFO",
                f"Finalizo el proceso de la reserva {self.id_reserva}."
            )


# ---------------------------------------------------------------------
# 6. Simulacion de las 10 operaciones solicitadas para el proyecto
# ---------------------------------------------------------------------

def simular_operaciones_software_fj():
    """Ejecuta diez operaciones para demostrar el funcionamiento del sistema."""
    print("=" * 65)
    print("SIMULACION DE OPERACIONES - SOFTWARE FJ")
    print("=" * 65)

    registrar_log("INICIO", "Comenzo la simulacion de las 10 operaciones.")

    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # Operacion 1: registrar un cliente con datos validos.
    print("\nOperacion 1: Registro correcto de cliente")
    try:
        cliente = Cliente(
            "CLI-01",
            "Daniel Mendoza",
            "daniel.mendoza@unad.edu.co",
            "3001112233"
        )
        lista_clientes.append(cliente)
        print(f"   [EXITO] {cliente.obtener_detalles()}")
    except ClienteNoValidoError as error:
        print(f"   [ERROR CONTROLADO] {error}")

    # Operacion 2: intentar registrar un cliente con correo invalido.
    print("\nOperacion 2: Registro de cliente con correo invalido")
    try:
        cliente_invalido = Cliente(
            "CLI-02",
            "Maria Perez",
            "correosinconsignar",
            "3112223344"
        )
        lista_clientes.append(cliente_invalido)
    except ClienteNoValidoError as error:
        print(f"   [EXCEPCION CAPTURADA] {error}")

    # Operacion 3: crear un servicio de reserva de salas.
    print("\nOperacion 3: Creacion del servicio de salas")
    sala = ReservaSalas("SRV-10", 45.0, capacidad=15)
    lista_servicios.append(sala)
    print(f"   {sala.obtener_detalles()}")

    # Operacion 4: crear un servicio de alquiler de equipos.
    print("\nOperacion 4: Creacion del servicio de alquiler de equipos")
    equipos = AlquilerEquipos("SRV-20", 25.0, tipo_equipo="Kit de Redes Cisco")
    lista_servicios.append(equipos)
    print(f"   {equipos.obtener_detalles()}")

    # Operacion 5: crear un servicio de asesoria especializada.
    print("\nOperacion 5: Creacion del servicio de asesoria")
    asesoria = AsesoriaEspecializada(
        "SRV-30",
        60.0,
        area="Ingenieria de Telecomunicaciones"
    )
    lista_servicios.append(asesoria)
    print(f"   {asesoria.obtener_detalles()}")

    # Operacion 6: procesar una reserva valida de sala.
    print("\nOperacion 6: Reserva exitosa de sala")
    reserva_1 = Reserva("RES-001", lista_clientes[0], sala, tiempo_cantidad=3)
    lista_reservas.append(reserva_1)
    reserva_1.procesar_reserva()

    # Operacion 7: procesar una reserva valida de equipos.
    print("\nOperacion 7: Reserva exitosa de equipos")
    reserva_2 = Reserva("RES-002", lista_clientes[0], equipos, tiempo_cantidad=4)
    lista_reservas.append(reserva_2)
    reserva_2.procesar_reserva()

    # Operacion 8: intentar reservar un servicio que esta inactivo.
    print("\nOperacion 8: Intento de reserva de un servicio inactivo")
    asesoria.disponible = False
    reserva_3 = Reserva("RES-003", lista_clientes[0], asesoria, tiempo_cantidad=2)
    lista_reservas.append(reserva_3)
    reserva_3.procesar_reserva()

    # Operacion 9: provocar y capturar un error por cantidad negativa.
    print("\nOperacion 9: Validacion de cantidad negativa")
    try:
        sala.calcular_costo(horas=-4)
    except ValueError as error:
        print(f"   [EXCEPCION CAPTURADA] {error}")
        registrar_log("ERROR", f"Calculo rechazado por cantidad invalida: {error}")

    # Operacion 10: reactivar la asesoria y procesar una nueva reserva.
    print("\nOperacion 10: Reactivacion de asesoria y reserva final")
    asesoria.disponible = True
    reserva_4 = Reserva("RES-004", lista_clientes[0], asesoria, tiempo_cantidad=2)
    lista_reservas.append(reserva_4)
    reserva_4.procesar_reserva()

    print("\n" + "=" * 65)
    print("RESUMEN DE LA SIMULACION")
    print("=" * 65)
    print(f"Clientes registrados: {len(lista_clientes)}")
    print(f"Servicios creados: {len(lista_servicios)}")
    print(f"Reservas procesadas: {len(lista_reservas)}")
    print(f"Reservas confirmadas: {sum(r.estado == 'Confirmada' for r in lista_reservas)}")
    print(f"Reservas fallidas: {sum(r.estado == 'Fallida' for r in lista_reservas)}")
    print("La simulacion termino. Revisa el archivo sistema_log.txt.")

    registrar_log("FIN", "Termino la simulacion de las 10 operaciones.")


# Punto de entrada: ejecuta la simulacion al iniciar este archivo.
if __name__ == "__main__":
    simular_operaciones_software_fj()
