"""
Módulo para la gestión de clientes. Define la clase Cliente con validaciones
robustas de nombre, email y teléfono.
"""

import re
from base import Entity, InvalidDataError, logger


class Cliente(Entity):
    """Representa un cliente del sistema. Encapsula sus datos y valida entradas."""

    def __init__(self, nombre: str, email: str, telefono: str) -> None:
        super().__init__()
        self._nombre: str | None = None
        self._email: str | None = None
        self._telefono: str | None = None
        # Usa las propiedades para validar
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre  # type: ignore

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            msg = "El nombre del cliente no puede estar vacío."
            logger.error(msg)
            raise InvalidDataError(msg)
        self._nombre = value.strip()

    @property
    def email(self) -> str:
        return self._email  # type: ignore

    @email.setter
    def email(self, value: str) -> None:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            msg = f"Email inválido para el cliente '{self.nombre}': {value}"
            logger.error(msg)
            raise InvalidDataError(msg)
        self._email = value

    @property
    def telefono(self) -> str:
        return self._telefono  # type: ignore

    @telefono.setter
    def telefono(self, value: str) -> None:
        digits = re.sub(r"\D", "", value)
        if len(digits) < 7:
            msg = f"Teléfono inválido para el cliente '{self.nombre}': {value}"
            logger.error(msg)
            raise InvalidDataError(msg)
        self._telefono = digits

    def __str__(self) -> str:
        return f"Cliente({self.id}, {self.nombre})"