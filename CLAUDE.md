# Evaluador de micropréstamos (todos los datos son FICTICIOS)

Objetivo: evaluar cada solicitud de `datos/solicitudes.csv` con `evaluar.py` y dejar el resultado en `salida/resultados.csv`.

## Reglas de negocio (aplicar en este orden; la primera que corresponda decide)
1. Edad fuera de 18 a 75 años → RECHAZADO.
2. 3 o más cheques rechazados en 12 meses, o 6 o más en 36 meses → RECHAZADO, sin importar el scoring.
3. Scoring menor a 600 → RECHAZADO.
4. Scoring 700 o más: hasta $500.000 y 24 cuotas. Scoring 600 a 699: hasta $200.000 y 12 cuotas. Si excede el monto o el plazo → RECHAZADO.
5. (monto / plazo + cuotas_otras_deudas) mayor al 35% del ingreso mensual → RECHAZADO. Justo en 35% se acepta.
6. Si pasó todo lo anterior y tiene 1 o más cheques rechazados en los últimos 3 meses → REVISION_MANUAL.
7. Todo lo demás → APROBADO.

## Reglas de trabajo
- No modificar `datos/` ni `tests.py` sin mi aprobación: los tests son las reglas de negocio hechas ejecutables.
- Un paso por vez: mostrar el cambio y esperar mi OK antes de seguir.
- Después de cada cambio correr `python -m pytest tests.py` y contarme qué pasó.
- Solo librería estándar de Python (más pytest para los tests). Sin red.
- Registrar en `evaluar.log` cuántas solicitudes se procesaron, el total por decisión y por motivo.
