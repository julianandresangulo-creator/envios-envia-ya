"""Cálculo del costo de envíos de EnvíaYa.

Versión 2.1.0. Parámetros de este código estudiantil: ver CHANGELOG.md.
Orden de cálculo: tarifa base -> recargo de zona -> hora pico -> descuentos (cliente y
luego cupón) -> recargo de fin de semana -> mínimo -> redondeo.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# --- Parámetros del negocio (derivados del código estudiantil) -------------
PESO_MAXIMO_KG = Decimal("45")
LIMITE_TRAMO_1_KG = Decimal("3")      # incluido: peso <= 3 (D par)
LIMITE_TRAMO_2_KG = Decimal("10")
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
TARIFA_KG_ADICIONAL = Decimal("800")
RECARGO_FINDE = Decimal("2000")       # se suma después de descuentos (E impar)
COSTO_MINIMO = Decimal("5000")
MULTIPLO_REDONDEO = Decimal("100")
CUPON_ENVIO10 = "ENVIO10"
DIA_MINIMO = 1
DIA_MAXIMO = 7
DIA_SABADO = 6
HORA_MINIMA = 0
HORA_MAXIMA = 23
HORA_PICO_INICIO = 17
HORA_PICO_FIN = 19                    # inclusive
RECARGO_HORA_PICO = Decimal("0.08")


# --- Patrón Estrategia: recargo por zona -----------------------------------
class EstrategiaZona(ABC):
    @abstractmethod
    def aplicar(self, monto):
        """Devuelve el monto con el recargo de la zona."""


class ZonaUrbana(EstrategiaZona):
    def aplicar(self, monto):
        return monto


class ZonaRural(EstrategiaZona):
    RECARGO = Decimal("0.15")

    def aplicar(self, monto):
        return monto * (1 + self.RECARGO)


class ZonaNacional(EstrategiaZona):
    RECARGO = Decimal("0.50")

    def aplicar(self, monto):
        return monto * (1 + self.RECARGO)


ZONAS = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# --- Patrón Estrategia: descuentos (cliente y cupón) -----------------------
class EstrategiaDescuento(ABC):
    PORCENTAJE = Decimal("0")

    def aplicar(self, monto):
        return monto * (1 - self.PORCENTAJE)


class SinDescuento(EstrategiaDescuento):
    pass


class DescuentoFrecuente(EstrategiaDescuento):
    PORCENTAJE = Decimal("0.05")


class DescuentoVip(EstrategiaDescuento):
    PORCENTAJE = Decimal("0.10")


class CuponEnvio10(EstrategiaDescuento):
    PORCENTAJE = Decimal("0.10")


DESCUENTOS_CLIENTE = {
    "frecuente": DescuentoFrecuente(),
    "vip": DescuentoVip(),
}
CUPONES = {
    CUPON_ENVIO10: CuponEnvio10(),
}
SIN_DESCUENTO = SinDescuento()


# --- Funciones auxiliares ---------------------------------------------------
def _validar_entradas(peso, zona, dia, hora=None):
    if peso <= 0 or peso > PESO_MAXIMO_KG:
        raise ValueError("peso invalido")
    if zona not in ZONAS:
        raise ValueError("zona invalida")
    if not DIA_MINIMO <= dia <= DIA_MAXIMO:
        raise ValueError("dia invalido")
    if hora is not None and not HORA_MINIMA <= hora <= HORA_MAXIMA:
        raise ValueError("hora invalida")


def _tarifa_base(peso):
    if peso <= LIMITE_TRAMO_1_KG:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2_KG:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2_KG) * TARIFA_KG_ADICIONAL


def _aplicar_hora_pico(monto, hora):
    if hora is not None and HORA_PICO_INICIO <= hora <= HORA_PICO_FIN:
        return monto * (1 + RECARGO_HORA_PICO)
    return monto


def _aplicar_descuentos(monto, cliente, cupon):
    # B impar: se aplican ambos, primero el del cliente y luego el cupón.
    # F par: un cupón inexistente se ignora.
    monto = DESCUENTOS_CLIENTE.get(cliente, SIN_DESCUENTO).aplicar(monto)
    if cupon in CUPONES:
        monto = CUPONES[cupon].aplicar(monto)
    return monto


def _recargo_finde(dia):
    return RECARGO_FINDE if dia >= DIA_SABADO else Decimal("0")


def _redondear(monto):
    unidades = (monto / MULTIPLO_REDONDEO).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)
    return int(unidades * MULTIPLO_REDONDEO)


# --- Función pública --------------------------------------------------------
def calcular_costo(peso, zona, cliente, dia, cupon=None, hora=None):
    peso = Decimal(str(peso))
    _validar_entradas(peso, zona, dia, hora)
    monto = ZONAS[zona].aplicar(_tarifa_base(peso))
    monto = _aplicar_hora_pico(monto, hora)
    monto = _aplicar_descuentos(monto, cliente, cupon)
    monto += _recargo_finde(dia)
    monto = max(monto, COSTO_MINIMO)
    return _redondear(monto)
