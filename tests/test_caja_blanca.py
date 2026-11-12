"""Caminos independientes de calc (caja blanca). Ver Parte 4 del informe."""
import pytest

try:
    from envios import calcular_costo as calc   # v2.x
except ImportError:
    from envios import calc                      # v1.x (código heredado)

ERR = "ERR"

CAMINOS = [
    pytest.param((2, "urbana", "normal", 1, None), 6000, id="WB01"),       # camino base
    pytest.param((0, "urbana", "normal", 1, None), ERR, id="WB02"),        # peso <= 0
    pytest.param((51, "urbana", "normal", 1, None), ERR, id="WB03"),       # peso > máximo
    pytest.param((5, "urbana", "normal", 1, None), 9000, id="WB04"),       # tramo 2
    pytest.param((12, "urbana", "normal", 1, None), 10600, id="WB05"),     # tramo 3
    pytest.param((2, "rural", "normal", 1, None), 6900, id="WB06"),        # zona rural
    pytest.param((2, "nacional", "normal", 1, None), 9000, id="WB07"),     # zona nacional
    pytest.param((2, "galaxia", "normal", 1, None), ERR, id="WB08"),       # zona inválida
    pytest.param((2, "urbana", "normal", 7, None), 8000, id="WB09"),       # fin de semana
    pytest.param((2, "urbana", "frecuente", 1, None), 5700, id="WB10"),    # cliente frecuente
    pytest.param((2, "urbana", "vip", 1, None), 5400, id="WB11"),          # cliente VIP
    pytest.param((2, "urbana", "normal", 1, "PROMO99"), 6000, id="WB12"),  # cupón inexistente
    pytest.param((5, "urbana", "normal", 1, "ENVIO10"), 8100, id="WB13"),  # cupón ENVIO10
    pytest.param((2, "urbana", "vip", 1, "ENVIO10"), 5000, id="WB14"),     # mínimo $5.000
]


@pytest.mark.parametrize("entrada, esperado", CAMINOS)
def test_camino(entrada, esperado):
    if esperado == ERR:
        with pytest.raises(ValueError):
            calc(*entrada)
    else:
        assert calc(*entrada) == esperado
