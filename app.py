import streamlit as st
import pandas as pd
from motor import calcular_remunerativo, calcular_foid, calcular_ayuda_material, calcular_descuentos

# Título
st.title("SIMULADOR SALARIAL DOCENTE V1.0")

# --- Cargar datos de cargos ---
cargos_df = pd.read_csv("Tabla_de_cargos.csv")

# Entrada de datos
valor_indice = st.number_input("Valor índice (actual)", value=89.36004)
antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0)

cargo = st.selectbox("Seleccioná el cargo", cargos_df["cargo"])
cargo_codigo = cargos_df.loc[cargos_df["cargo"] == cargo, "codigo"].values[0]
puntaje = cargos_df.loc[cargos_df["cargo"] == cargo, "puntaje"].values[0]

cargos_simples = st.number_input("Cantidad de cargos simples", min_value=0, max_value=2, value=0)
horas_catedra = st.number_input("Cantidad de horas cátedra", min_value=0, max_value=40, value=0)

# Calcular remunerativos
if st.button("Calcular"):
    remunerativos = calcular_remunerativo(cargo_codigo, puntaje, antiguedad, valor_indice)

    st.subheader("Remunerativos")
    for k, v in remunerativos.items():
        st.write(f"{k}: ${v:,.2f}")

    # No remunerativos
    foid = calcular_foid(cargos_simples, horas_catedra)
    ayuda = calcular_ayuda_material(cargos_simples, horas_catedra)

    st.subheader("No Remunerativos")
    st.write(f"FOID: ${foid:,.2f}")
    st.write(f"Refuerzo Ayuda Material Didáctico: ${ayuda:,.2f}")

    # Descuentos
    descuentos = calcular_descuentos(remunerativos["total"])
    
st.subheader("Descuentos Obligatorios")
 st.write(f"Jubilación: -${descuentos['jubilacion']:,.2f}")
 st.write(f"Obra Social: -${descuentos['obra_social']:,.2f}")
 st.write(f"Seguro de Vida: -${descuentos['seguro']:,.2f}")

if descuentos["gremiales"]:
    st.subheader("Descuentos Gremiales")
    for gremio, monto in descuentos["gremiales"]:
        st.write(f"{gremio}: -${monto:,.2f}")

st.subheader("Total Descuentos")
st.write(f"-${descuentos['total']:,.2f}")

    # Neto
neto = remunerativos["total"] - descuentos["total"] + foid + ayuda
st.subheader("💰 Sueldo Neto")
st.write(f"${neto:,.2f}")





