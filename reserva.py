"""
Módulo de reservas y demostración. Define la clase :class:`Reserva` (con
confirmación, cancelación y procesamiento) y la función ``simular_operaciones``
que ejecuta casos válidos e inválidos para probar el manejo de excepciones.

Se renombró desde ``reserva(3).py`` y se corrigieron errores de importación y
anotaciones de tipos para facilitar su uso como módulo estándar de Python.
"""

from typing import List

from base import (
    Entity,
    ReservationError,
    InvalidDataError,
    logger,
    Servicio,
)
from cliente import Cliente
from servicios import Sala, Equipo, Asesoria


class Reserva(Entity):
    """Gestiona una reserva asociando un cliente, un servicio y una duración.

    Las reservas pueden estar en tres estados: pendiente, confirmada o
    cancelada. Permite calcular el costo delegando al servicio, confirmar
    reservas y cancelarlas.
    """

    ESTADO_PENDIENTE: str = "pendiente"
    ESTADO_CONFIRMADA: str = "confirmada"
    ESTADO_CANCELADA: str = "cancelada"

    def __init__(self, cliente: Cliente, servicio: Servicio, unidades: float) -> None:
        super().__init__()
        # Validar unidades positivas
        if unidades <= 0:
            msg = "La duración/unidades debe ser positiva para la reserva."
            logger.error(msg)
            raise InvalidDataError(msg)
        self.cliente: Cliente = cliente
        self.servicio: Servicio = servicio
        self.unidades: float = unidades
        self.estado: str = self.ESTADO_PENDIENTE
        logger.info(
            f"Reserva creada: cliente={cliente.nombre}, servicio={servicio.nombre}, unidades={unidades}"
        )

    def calcular_costo(self) -> float:
        """Calcula el costo delegando en el servicio asociado.

        Returns:
            Costo total de la reserva.

        Raises:
            Exception: Repropaga cualquier excepción producida por el servicio.
        """
        try:
            return self.servicio.calcular_costo(self.unidades)
        except Exception as exc:
            logger.exception(f"Error al calcular costo de reserva {self.id}: {exc}")
            raise

    def confirmar(self) -> None:
        """Confirma la reserva si se encuentra en estado pendiente.

        Raises:
            ReservationError: Si la reserva ya está confirmada o cancelada.
        """
        if self.estado != self.ESTADO_PENDIENTE:
            msg = f"No se puede confirmar reserva {self.id} porque está {self.estado}."
            logger.error(msg)
            raise ReservationError(msg)
        self.estado = self.ESTADO_CONFIRMADA
        logger.info(f"Reserva {self.id} confirmada.")

    def cancelar(self) -> None:
        """Cancela la reserva si no está ya cancelada.

        Raises:
            ReservationError: Si la reserva ya se encontraba cancelada.
        """
        if self.estado == self.ESTADO_CANCELADA:
            msg = f"La reserva {self.id} ya está cancelada."
            logger.error(msg)
            raise ReservationError(msg)
        self.estado = self.ESTADO_CANCELADA
        logger.info(f"Reserva {self.id} cancelada.")

    def procesar(self) -> float:
        """Procesa la reserva: calcula el costo y confirma.

        Usa bloques ``try/except/else/finally`` para garantizar que el
        procesamiento se registra en el log independientemente del resultado.

        Returns:
            Costo total calculado.

        Raises:
            Exception: Propaga errores del cálculo de costo.
        """
        try:
            logger.debug(
                f"Procesando reserva {self.id} para {self.cliente.nombre}."
            )
            costo = self.calcular_costo()
        except Exception as exc:
            logger.exception(f"Fallo en procesamiento de reserva {self.id}: {exc}")
            raise
        else:
            self.confirmar()
            logger.info(f"Reserva {self.id} procesada. Costo total: {costo}")
            return costo
        finally:
            logger.debug(f"Finalizó procesamiento de reserva {self.id}.")


def simular_operaciones() -> None:
    """Ejecuta operaciones de prueba para validar el manejo de errores.

    Se crean clientes y servicios válidos e inválidos y se intenta realizar
    reservas en diferentes escenarios para comprobar que las excepciones se
    gestionan correctamente. Al finalizar, imprime un resumen de las
    operaciones ejecutadas.
    """
    operaciones: List[str] = []
    clientes: List[Cliente] = []
    servicios: List[Sala | Equipo | Asesoria] = []
    reservas: List[Reserva] = []

    # 1. Cliente válido
    try:
        c1 = Cliente("Andrea Pérez", "andrea.perez@example.com", "3001234567")
        clientes.append(c1)
        operaciones.append("Cliente válido creado")
    except InvalidDataError as e:
        operaciones.append(f"Fallo: {e}")

    # 2. Cliente con email inválido
    try:
        c2 = Cliente("Luis Gómez", "luis.gomez[at]example.com", "3107654321")
        clientes.append(c2)
        operaciones.append("Email inválido no debería crearse")
    except InvalidDataError as e:
        operaciones.append(f"Email inválido detectado: {e}")

    # 3. Sala válida
    try:
        sala1 = Sala("Sala Grande", "Sala amplia", tarifa_hora=50.0, capacidad=20)
        servicios.append(sala1)
        operaciones.append("Sala válida creada")
    except InvalidDataError as e:
        operaciones.append(f"Fallo sala: {e}")

    # 4. Sala con capacidad negativa
    try:
        sala2 = Sala("Sala Pequeña", "Capacidad negativa", tarifa_hora=30.0, capacidad=-5)
        servicios.append(sala2)
        operaciones.append("Sala inválida creada")
    except InvalidDataError as e:
        operaciones.append(f"Capacidad inválida detectada: {e}")

    # 5. Equipo válido
    try:
        eq1 = Equipo(
            "Proyector", "Proyector HD", tarifa_hora=15.0, tipo_equipo="proyector", deposito=50.0
        )
        servicios.append(eq1)
        operaciones.append("Equipo válido creado")
    except InvalidDataError as e:
        operaciones.append(f"Fallo equipo: {e}")

    # 6. Asesoría con costo base negativo (debe fallar)
    try:
        ases1 = Asesoria("Consultoría", "Costo negativo", costo_base=-100.0)  # type: ignore[arg-type]
        servicios.append(ases1)
        operaciones.append("Asesoría inválida creada")
    except InvalidDataError as e:
        operaciones.append(f"Costo base negativo detectado: {e}")

    # 7. Reserva válida y procesamiento
    try:
        if clientes and servicios:
            r1 = Reserva(clientes[0], servicios[0], unidades=2)
            reservas.append(r1)
            costo = r1.procesar()
            operaciones.append(f"Reserva válida procesada. Costo: {costo}")
        else:
            operaciones.append("No se pudo crear reserva válida (falta cliente/servicio)")
    except Exception as e:
        operaciones.append(f"Error en reserva válida: {e}")

    # 8. Confirmar dos veces (debe fallar)
    try:
        if reservas:
            reservas[0].confirmar()  # ya está confirmada por procesar()
            operaciones.append("Confirmación duplicada")
    except ReservationError as e:
        operaciones.append(f"Confirmación duplicada detectada: {e}")

    # 9. Reserva con unidades negativas (debe fallar)
    try:
        if clientes and servicios:
            r2 = Reserva(clientes[0], servicios[0], unidades=-3)
            reservas.append(r2)
            operaciones.append("Reserva con unidades negativas creada")
    except InvalidDataError as e:
        operaciones.append(f"Unidades negativas detectadas: {e}")

    # 10. Cancelar dos veces
    try:
        if reservas:
            # Cancelar la primera reserva si no lo está
            if reservas[0].estado != Reserva.ESTADO_CANCELADA:
                reservas[0].cancelar()
            # Segundo intento de cancelar (falla)
            reservas[0].cancelar()
            operaciones.append("Cancelación duplicada")
    except ReservationError as e:
        operaciones.append(f"Cancelación duplicada detectada: {e}")

    # Resumen final (imprimir en consola y registrar)
    logger.info("Simulación completada. Resumen de operaciones:")
    for op in operaciones:
        logger.info(f" - {op}")

    print("\n=== RESUMEN DE OPERACIONES ===")
    for op in operaciones:
        print(f" • {op}")
    print("=== Fin de la simulación ===\n")


if __name__ == "__main__":
    simular_operaciones()