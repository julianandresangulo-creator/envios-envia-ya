# Changelog
Todos los cambios importantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [2.1.0]
### Added
- Parámetro opcional `hora` (0 a 23). Entre las 17 y las 19, inclusive,
  recargo del 8 % calculado después del recargo por zona (R9).
- Error "hora invalida" cuando la hora está fuera de 0 a 23.
- Pruebas `tests/test_hora_pico.py` (H01 a H13), escritas antes del código.

## [2.0.0]
### Changed
- **BREAKING:** `calc` se renombra a `calcular_costo` y recibe nombres claros
  (`peso, zona, cliente, dia, cupon`).
- Refactorización: funciones auxiliares, constantes con nombre y patrón
  Estrategia para zonas y descuentos. El cálculo usa `Decimal`.
### Removed
- **BREAKING:** argumento `flag` y su `print` dentro de la lógica de negocio.

## [1.0.1]
### Fixed
- DEF-01: el peso máximo es 45 kg, no 50 (R1).
- DEF-02: una zona inválida lanza error (R2).
- DEF-03: un día fuera de 1 a 7 lanza error (R2).
- DEF-04: el sábado recibe el recargo de fin de semana (R5).
- DEF-05: el recargo de fin de semana se suma después de los descuentos (R5, R6).
- DEF-06: el redondeo es al múltiplo de $100 más cercano, con los $50 hacia arriba (R8).

## [1.0.0]
### Added
- Código heredado de EnvíaYa con `CONFIG` llenado con los parámetros del
  código estudiantil 0182310018.

[2.1.0]: https://github.com/USUARIO/REPO/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/USUARIO/REPO/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/USUARIO/REPO/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/USUARIO/REPO/releases/tag/v1.0.0
