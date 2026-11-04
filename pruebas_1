# Proyecto: Sistema Integral de Gestión - Software FJ (Fase 4)
# Curso: Programación (UNAD)

from abc import ABC, abstractmethod
import datetime


# Excepciones personalizadas para controlar las fallas del negocio
class ErrorSoftwareFJ(Exception):
    pass

class ClienteNoValidoError(ErrorSoftwareFJ):
    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    pass


# Función para registrar eventos y errores en un archivo de texto plano (logs)
def registrar_log(tipo, mensaje):
    hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{hora_actual}] [{tipo.upper()}] -> {mensaje}\n"
    try:
        with open("sistema_log.txt", "a", encoding="utf-8") as archivo:
            archivo.write(linea_log)
    except IOError as e:
        print(f"No se pudo escribir en el archivo de log: {e}")


# Clase abstracta general exigida por la guía
class EntidadBase(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass


# Clase Cliente con encapsulación (atributos privados) y validaciones
class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, correo, telefono):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.__validar_datos_cliente()

    def __validar_datos_cliente(self):
        if not self.__id_cliente or not self.__nombre:
            registrar_log("ERROR", "Intento fallido: Cliente sin ID o sin nombre.")
            raise ClienteNoValidoError("El ID y el nombre del cliente son obligatorios.")
        if "@" not in self.__correo:
            registrar_log("ERROR", f"Intento fallido: Correo inválido para {self.__nombre}.")
            raise ClienteNoValidoError("El correo electrónico debe llevar '@'.")

    def obtener_detalles(self):
        return f"Cliente: {self.__nombre} (ID: {self.__id_cliente}) | Correo: {self.__correo}"

    @property
    def nombre(self):
        return self.__nombre


# Clase abstracta Servicio
class Servicio(ABC):
    def __init__(self, codigo, nombre_servicio, tarifa_base):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self):
        pass

    def obtener_detalles(self):
        estado = "Activo" if self.disponible else "Inactivo"
        return f"[{self.codigo}] {self.nombre_servicio} - Tarifa base: ${self.tarifa_base} ({estado})"


# Servicios especializados que heredan de la clase Servicio
class ReservaSalas(Servicio):
    def __init__(self, codigo, tarifa_base, capacidad):
        super().__init__(codigo, "Reserva de Salas", tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas=1, descuento=False):
        if horas <= 0:
            raise ValueError("Las horas a reservar tienen que ser mayores a cero.")
        total = self.tarifa_base * horas
        if descuento:
            total = total * 0.90
        return round(total, 2)


class AlquilerEquipos(Servicio):
    def __init__(self, codigo, tarifa_base, tipo_equipo):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias=1, incluir_seguro=False):
        if dias <= 0:
            raise ValueError("Los días de alquiler deben ser mayores a cero.")
        total = self.tarifa_base * dias
        if incluir_seguro:
            total += 20.0
        return round(total, 2)


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, tarifa_base, area):
        super().__init__(codigo, "Asesoría Especializada", tarifa_base)
        self.area = area

    def calcular_costo(self, sesiones=1):
        if sesiones <= 0:
            raise ValueError("El número de sesiones de asesoría debe ser positivo.")
        return round(self.tarifa_base * sesiones, 2)


# Clase Reserva que une cliente, servicio y tiempos
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, tiempo_cantidad):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.tiempo_cantidad = tiempo_cantidad
        self.estado = "Pendiente"
        self.costo_final = 0.0

    def procesar_reserva(self):
        try:
            registrar_log("INFO", f"Iniciando trámite de reserva ID: {self.id_reserva}...")
            
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre_servicio}' está inactivo.")

            if isinstance(self.servicio, ReservaSalas):
                self.costo_final = self.servicio.calcular_costo(horas=self.tiempo_cantidad, descuento=True)
            elif isinstance(self.servicio, AlquilerEquipos):
                self.costo_final = self.servicio.calcular_costo(dias=self.tiempo_cantidad, incluir_seguro=True)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                self.costo_final = self.servicio.calcular_costo(sesiones=self.tiempo_cantidad)
            else:
                raise ReservaInvalidaError("Tipo de servicio no reconocido.")

        except (ServicioNoDisponibleError, ReservaInvalidaError) as error_controlado:
            self.estado = "Fallida"
            registrar_log("ADVERTENCIA", f"Reserva {self.id_reserva} rechazada: {error_controlado}")
            print(f"   [CONTROLADO] No se pudo hacer la reserva: {error_controlado}")

        except Exception as error_inesperado:
            self.estado = "Error Crítico"
            registrar_log("CRITICO", f"Falla inesperada en reserva {self.id_reserva}: {error_inesperado}")
            raise RuntimeError(f"Ocurrió un fallo no esperado en el sistema") from error_inesperado

        else:
            self.estado = "Confirmada"
            registrar_log("EXITO", f"Reserva {self.id_reserva} exitosa. Total a pagar: ${self.costo_final}")
            print(f"   [ÉXITO] Reserva confirmada para {self.cliente.nombre}. Total: ${self.costo_final}")

        finally:
            registrar_log("INFO", f"Cierre de ciclo para la reserva {self.id_reserva}.\n")


# Simulación de las 10 operaciones requeridas por la guía
def simular_operaciones_software_fj():
    print("Iniciando simulación de operaciones - Software FJ\n")
    registrar_log("INICIO", "El programa arrancó la simulación de las 10 operaciones.")
    
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # 1. Registrar un cliente válido con éxito
    print("Operación 1: Registro correcto de cliente")
    try:
        cli1 = Cliente("CLI-01", "Daniel Mendoza", "daniel.mendoza@unad.edu.co", "3001112233")
        lista_clientes.append(cli1)
        print(f"   > Creado con éxito: {cli1.obtener_detalles()}\n")
    except ClienteNoValidoError as e:
        print(f"   > Error: {e}\n")

    # 2. Intentar registrar un cliente con correo malo (provoca excepción)
    print("Operación 2: Registro fallido de cliente (correo sin @)")
    try:
        cli_malo = Cliente("CLI-02", "María Pérez", "correosinconsignar", "3112223344")
        lista_clientes.append(cli_malo)
    except ClienteNoValidoError as e:
        print(f"   > Excepción atrapada de forma limpia: {e}\n")

    # 3. Crear servicio de Reserva de Salas
    print("Operación 3: Creación de servicio de Sala")
    serv_sala = ReservaSalas("SRV-10", 45.0, capacidad=15)
    lista_servicios.append(serv_sala)
    print(f"   > {serv_sala.obtener_detalles()}\n")

    # 4. Crear servicio de Alquiler de Equipos
    print("Operación 4: Creación de servicio de Equipos")
    serv_eq = AlquilerEquipos("SRV-20", 25.0, tipo_equipo="Kit de Redes Cisco")
    lista_servicios.append(serv_eq)
    print(f"   > {serv_eq.obtener_detalles()}\n")

    # 5. Crear servicio de Asesoría Especializada
    print("Operación 5: Creación de servicio de Asesoría")
    serv_asesor = AsesoriaEspecializada("SRV-30", 60.0, area="Ingeniería de Telecomunicaciones")
    lista_servicios.append(serv_asesor)
    print(f"   > {serv_asesor.obtener_detalles()}\n")

    # 6. Hacer una reserva exitosa de Sala
    print("Operación 6: Procesar reserva exitosa de Sala")
    res1 = Reserva("RES-001", lista_clientes[0], lista_servicios[0], tiempo_cantidad=3)
    lista_reservas.append(res1)
    res1.procesar_reserva()
    print()

    # 7. Hacer una reserva exitosa de Equipos
    print("Operación 7: Procesar reserva exitosa de Equipos")
    res2 = Reserva("RES-002", lista_clientes[0], lista_servicios[1], tiempo_cantidad=4)
    lista_reservas.append(res2)
    res2.procesar_reserva()
    print()

    # 8. Intentar reservar un servicio desactivado
    print("Operación 8: Intentar reservar con servicio inactivo")
    lista_servicios[2].disponible = False
    res3 = Reserva("RES-003", lista_clientes[0], lista_servicios[2], tiempo_cantidad=2)
    lista_reservas.append(res3)
    res3.procesar_reserva()
    print()

    # 9. Probar un error de cálculo con parámetros inválidos (tiempo negativo)
    print("Operación 9: Validación de error interno en cálculos de costos")
    try:
        lista_servicios[0].calcular_costo(horas=-4)
    except ValueError as ex:
        print(f"   > Excepción de valores capturada con éxito: {ex}")
        registrar_log("ERROR", f"Fallo en cálculo matemático por número negativo: {ex}")
    print()

    # 10. Reactivar el servicio y procesar una reserva final con éxito
    print("Operación 10: Reactivación de asesoría y reserva final")
    lista_servicios[2].disponible = True
    res4 = Reserva("RES-004", lista_clientes[0], lista_servicios[2], tiempo_cantidad=2)
    lista_reservas.append(res4)
    res4.procesar_reserva()
    print()

    print("Simulación terminada. Revisa el archivo 'sistema_log.txt'")


if __name__ == "__main__":
    simular_operaciones_software_fj()
