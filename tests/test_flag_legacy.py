"""WB15: camino con flag=True. SOLO existe en v1.x; se elimina junto con el
argumento flag en la refactorización (v2.0.0)."""
import pytest
from envios import calc


@pytest.mark.parametrize("entrada, esperado", [
    pytest.param((2, "urbana", "normal", 1, None, True), 6000, id="WB15"),
])
def test_flag(entrada, esperado):
    assert calc(*entrada) == esperado
