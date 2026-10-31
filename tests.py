"""Tests de las reglas de negocio de micropréstamos (datos ficticios).

Cada test es un caso armado a mano con su respuesta correcta según CLAUDE.md.
Correr con:  python -m pytest tests.py
"""
from collections import Counter
from pathlib import Path

from evaluar import cargar_solicitudes, evaluar

CSV = Path(__file__).parent / "datos" / "solicitudes.csv"


def decision(**cambios):
    """Solicitud sana (se aprueba) a la que se le cambia solo lo que se quiere probar."""
    s = dict(
        edad=40, ingreso_mensual=1_500_000, cuotas_otras_deudas=0,
        monto_solicitado=150_000, plazo_meses=12, scoring=720,
        cheques_rechazados_3m=0, cheques_rechazados_6m=0, cheques_rechazados_9m=0,
        cheques_rechazados_12m=0, cheques_rechazados_18m=0, cheques_rechazados_24m=0,
        cheques_rechazados_36m=0,
    )
    s.update(cambios)
    return evaluar(s)["decision"]


def test_solicitud_sana_se_aprueba():
    assert decision() == "APROBADO"


def test_scoring_700_exacto_accede_al_tramo_alto():
    assert decision(scoring=700, monto_solicitado=500_000, plazo_meses=24,
                    ingreso_mensual=2_000_000) == "APROBADO"


def test_scoring_599_se_rechaza():
    assert decision(scoring=599) == "RECHAZADO"


def test_monto_sobre_el_tope_del_tramo_medio_se_rechaza():
    assert decision(scoring=650, monto_solicitado=250_000, plazo_meses=12) == "RECHAZADO"


def test_plazo_sobre_el_maximo_del_tramo_medio_se_rechaza():
    assert decision(scoring=650, monto_solicitado=150_000, plazo_meses=18) == "RECHAZADO"


def test_tres_cheques_en_12_meses_rechazan_aunque_el_scoring_sea_alto():
    assert decision(scoring=780, cheques_rechazados_6m=1, cheques_rechazados_9m=1,
                    cheques_rechazados_12m=3, cheques_rechazados_18m=3,
                    cheques_rechazados_24m=3, cheques_rechazados_36m=3) == "RECHAZADO"


def test_seis_cheques_en_36_meses_rechazan():
    assert decision(cheques_rechazados_9m=1, cheques_rechazados_12m=2,
                    cheques_rechazados_18m=3, cheques_rechazados_24m=4,
                    cheques_rechazados_36m=6) == "RECHAZADO"


def test_edad_17_se_rechaza():
    assert decision(edad=17) == "RECHAZADO"


def test_edad_75_se_aprueba():
    assert decision(edad=75) == "APROBADO"


def test_edad_78_se_rechaza():
    assert decision(edad=78) == "RECHAZADO"


def test_cuota_total_justo_en_35_por_ciento_se_aprueba():
    assert decision(scoring=650, monto_solicitado=180_000, plazo_meses=12,
                    ingreso_mensual=1_000_000, cuotas_otras_deudas=335_000) == "APROBADO"


def test_cuota_total_incluye_otras_deudas_y_supera_el_35_por_ciento():
    assert decision(scoring=650, monto_solicitado=180_000, plazo_meses=12,
                    ingreso_mensual=1_000_000, cuotas_otras_deudas=340_000) == "RECHAZADO"


def test_cheque_rechazado_en_los_ultimos_3_meses_va_a_revision_manual():
    assert decision(cheques_rechazados_3m=1, cheques_rechazados_6m=1,
                    cheques_rechazados_9m=1, cheques_rechazados_12m=1,
                    cheques_rechazados_18m=1, cheques_rechazados_24m=1,
                    cheques_rechazados_36m=1) == "REVISION_MANUAL"


def test_totales_del_dataset_completo():
    """Con las reglas bien aplicadas, las 200 solicitudes del CSV dan estos totales."""
    totales = Counter(evaluar(s)["decision"] for s in cargar_solicitudes(CSV))
    assert totales == {"APROBADO": 113, "RECHAZADO": 67, "REVISION_MANUAL": 20}
