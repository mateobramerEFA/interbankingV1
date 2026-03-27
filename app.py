import streamlit as st
from datetime import date, timedelta
import importlib
from reportes.generador import generar_excel

# ✅ Configuración de la página
st.set_page_config(
    page_title="Interbanking · Reportes",
    page_icon="📊",
    layout="centered",
)

# ─────────────────────────────────────────────
# Usuario ficticio para pruebas (sin login)
# ─────────────────────────────────────────────
user_email = "test@empresa.com"
st.success(f"Bienvenido {user_email} 👋")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("📊 Extractos bancarios")
st.caption("Seleccioná empresa, cuentas y período")

# ─────────────────────────────────────────────
# EMPRESA
# ─────────────────────────────────────────────
empresa = st.selectbox(
    "Empresa",
    options=["eliantus", "elementa", "integra"],
    format_func=lambda x: x.capitalize(),
)

# ─────────────────────────────────────────────
# RESET CUENTAS SI CAMBIA EMPRESA
# ─────────────────────────────────────────────
if "empresa_prev" not in st.session_state:
    st.session_state["empresa_prev"] = empresa

if st.session_state["empresa_prev"] != empresa:
    st.session_state["cuentas"] = []
    st.session_state["empresa_prev"] = empresa

# ─────────────────────────────────────────────
# CARGAR CUENTAS
# ─────────────────────────────────────────────
EMPRESAS_MODULOS = {
    "eliantus": "srcELIANTUS.CodigoBancosEliantus",
    "elementa": "srcELEMENTA.CodigoBancosElementa",
    "integra": "srcINTEGRA.CodigoBancosINTEGRA",
}

mod_cuentas = importlib.import_module(EMPRESAS_MODULOS[empresa])
CUENTAS = mod_cuentas.CUENTAS

# ─────────────────────────────────────────────
# FORMATO CUENTAS
# ─────────────────────────────────────────────
def format_cuenta(c):
    return f"{c.abreviatura} - {c.numero} ({c.banco})"

# ─────────────────────────────────────────────
# SELECTOR DE CUENTAS
# ─────────────────────────────────────────────
st.markdown("### 🏦 Cuentas")
col1, col2 = st.columns(2)

with col1:
    if st.button("Seleccionar todas"):
        st.session_state["cuentas"] = CUENTAS

with col2:
    if st.button("Limpiar selección"):
        st.session_state["cuentas"] = []

default_cuentas = [
    c for c in st.session_state.get("cuentas", [])
    if c in CUENTAS
]

cuentas_seleccionadas = st.multiselect(
    "Elegí las cuentas",
    options=CUENTAS,
    default=default_cuentas,
    format_func=format_cuenta
)

st.session_state["cuentas"] = cuentas_seleccionadas

# ─────────────────────────────────────────────
# FECHAS
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    desde = st.date_input("Desde", value=date.today() - timedelta(days=7))

with col2:
    hasta = st.date_input("Hasta", value=date.today())

# ─────────────────────────────────────────────
# GENERAR REPORTE
# ─────────────────────────────────────────────
if st.button("⬇ Generar reporte", use_container_width=True):

    if not cuentas_seleccionadas:
        st.warning("⚠ Seleccioná al menos una cuenta")
        st.stop()

    if desde > hasta:
        st.error("⚠ La fecha 'Desde' no puede ser mayor que 'Hasta'")
        st.stop()

    with st.spinner("Procesando cuentas..."):

        excel_bytes, resultados = generar_excel(
            empresa=empresa,
            desde=str(desde),
            hasta=str(hasta),
            cuentas_seleccionadas=cuentas_seleccionadas
        )

    # ─────────────────────────────
    # RESULTADOS
    # ─────────────────────────────
    con_mov = [c for c, ok in resultados if ok]
    sin_mov = [c for c, ok in resultados if not ok]

    if con_mov:
        st.success(f"✔ {len(con_mov)} cuentas con movimientos")
    if sin_mov:
        st.warning(f"⚠ {len(sin_mov)} cuentas sin movimientos")

    for cuenta, ok in resultados:
        if ok:
            st.success(f"{cuenta.abreviatura} → con movimientos")
        else:
            st.warning(f"{cuenta.abreviatura} → sin movimientos")

    # ─────────────────────────────
    # DESCARGA
    # ─────────────────────────────
    st.download_button(
        label="📥 Descargar Excel",
        data=excel_bytes,
        file_name=f"reporte_{empresa}_{desde}_{hasta}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )