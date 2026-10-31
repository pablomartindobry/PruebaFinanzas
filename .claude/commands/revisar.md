---
description: Compara las 2 ultimas corridas de evaluar.py segun evaluar.log (solo lectura)
allowed-tools: Read, Grep
---

Comando de SOLO LECTURA: no modifiques, crees ni borres ningun archivo, y no ejecutes `evaluar.py` ni los tests. Usa unicamente Read/Grep sobre `evaluar.log`.

## Pasos

1. Lee `evaluar.log` (raiz del proyecto). Si no existe, decilo y termina.
2. Ubica las corridas. Cada corrida termina con una linea `Solicitudes procesadas: N de M (errores: E)`; las lineas `Decision ...`, `Motivo ...` y los `ERROR` que la preceden/siguen pertenecen a esa corrida. Toma las 2 ultimas.
   - procesadas = N, leidas = M, con error = E.
   - aprobadas / revision manual / rechazadas: de las lineas `Decision APROBADO|REVISION_MANUAL|RECHAZADO: n` de esa corrida (si falta una, es 0).
   - Fecha y hora: el timestamp de la linea `Solicitudes procesadas`.
3. Muestra una tabla corta (Diferencia = ultima - anterior, con signo):

| Metrica | Corrida anterior | Ultima corrida | Diferencia |
|---|---|---|---|
| Fecha y hora | ... | ... | - |
| Solicitudes leidas | | | |
| Procesadas | | | |
| Con error | | | |
| Aprobadas | | | |
| Revision manual | | | |
| Rechazadas | | | |

4. Si alguna de las dos corridas tuvo solicitudes con error, listalas debajo de la tabla (corrida, `id_solicitud` o numero de fila del CSV, y el motivo de la linea `ERROR`). Si ninguna tuvo, omiti esta seccion.
5. Cierra con una sola linea: **Sin Cambios** si todas las metricas son iguales, o **Con Diferencias: <metricas que difieren>**.

## Si el log tiene una sola corrida
Dilo claramente ("evaluar.log tiene una sola corrida"), mostra sus datos (fecha y hora y las metricas) y NO inventes comparacion ni diferencias ni la linea final de Sin Cambios/Con Diferencias.
