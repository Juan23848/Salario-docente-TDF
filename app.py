
import streamlit as st
from motor import calcular_salario
import pandas as pd

st.set_page_config(page_title="Simulador Salarial Docente - Tierra del Fuego", layout="centered")

st.title("🧮 Simulador Salarial Docente – Tierra del Fuego")

st.subheader("📊 Datos generales")
st.markdown("**Valor Índice Fijo (VI):** 89.36004")
valor_indice = 89.36004  # valor fijo como se pidió

antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=60, step=1)

st.subheader("🛠️ Carga de hasta 4 espacios de cargos/horas")

espacios = []
for i in range(4):
    st.markdown(f"**Espacio #{i+1}**")
    cargo = st.selectbox(f"Buscar por código o nombre", options=[], key=f"cargo_{i}", index=None, placeholder="Escriba código o nombre...")
    cantidad = st.number_input("Cantidad", min_value=0, max_value=54, step=1, key=f"cantidad_{i}")
    if cargo:
        espacios.append({"codigo": cargo.split(" - ")[0], "cantidad": cantidad})

st.subheader("📌 Selección de gremios (máximo 2)")
gremio1 = st.selectbox("Gremio 1", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)
gremio2 = st.selectbox("Gremio 2", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)

gremios = []
if gremio1 != "Ninguno":
    gremios.append(gremio1)
if gremio2 != "Ninguno" and gremio2 != gremio1:
    gremios.append(gremio2)

if st.button("Calcular sueldo"):
    resultado = calcular_salario(valor_indice, antiguedad, espacios, gremios)

    st.subheader("📈 Resultados")
    st.markdown(f"**Total Remunerativo:** ${resultado['total_remunerativo']:,.2f}")

    st.subheader("🧾 Detalle por cargo")
    for detalle in resultado['detalle_cargos']:
        st.markdown(f"**Código {detalle['codigo']} x{detalle['cantidad']}**")
        st.markdown(f"- Puntaje: {detalle['puntaje']}")
        st.markdown(f"- Básico: ${detalle['basico']:,.2f}")
        st.markdown(f"- Función: ${detalle['funcion']:,.2f}")
        st.markdown(f"- Transformación: ${detalle['transformacion']:,.2f}")
        st.markdown(f"- Antigüedad: ${detalle['antiguedad']:,.2f}")
        st.markdown(f"- Bonif docente: ${detalle['bonificacion_docente']:,.2f}")
        st.markdown(f"- Adic jerarquico: ${detalle['adicional_jerarquico']:,.2f}")
        st.markdown(f"- Subtotal: ${detalle['subtotal']:,.2f}")
        st.markdown("---")

    st.markdown(f"**FOID:** ${resultado['foid']:,.2f}")
    st.markdown(f"**Ayuda Material:** ${resultado['ayuda_material']:,.2f}")

    st.subheader("🧾 Descuentos")
    for nombre, valor in resultado["descuentos"].items():
        st.markdown(f"- {nombre}: ${valor:,.2f}")
    st.markdown(f"**Total Descuentos:** ${resultado['total_descuentos']:,.2f}")

    st.subheader("💰 Sueldo Neto Estimado")
    st.success(f"${resultado['sueldo_neto']:,.2f}")

    if resultado['exceso_horas']:
        st.error("❌ Exceso de carga: supera el máximo legal de 54 horas (incluso con excepción).")
