"""
Módulo de servicios especializados. Implementa las clases ``Sala``, ``Equipo``
y ``Asesoria`` que heredan de :class:`~base.Servicio` y sobrescriben
``calcular_costo()`` y ``describir()``.

Este archivo consolida el contenido de ``servicios(1).py`` y se renombró para
utilizar un nombre de módulo válido en Python.
"""

from typing import Any

from base import Servicio, InvalidDataError, logger


class Sala(Servicio):
    """Reserva de salas (tarifa por hora, capacidad).

    Cada instancia de ``Sala`` representa un tipo de espacio disponible para
    reservas. Se valida que la tarifa por hora sea positiva en la clase base
    y que la capacidad también sea positiva.
    """

    def __init__(self, nombre: str, descripcion: str, tarifa_hora: float, capacidad: int) -> None:
        super().__init__(nombre, descripcion, tarifa_hora)
        if capacidad <= 0:
            msg = f"La capacidad debe ser positiva para la sala '{nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        self.capacidad = capacidad

    def calcular_costo(self, horas: float, impuesto: float = 0.0) -> float:
        """Calcula el costo de la sala en función de las horas y el impuesto.

        Args:
            horas: Número de horas a reservar.
            impuesto: Porcentaje de impuesto a aplicar (por ejemplo, 0.19 para 19%).

        Returns:
            Costo total de la reserva.

        Raises:
            InvalidDataError: Si las horas son negativas o cero.
        """
        if horas <= 0:
            msg = f"La duración en horas debe ser positiva para la sala '{self.nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        costo = self.costo_base * horas
        if impuesto:
            costo += costo * impuesto
        logger.debug(
            f"Sala '{self.nombre}' – horas: {horas}, impuesto: {impuesto}, total: {costo}"
        )
        return costo

    def describir(self) -> str:
        """Devuelve una descripción legible de la sala."""
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}). Tarifa por hora: {self.costo_base}"


class Equipo(Servicio):
    """Alquiler de equipos (tarifa por hora, depósito).

    Se valida que el depósito no sea negativo. El costo depende de las horas,
    un descuento opcional y se suma el depósito al valor final.
    """

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        tarifa_hora: float,
        tipo_equipo: str,
        deposito: float,
    ) -> None:
        super().__init__(nombre, descripcion, tarifa_hora)
        if deposito < 0:
            msg = f"El depósito no puede ser negativo para el equipo '{nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        self.tipo_equipo = tipo_equipo
        self.deposito = deposito

    def calcular_costo(self, horas: float, descuento: float = 0.0) -> float:
        """Calcula el costo total del alquiler del equipo.

        Args:
            horas: Cantidad de horas que se alquila el equipo.
            descuento: Porcentaje de descuento a aplicar (0.0–1.0).

        Returns:
            El costo total incluyendo depósito.

        Raises:
            InvalidDataError: Si las horas no son positivas.
        """
        if horas <= 0:
            msg = f"Las horas deben ser positivas para el equipo '{self.nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        costo = self.costo_base * horas
        if descuento:
            costo -= costo * descuento
        total = costo + self.deposito
        logger.debug(
            f"Equipo '{self.nombre}' – horas: {horas}, descuento: {descuento}, depósito: {self.deposito}, total: {total}"
        )
        return total

    def describir(self) -> str:
        """Devuelve una descripción legible del equipo."""
        return (
            f"Equipo '{self.nombre}' (tipo: {self.tipo_equipo}). "
            f"Tarifa por hora: {self.costo_base}, depósito: {self.deposito}"
        )


class Asesoria(Servicio):
    """Asesorías especializadas (tarifa por sesión).

    Usa el ``costo_base`` como tarifa por sesión y permite aplicar impuestos o
    descuentos opcionales. El método ``calcular_costo`` asume que ``sesiones``
    es un entero positivo.
    """

    def calcular_costo(
        self,
        sesiones: int,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        """Calcula el costo total de la asesoría.

        Args:
            sesiones: Número de sesiones contratadas.
            impuesto: Porcentaje de impuesto a aplicar (0.0–1.0).
            descuento: Porcentaje de descuento a aplicar (0.0–1.0).

        Returns:
            Costo total de la asesoría considerando impuestos y descuentos.

        Raises:
            InvalidDataError: Si ``sesiones`` no es positivo.
        """
        if sesiones <= 0:
            msg = f"El número de sesiones debe ser positivo para la asesoría '{self.nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        costo = self.costo_base * sesiones
        if descuento:
            costo -= costo * descuento
        if impuesto:
            costo += costo * impuesto
        logger.debug(
            f"Asesoría '{self.nombre}' – sesiones: {sesiones}, descuento: {descuento}, impuesto: {impuesto}, total: {costo}"
        )
        return costo

    def describir(self) -> str:
        """Devuelve una descripción legible de la asesoría."""
        return f"Asesoría '{self.nombre}'. Tarifa por sesión: {self.costo_base}"