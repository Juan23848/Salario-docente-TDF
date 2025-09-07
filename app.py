
import streamlit as st
import pandas as pd
from motor import calcular_remunerativo, calcular_foid, calcular_ayuda_material, calcular_descuentos

st.set_page_config(page_title="Simulador Salarial Docente", layout="centered")

st.title("💼 Simulador Salarial Docente – Tierra del Fuego")

# --- Cargar datos de cargos ---
cargos_df = pd.read_csv("Tabla_de_cargos.csv")

# --- Entrada de datos ---
valor_indice = st.number_input("Valor índice (actual)", value=89.36004)
antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0)

st.subheader("🧮 Selección de cargo")
cargo = st.selectbox("Seleccioná el cargo", cargos_df["cargo"])
cargo_codigo = cargos_df.loc[cargos_df["cargo"] == cargo, "codigo"].values[0]
puntaje = cargos_df.loc[cargos_df["cargo"] == cargo, "puntaje"].values[0]

cargos_simples = st.number_input("Cantidad de cargos simples", min_value=0, max_value=2, value=0)
horas_catedra = st.number_input("Cantidad de horas cátedra", min_value=0, max_value=40, value=0)

gremios = st.multiselect("Seleccioná gremios", options=["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

# --- Cálculo ---
if st.button("Calcular sueldo"):
    st.subheader("📊 Resultados")

    # Remunerativos
    remunerativos = calcular_remunerativo(cargo_codigo, puntaje, antiguedad, valor_indice)
    for k, v in remunerativos.items():
        st.write(f"{k.replace('_',' ').capitalize()}: ${v:,.2f}")

    # No remunerativos
    foid = calcular_foid(cargos_simples, horas_catedra)
    ayuda = calcular_ayuda_material(cargos_simples, horas_catedra)
    st.write(f"FOID: ${foid:,.2f}")
    st.write(f"Ayuda Material: ${ayuda:,.2f}")

    # Descuentos
    descuentos = calcular_descuentos(remunerativos["total"], gremios)
    st.subheader("📉 Descuentos")
    st.write(f"Jubilación (16%): -${descuentos['jubilacion']:,.2f}")
    st.write(f"Obra Social (3%): -${descuentos['obra_social']:,.2f}")
    st.write(f"Seguro de Vida: -${descuentos['seguro']:,.2f}")

    if descuentos["gremiales"]:
        st.write("Descuentos Gremiales:")
        for gremio, monto in descuentos["gremiales"].items():
            st.write(f"- {gremio}: -${monto:,.2f}")

    st.write(f"**Total Descuentos:** -${descuentos['total']:,.2f}")

    # Neto
    neto = remunerativos["total"] - descuentos["total"] + foid + ayuda
    st.subheader("💰 Sueldo Neto Estimado")
    st.success(f"${neto:,.2f}")
