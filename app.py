
import streamlit as st
import pandas as pd
from motor import calcular_salario  # solo usamos calcular_salario ahora

# Configuración de la página
st.set_page_config(page_title="Simulador Docente TDF", layout="centered")

st.title("📊 Simulador Salarial Docente - Tierra del Fuego")

# Valor índice fijo
st.markdown("### Valor Índice Fijo (VI): 89.36004")
VI = 89.36004

# Antigüedad
antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0, step=1)

st.markdown("### ➕ Carga de hasta 4 espacios de cargos/horas")

# Cargar la tabla de cargos
cargos_df = pd.read_csv("Tabla_de_cargos.csv")
cargos_df["opcion"] = cargos_df["codigo"].astype(str) + " - " + cargos_df["nombre"]

cargos_seleccionados = []

# Interfaz de selección de hasta 4 cargos
for i in range(4):
    st.markdown(f"#### Espacio #{i+1}")

    # Selectbox con autocompletado dinámico
    cargo_seleccionado = st.selectbox(
        f"Seleccionar cargo/horas para espacio {i+1}",
        options=[""] + list(cargos_df["opcion"]),
        index=0,
        key=f"cargo_{i}"
    )

    cantidad = st.number_input(
        f"Cantidad (hs/cargos) para espacio {i+1}",
        min_value=0,
        max_value=54,
        value=0,
        step=1,
        key=f"cantidad_{i}"
    )

    if cargo_seleccionado != "" and cantidad > 0:
        cargo_info = cargos_df[cargos_df["opcion"] == cargo_seleccionado].iloc[0]
        cargos_seleccionados.append({
            "codigo": int(cargo_info["codigo"]),
            "nombre": cargo_info["nombre"],
            "cantidad": cantidad,
            "puntaje": cargo_info["puntaje"]  # si lo usás en motor.py
        })

# Selección de gremios
st.markdown("### 🏛 Selección de gremios (máximo 2)")
gremio1 = st.selectbox("Gremio 1", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)
gremio2 = st.selectbox("Gremio 2", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)

# Botón de cálculo
if st.button("Calcular sueldo"):
    if not cargos_seleccionados:
        st.error("⚠️ Debe ingresar al menos un cargo.")
    else:
        resultado = calcular_salario(cargos_seleccionados, antiguedad, gremio1, gremio2, VI)
        st.markdown("## 🧾 Resultado del cálculo")
        st.write(resultado)
