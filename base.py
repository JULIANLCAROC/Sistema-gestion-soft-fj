"""
Módulo base del Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Define la configuración de logging, excepciones personalizadas, la clase Entity
(identificadores únicos) y la clase abstracta Servicio.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

# Configuración de logging: escribe en archivo y captura nivel DEBUG
logging.basicConfig(
    filename="sistema_gestion.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


# Excepciones personalizadas
class InvalidDataError(Exception):
    """Datos proporcionados inválidos (email, teléfono, costo base, etc.)."""


class ServiceNotAvailableError(Exception):
    """Servicio no disponible o parámetros incorrectos."""


class ReservationError(Exception):
    """Error relacionado con operaciones de reserva (confirmar, cancelar)."""


# Clase base para todas las entidades (asigna ID automático)
class Entity:
    _next_id: int = 1

    def __init__(self) -> None:
        self.id = Entity._next_id
        Entity._next_id += 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


# Clase abstracta Servicio
class Servicio(Entity, ABC):
    """Define la interfaz común para todos los servicios."""

    def __init__(self, nombre: str, descripcion: str, costo_base: float) -> None:
        super().__init__()
        if costo_base <= 0:
            msg = f"El costo base debe ser positivo para el servicio '{nombre}'."
            logger.error(msg)
            raise InvalidDataError(msg)
        self.nombre = nombre
        self.descripcion_servicio = descripcion
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args: Any, **kwargs: Any) -> float:
        """Calcula el costo total del servicio (polimórfico)."""

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción textual del servicio."""