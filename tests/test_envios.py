"""Suite de pruebas de EnvíaYa (pytest). Parámetros: ver CHANGELOG.md."""
import pytest

try:
    from envios import calcular_costo as calc   # v2.x
except ImportError:
    from envios import calc                      # v1.x (código heredado)

ERR = "ERR"

CASOS = [
    pytest.param((0, 'urbana', 'normal', 1, None), "ERR", id="CP01"),  # R1 | Valor límite (0)
    pytest.param((-1, 'urbana', 'normal', 1, None), "ERR", id="CP02"),  # R1 | Partición inválida (peso < 0)
    pytest.param((0.01, 'urbana', 'normal', 1, None), 6000, id="CP03"),  # R1/R3 | Valor límite (0 más un centésimo)
    pytest.param((45, 'urbana', 'normal', 1, None), 37000, id="CP04"),  # R1/R3 | Valor límite (PMAX)
    pytest.param((45.01, 'urbana', 'normal', 1, None), "ERR", id="CP05"),  # R1 | Valor límite (PMAX+)
    pytest.param((50, 'urbana', 'normal', 1, None), "ERR", id="CP06"),  # R1 | Partición inválida (peso > PMAX)
    pytest.param((3, 'urbana', 'normal', 1, None), 6000, id="CP07"),  # R3 | Valor límite (L1, incluido por D par)
    pytest.param((3.01, 'urbana', 'normal', 1, None), 9000, id="CP08"),  # R3 | Valor límite (L1+)
    pytest.param((10, 'urbana', 'normal', 1, None), 9000, id="CP09"),  # R3 | Valor límite (L2, incluido)
    pytest.param((10.5, 'urbana', 'normal', 1, None), 9400, id="CP10"),  # R3 | Valor límite (L2+) / partición tramo 3
    pytest.param((20, 'urbana', 'normal', 1, None), 17000, id="CP11"),  # R3 | Partición válida (tramo 3)
    pytest.param((5, 'rural', 'normal', 2, None), 10400, id="CP12"),  # R4/R8 | Partición zona rural / redondeo $50
    pytest.param((5, 'nacional', 'normal', 3, None), 13500, id="CP13"),  # R4 | Partición zona nacional
    pytest.param((5, 'urbana', 'normal', 4, None), 9000, id="CP14"),  # R4 | Partición zona urbana
    pytest.param((5, 'internacional', 'normal', 1, None), "ERR", id="CP15"),  # R2 | Partición inválida (zona)
    pytest.param((5, 'urbana', 'normal', 0, None), "ERR", id="CP16"),  # R2 | Valor límite (día 0)
    pytest.param((5, 'urbana', 'normal', 8, None), "ERR", id="CP17"),  # R2 | Valor límite (día 8)
    pytest.param((2, 'urbana', 'normal', 6, None), 8000, id="CP18"),  # R5 | Valor límite (sábado)
    pytest.param((2, 'urbana', 'normal', 7, None), 8000, id="CP19"),  # R5 | Valor límite (domingo)
    pytest.param((2, 'urbana', 'normal', 5, None), 6000, id="CP20"),  # R5 | Valor límite (viernes)
    pytest.param((5, 'urbana', 'frecuente', 1, None), 8600, id="CP21"),  # R6/R8 | Tabla de decisión (frecuente, sin cupón)
    pytest.param((5, 'urbana', 'vip', 1, None), 8100, id="CP22"),  # R6 | Tabla de decisión (VIP, sin cupón)
    pytest.param((5, 'urbana', 'normal', 1, 'ENVIO10'), 8100, id="CP23"),  # R6 | Tabla de decisión (normal + cupón)
    pytest.param((5, 'urbana', 'vip', 1, 'ENVIO10'), 7300, id="CP24"),  # R6 | Tabla de decisión (VIP + cupón, ambos)
    pytest.param((5, 'urbana', 'frecuente', 1, 'ENVIO10'), 7700, id="CP25"),  # R6 | Tabla de decisión (frecuente + cupón)
    pytest.param((5, 'urbana', 'vip', 7, 'ENVIO10'), 9300, id="CP26"),  # R5/R6 | Tabla de decisión (VIP + cupón + finde)
    pytest.param((5, 'urbana', 'normal', 1, 'PROMO99'), 9000, id="CP27"),  # R7 | Partición cupón inexistente (F par: se ignora)
    pytest.param((2, 'urbana', 'vip', 1, 'ENVIO10'), 5000, id="CP28"),  # R8 | Valor límite (mínimo $5.000)
    pytest.param((10.05, 'urbana', 'normal', 1, None), 9000, id="CP29"),  # R8 | Redondeo hacia abajo
    pytest.param((5, 'rural', 'vip', 6, 'ENVIO10'), 10400, id="CP30"),  # R4/R5/R6 | Combinación (ejemplo del enunciado)
    pytest.param((12, 'nacional', 'frecuente', 7, None), 17100, id="CP31"),  # R3/R4/R5/R6 | Combinación (tramo 3 + nacional + finde + frecuente)
    pytest.param((45, 'nacional', 'vip', 6, 'ENVIO10'), 47000, id="CP32"),  # R1/R3/R4/R5/R6 | Combinación (PMAX, todos los factores)
    pytest.param((5, 'urbana', 'frecuente', 7, None), 10600, id="CP33"),  # R5/R6 | Tabla de decisión (frecuente + finde)
    pytest.param((5, 'urbana', 'normal', 6, 'ENVIO10'), 10100, id="CP34"),  # R5/R6 | Tabla de decisión (cupón + finde, sin cliente)
    pytest.param((5, 'urbana', 'vip', 7, None), 10100, id="CP35"),  # R5 | Tabla de decisión (VIP + finde: orden del recargo)
    pytest.param((5, 'urbana', 'normal', 7, None), 11000, id="CP36"),  # R5 | Tabla de decisión (normal + finde)
    pytest.param((5, 'urbana', 'frecuente', 7, 'ENVIO10'), 9700, id="CP37"),  # R5/R6 | Tabla de decisión (frecuente + cupón + finde)
]


@pytest.mark.parametrize("entrada, esperado", CASOS)
def test_costo(entrada, esperado):
    if esperado == ERR:
        with pytest.raises(ValueError):
            calc(*entrada)
    else:
        assert calc(*entrada) == esperado
