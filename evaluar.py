import csv
import os

COLUMNAS_TEXTO = {"fecha_solicitud", "nombre_solicitante", "ciudad"}


def cargar_solicitudes(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for fila in filas:
        for col, val in fila.items():
            if col not in COLUMNAS_TEXTO:
                fila[col] = int(val)
    return filas


def evaluar(s):
    if s["edad"] < 18 or s["edad"] > 80:
        return {"decision": "RECHAZADO", "motivo": "edad fuera de rango"}

    if s["cheques_rechazados_12m"] > 3:
        return {"decision": "RECHAZADO", "motivo": "cheques rechazados en 12 meses"}

    if s["scoring"] < 600:
        return {"decision": "RECHAZADO", "motivo": "scoring bajo"}

    if s["scoring"] > 700:
        tope, plazo_max = 500000, 24
    else:
        tope, plazo_max = 200000, 12

    if s["monto_solicitado"] > tope:
        return {"decision": "RECHAZADO", "motivo": "monto supera el tope"}

    cuota = s["monto_solicitado"] / s["plazo_meses"]
    if cuota > s["ingreso_mensual"] * 0.35:
        return {"decision": "RECHAZADO", "motivo": "cuota supera el 35% del ingreso"}

    return {"decision": "APROBADO", "motivo": "ok"}


def main():
    solicitudes = cargar_solicitudes("datos/solicitudes.csv")
    resultados = []
    for s in solicitudes:
        try:
            r = evaluar(s)
            resultados.append({**s, **r})
        except Exception:
            pass

    os.makedirs("salida", exist_ok=True)
    with open("salida/resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        w.writeheader()
        w.writerows(resultados)
    print("Listo")


if __name__ == "__main__":
    main()
