"""
generador.py
Genera un ZIP en memoria con un Excel por cuenta seleccionada.
Nombre de cada archivo: EMPRESA_BANCO_DESDE_HASTA.xlsx
"""

import io
import zipfile
import importlib
from datetime import datetime

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


# ─────────────────────────────────────────────
# FUNCIONES DE FORMATO
# ─────────────────────────────────────────────

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


def _formatear_fecha(fecha_iso):
    """Convierte 2026-03-30 a 30-03"""
    anio, mes, dia = fecha_iso.split("-")
    return f"{dia}-{mes}"


def _nombre_archivo(cuenta, desde, hasta):
    """Genera el nombre: BANCO_DD-MM_DD-MM.xlsx"""
    banco = cuenta.banco.replace(" ", "_")
    return f"{banco}_{_formatear_fecha(desde)}_{_formatear_fecha(hasta)}.xlsx"


def _generar_excel_cuenta(cuenta, statements, desde, hasta):
    """Genera un Excel en memoria para una sola cuenta."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracto"
    _escribir_cuenta(ws, cuenta, statements, desde, hasta)
    _aplicar_formato_hoja(ws)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def generar_zip(empresa: str, desde: str, hasta: str, cuentas_seleccionadas=None):
    """
    Genera un ZIP en memoria con un Excel por cuenta.
    Retorna (zip_bytes, resultados).
    """
    CUENTAS, obtener_extractos = cargar_modulos(empresa)
    token, customer_id = obtener_token(empresa)

    cuentas_a_usar = cuentas_seleccionadas if cuentas_seleccionadas else CUENTAS
    resultados = []

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for cuenta in cuentas_a_usar:
            try:
                _, statements = obtener_extractos(cuenta, token, desde, hasta)

                if not statements:
                    print(f"[INFO] {cuenta.nombre} → sin movimientos")
                    resultados.append((cuenta, False))
                    continue

                excel_bytes = _generar_excel_cuenta(cuenta, statements, desde, hasta)
                filename = _nombre_archivo(cuenta, desde, hasta)
                zf.writestr(filename, excel_bytes)
                resultados.append((cuenta, True))
                print(f"[INFO] {cuenta.nombre} → OK ({filename})")

            except Exception as e:
                print(f"[ERROR] {cuenta.nombre}: {e}")
                resultados.append((cuenta, False))

    zip_buf.seek(0)
    return zip_buf.read(), resultados