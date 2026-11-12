"""Pruebas de la solicitud de cambio: hora pico (escritas ANTES del código)."""
import pytest
from envios import calcular_costo

ERR = "ERR"

CASOS_HORA = [
    pytest.param((5, "urbana", "normal", 1, None, 16), 9000, id="H01"),   # justo antes de la hora pico
    pytest.param((5, "urbana", "normal", 1, None, 17), 9700, id="H02"),   # límite inferior (inclusive)
    pytest.param((5, "urbana", "normal", 1, None, 18), 9700, id="H03"),   # dentro de la franja
    pytest.param((5, "urbana", "normal", 1, None, 19), 9700, id="H04"),   # límite superior (inclusive)
    pytest.param((5, "urbana", "normal", 1, None, 20), 9000, id="H05"),   # justo después
    pytest.param((5, "urbana", "normal", 1, None, 0), 9000, id="H06"),    # límite del rango válido
    pytest.param((5, "urbana", "normal", 1, None, 23), 9000, id="H07"),   # límite del rango válido
    pytest.param((5, "urbana", "normal", 1, None, -1), ERR, id="H08"),    # hora inválida
    pytest.param((5, "urbana", "normal", 1, None, 24), ERR, id="H09"),    # hora inválida
    pytest.param((5, "rural", "normal", 1, None, 18), 11200, id="H10"),   # el 8 % va después de la zona
    pytest.param((5, "urbana", "normal", 1, None, None), 9000, id="H11"), # sin hora: compatibilidad
    pytest.param((5, "rural", "vip", 6, "ENVIO10", 18), 11100, id="H12"), # combinación completa
    pytest.param((2, "urbana", "vip", 1, "ENVIO10", 17), 5200, id="H13"), # interacción con el mínimo
]


@pytest.mark.parametrize("entrada, esperado", CASOS_HORA)
def test_hora_pico(entrada, esperado):
    if esperado == ERR:
        with pytest.raises(ValueError):
            calcular_costo(*entrada)
    else:
        assert calcular_costo(*entrada) == esperado
