import csv
import logging
import os
from collections import Counter

COLUMNAS_TEXTO = {"fecha_solicitud", "nombre_solicitante", "ciudad"}


def cargar_solicitudes(ruta, filas_con_error=None):
    """Lee el CSV; una fila con valores invalidos se registra en el log, se salta y se anota en filas_con_error."""
    solicitudes = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for nro, fila in enumerate(csv.DictReader(f), start=2):  # la fila 1 es el encabezado
            try:
                solicitudes.append({col: val if col in COLUMNAS_TEXTO else int(val)
                                    for col, val in fila.items()})
            except (ValueError, TypeError):
                logging.exception("Fila %d del CSV invalida (id_solicitud=%s)", nro, fila.get("id_solicitud"))
                if filas_con_error is not None:
                    filas_con_error.append(nro)
    return solicitudes


def evaluar(s):
    if s["edad"] < 18 or s["edad"] > 75:
        return {"decision": "RECHAZADO", "motivo": "edad fuera de rango"}

    if s["cheques_rechazados_12m"] >= 3 or s["cheques_rechazados_36m"] >= 6:
        return {"decision": "RECHAZADO", "motivo": "cheques rechazados"}

    if s["scoring"] < 600:
        return {"decision": "RECHAZADO", "motivo": "scoring bajo"}

    if s["scoring"] >= 700:
        tope, plazo_max = 500000, 24
    else:
        tope, plazo_max = 200000, 12

    if s["monto_solicitado"] > tope:
        return {"decision": "RECHAZADO", "motivo": "monto supera el tope"}
    if s["plazo_meses"] > plazo_max:
        return {"decision": "RECHAZADO", "motivo": "plazo supera el maximo"}

    # monto/plazo + otras deudas > 35% del ingreso, en enteros para evitar errores de coma flotante
    cuota_x_plazo = s["monto_solicitado"] + s["cuotas_otras_deudas"] * s["plazo_meses"]
    if cuota_x_plazo * 100 > s["ingreso_mensual"] * s["plazo_meses"] * 35:
        return {"decision": "RECHAZADO", "motivo": "cuota supera el 35% del ingreso"}

    if s["cheques_rechazados_3m"] >= 1:
        return {"decision": "REVISION_MANUAL", "motivo": "cheque rechazado en los ultimos 3 meses"}

    return {"decision": "APROBADO", "motivo": "ok"}


def main():
    logging.basicConfig(filename="evaluar.log", filemode="w", encoding="utf-8",
                        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    filas_con_error = []
    solicitudes = cargar_solicitudes("datos/solicitudes.csv", filas_con_error)
    resultados = []
    errores = len(filas_con_error)
    for s in solicitudes:
        try:
            r = evaluar(s)
            resultados.append({**s, **r})
        except Exception:
            errores += 1
            logging.exception("Error evaluando solicitud %s", s.get("id_solicitud"))

    os.makedirs("salida", exist_ok=True)
    if resultados:
        with open("salida/resultados.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
            w.writeheader()
            w.writerows(resultados)

    logging.info("Solicitudes procesadas: %d de %d (errores: %d)",
                 len(resultados), len(solicitudes) + len(filas_con_error), errores)
    for decision, n in Counter(r["decision"] for r in resultados).items():
        logging.info("Decision %s: %d", decision, n)
    for (decision, motivo), n in Counter((r["decision"], r["motivo"]) for r in resultados).items():
        logging.info("Motivo [%s] %s: %d", decision, motivo, n)
    print("Listo")


if __name__ == "__main__":
    main()
