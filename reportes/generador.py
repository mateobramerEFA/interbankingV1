"""
generador.py
Genera un único Excel en memoria con todos los movimientos de cuentas seleccionadas.
"""

import io
import importlib
from datetime import datetime

import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from auth import obtener_token


# ─────────────────────────────────────────────
# CONFIG EMPRESAS
# ─────────────────────────────────────────────

EMPRESAS = {
    "eliantus": {
        "cuentas": "srcELIANTUS.CodigoBancosEliantus",
        "movimientos": "srcELIANTUS.MovimientosEliantus",
        "func_movimientos": "obtener_extractos_Eliantus",
    },
    "elementa": {
        "cuentas": "srcELEMENTA.CodigoBancosElementa",
        "movimientos": "srcELEMENTA.MovimientosElementa",
        "func_movimientos": "obtener_extractos_Elementa",
    },
    "integra": {
        "cuentas": "srcINTEGRA.CodigoBancosINTEGRA",
        "movimientos": "srcINTEGRA.MovimientosIntegra",
        "func_movimientos": "obtener_extractos_Integra",
    },
}


def cargar_modulos(empresa):
    config = EMPRESAS[empresa]

    mod_cuentas = importlib.import_module(config["cuentas"])
    mod_mov = importlib.import_module(config["movimientos"])

    CUENTAS = mod_cuentas.CUENTAS
    obtener_extractos = getattr(mod_mov, config["func_movimientos"])

    return CUENTAS, obtener_extractos


# ─────────────────────────────────────────────
# ESTILOS EXCEL
# ─────────────────────────────────────────────

HEADER_FILL   = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT   = Font(bold=True, color="FFFFFF")
SALDO_FILL    = PatternFill("solid", fgColor="D6E4F0")
SALDO_FONT    = Font(bold=True, color="1F4E79")
SUBTOTAL_FILL = PatternFill("solid", fgColor="EBF5FB")
SUBTOTAL_FONT = Font(bold=True)
ACCOUNT_FILL  = PatternFill("solid", fgColor="FFF2CC")
ACCOUNT_FONT  = Font(bold=True, color="7B6000")
NUMBER_FORMAT = '#,##0.00'


def _aplicar_fila(ws, row_num, fill, font):
    for cell in ws[row_num]:
        cell.fill = fill
        cell.font = font


def _escribir_cuenta(ws, cuenta, statements, desde, hasta):
    ws.append([f"▶ {cuenta.nombre}  ({desde} → {hasta})",
               None, None, None, None, None, None, None, None])
    _aplicar_fila(ws, ws.max_row, ACCOUNT_FILL, ACCOUNT_FONT)

    ws.append(["Fecha", "Importe", "Tipo", "CUIT", "Descripcion",
               "Saldo Inicial", "Saldo Final", "Total Débitos", "Total Créditos"])

    for cell in ws[ws.max_row]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center")

    statements = sorted(statements, key=lambda x: x["operation_date"])

    for statement in statements:
        fecha_op = statement["operation_date"][:10]
        anio, mes_s, dia = fecha_op.split("-")
        fecha_fmt = f"{dia}/{mes_s}/{anio}"

        opening    = statement.get("opening_balance") or 0
        ending     = statement.get("ending_balance")
        deb_total  = statement.get("debits_total_amount")
        cred_total = statement.get("credits_total_amount")
        movimientos = statement.get("movement_detail", [])

        if not movimientos:
            ws.append([fecha_fmt, None, "RESUMEN DIA", None, "(sin movimientos)",
                        opening, ending, deb_total, cred_total])
            _aplicar_fila(ws, ws.max_row, SUBTOTAL_FILL, SUBTOTAL_FONT)
            continue

        saldo_corriente = opening

        for mov in sorted(movimientos, key=lambda x: x.get("process_date", "")):
            importe = mov.get("amount") or 0
            saldo_ini = saldo_corriente
            saldo_fin = saldo_corriente + importe
            saldo_corriente = saldo_fin

            descripcion = " | ".join(filter(None, [
                mov.get("code_description_bank"),
                mov.get("code_description_ib"),
                mov.get("code_description_standard"),
            ]))

            ws.append([fecha_fmt, importe, mov.get("debit_credit_type"),
                        mov.get("customer_cuit"), descripcion,
                        saldo_ini, saldo_fin, None, None])

        ws.append([fecha_fmt, None, "RESUMEN DIA", None, None,
                    opening, ending, deb_total, cred_total])
        _aplicar_fila(ws, ws.max_row, SALDO_FILL, SALDO_FONT)

    ws.append([])


def _aplicar_formato_hoja(ws):
    col_numericas = [2, 6, 7, 8, 9]

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            if cell.column in col_numericas and isinstance(cell.value, (int, float)):
                cell.number_format = NUMBER_FORMAT

    for col_letra, ancho in {
        "A": 13, "B": 16, "C": 12, "D": 16,
        "E": 45, "F": 17, "G": 17, "H": 17, "I": 17,
    }.items():
        ws.column_dimensions[col_letra].width = ancho

    ws.freeze_panes = "A2"


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def generar_excel(empresa: str, desde: str, hasta: str, cuentas_seleccionadas=None):

    secrets = st.secrets[empresa]

    CUENTAS, obtener_extractos = cargar_modulos(empresa)
    token = obtener_token(secrets)

    wb = Workbook()
    ws = wb.active
    ws.title = "Extractos"

    hubo_datos = False

    cuentas_a_usar = cuentas_seleccionadas if cuentas_seleccionadas else CUENTAS

    resultados = []

    for cuenta in cuentas_a_usar:
        try:
            _, statements = obtener_extractos(cuenta, token, desde, hasta, secrets)

            if not statements:
                resultados.append((cuenta, False))
                continue

            resultados.append((cuenta, True))
            hubo_datos = True

            _escribir_cuenta(ws, cuenta, statements, desde, hasta)

        except Exception:
            resultados.append((cuenta, False))

    if not hubo_datos:
        ws.append(["Sin movimientos para el período seleccionado."])

    _aplicar_formato_hoja(ws)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    return buf.read(), resultados