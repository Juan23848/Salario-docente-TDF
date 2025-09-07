
import streamlit as st
import pandas as pd
from motor import (
    calcular_remunerativos_multiples,
    calcular_foid,
    calcular_ayuda_material,
    calcular_descuentos
)

st.set_page_config(page_title="Simulador Salarial Docente", layout="centered")
st.title("📘 Simulador Salarial Docente – Tierra del Fuego (Multicargo)")

# --- Cargar tabla de cargos ---
cargos_df = pd.read_csv("Tabla_de_cargos.csv")

valor_indice = st.number_input("Valor índice (actual)", value=89.36004)
antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0)
cargos_simples = st.number_input("Cantidad de cargos simples", min_value=0, max_value=2, value=0)
horas_catedra = st.number_input("Cantidad de horas cátedra", min_value=0, max_value=40, value=0)

gremios = st.multiselect("Seleccioná gremios", options=["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

st.subheader("➕ Selección de múltiples cargos")
num_cargos = st.number_input("¿Cuántos cargos querés cargar?", min_value=1, max_value=10, value=3)

cargos = []
for i in range(int(num_cargos)):
    st.markdown(f"**Cargo #{i+1}**")
    col1, col2 = st.columns([3, 1])
    with col1:
        cargo = st.selectbox(f"Cargo", cargos_df["cargo"], key=f"cargo_{i}")
    with col2:
        cantidad = st.number_input("Cantidad", min_value=0, max_value=10, step=1, key=f"cantidad_{i}")

    codigo = cargos_df.loc[cargos_df["cargo"] == cargo, "codigo"].values[0]
    puntaje = cargos_df.loc[cargos_df["cargo"] == cargo, "puntaje"].values[0]
    cargos.append({"codigo": str(codigo), "puntaje": float(puntaje), "cantidad": int(cantidad)})

if st.button("Calcular sueldo"):
    st.subheader("📊 Resultados")

    remunerativo, detalle = calcular_remunerativos_multiples(cargos, valor_indice, antiguedad)
    st.write(f"**Total Remunerativo:** ${remunerativo:,.2f}")

    st.subheader("🧾 Detalle por cargo")
    for item in detalle:
        st.markdown(f"**Código {item['codigo']} x{item['cantidad']}**")
        for k, v in item.items():
            if k not in {"codigo", "cantidad"}:
                st.write(f"{k.replace('_', ' ').capitalize()}: ${v:,.2f}")

    foid = calcular_foid(cargos_simples, horas_catedra)
    ayuda = calcular_ayuda_material(cargos_simples, horas_catedra)
    st.write(f"**FOID:** ${foid:,.2f}")
    st.write(f"**Ayuda Material:** ${ayuda:,.2f}")

    descuentos = calcular_descuentos(remunerativo, gremios)
    st.subheader("📉 Descuentos")
    st.write(f"Jubilación (16%): -${descuentos['jubilacion']:,.2f}")
    st.write(f"Obra Social (3%): -${descuentos['obra_social']:,.2f}")
    st.write(f"Seguro de Vida: -${descuentos['seguro']:,.2f}")
    if descuentos["gremiales"]:
        for gremio, monto in descuentos["gremiales"].items():
            st.write(f"{gremio}: -${monto:,.2f}")
    st.write(f"**Total Descuentos:** -${descuentos['total']:,.2f}")

    neto = remunerativo - descuentos["total"] + foid + ayuda
    st.subheader("💰 Sueldo Neto Estimado")
    st.success(f"${neto:,.2f}")
