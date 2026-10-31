# Diccionario de datos: `datos/solicitudes.csv`

**Todos los datos son sintéticos** (semilla 42, generados con `generar_solicitudes.py`). Los nombres, scorings e historiales no corresponden a personas reales ni a ningún ente crediticio real.

200 filas × 26 columnas · CSV UTF-8, separador `,` · una fila = una solicitud de micropréstamo · montos en pesos (ficticios).

| # | Columna | Tipo | Descripción | Rango / valores |
|---|---|---|---|---|
| 1 | `id_solicitud` | entero | Identificador único | 1 a 200 |
| 2 | `fecha_solicitud` | fecha ISO | Fecha de la solicitud | 2026-04-02 a 2026-09-28 |
| 3 | `nombre_solicitante` | texto | Nombre ficticio | 182 nombres distintos |
| 4 | `ciudad` | texto | Ciudad del solicitante | 10 ciudades |
| 5 | `edad` | entero | Años cumplidos | 18 a 78 |
| 6 | `ingreso_mensual` | entero | Ingreso mensual declarado | 341.000 a 3.725.000 |
| 7 | `antiguedad_actividad_meses` | entero | Meses en su actividad actual (0 para jubilados) | 0 a 370 |
| 8 | `cuotas_otras_deudas` | entero | Suma mensual de cuotas de otras deudas | 0 a 1.368.000 |
| 9 | `monto_solicitado` | entero | Monto pedido | 30.000 a 600.000 |
| 10 | `plazo_meses` | entero | Cantidad de cuotas pedidas | 6, 12, 18, 24, 36 |
| 11 | `scoring` | entero | Puntaje de un ente crediticio externo (ficticio) | 528 a 892 |
| 12 | `cheques_rechazados_3m` | entero | Cheques rechazados en los últimos 3 meses | 0 a 3 |
| 13 | `cheques_rechazados_6m` | entero | ... últimos 6 meses (incluye los de 3m) | 0 a 4 |
| 14 | `cheques_rechazados_9m` | entero | ... últimos 9 meses | 0 a 4 |
| 15 | `cheques_rechazados_12m` | entero | ... últimos 12 meses | 0 a 5 |
| 16 | `cheques_rechazados_18m` | entero | ... últimos 18 meses | 0 a 6 |
| 17 | `cheques_rechazados_24m` | entero | ... últimos 24 meses | 0 a 8 |
| 18 | `cheques_rechazados_36m` | entero | ... últimos 36 meses | 0 a 9 |
| 19 | `tiene_tarjeta_credito` | booleano 0/1 | Posee tarjeta de crédito | 0 / 1 |
| 20 | `laboral_dependiente` | booleano 0/1 | Situación laboral (excluyente: un solo 1 entre 20 y 23) | 104 filas |
| 21 | `laboral_monotributista` | booleano 0/1 | | 43 filas |
| 22 | `laboral_autonomo` | booleano 0/1 | | 44 filas |
| 23 | `laboral_jubilado` | booleano 0/1 | | 9 filas |
| 24 | `vivienda_propia` | booleano 0/1 | Tipo de vivienda (excluyente: un solo 1 entre 24 y 26) | 79 filas |
| 25 | `vivienda_alquila` | booleano 0/1 | | 73 filas |
| 26 | `vivienda_familiar` | booleano 0/1 | | 48 filas |

## Relaciones internas
- Las ventanas de cheques son **acumulativas**: `3m ≤ 6m ≤ 9m ≤ 12m ≤ 18m ≤ 24m ≤ 36m` en cada fila.
- Mayor riesgo latente → menor scoring y más cheques rechazados (correlación intencional).
- Hay 14 casos límite escritos a mano (scoring 700 exacto, 3 cheques en 12 meses, cuota justo en 35%, edades 75 y 78, etc.) mezclados con las filas aleatorias.
- `laboral_*` y `vivienda_*` no intervienen en las reglas actuales: quedan disponibles para sumar reglas nuevas.
