
import streamlit as st
import pandas as pd
from motor_corregido import calcular_salario, buscar_cargo_por_codigo_o_nombre

st.set_page_config(page_title="Simulador Salarial Docente TDF", layout="centered")

st.title("🧮 Simulador Salarial Docente – Tierra del Fuego")

st.markdown("### Valor Índice Fijo (VI): 89.36004")
VI = 89.36004

antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0, step=1)

st.markdown("## 🛠️ Carga de hasta 4 espacios de cargos/horas")

cargos_seleccionados = []

for i in range(4):
    st.markdown(f"### Espacio #{i+1}")
    entrada = st.text_input(f"Buscar por código o nombre", key=f"busqueda_{i}")
    cantidad = st.number_input("Cantidad", min_value=0, max_value=54, value=0, step=1, key=f"cantidad_{i}")

    if entrada and cantidad > 0:
        resultados = buscar_cargo_por_codigo_o_nombre(entrada)
        if not resultados.empty:
            codigo_seleccionado = int(resultados.iloc[0]["codigo"])
            cargos_seleccionados.append({
                "codigo": codigo_seleccionado,
                "cantidad": cantidad
            })
        else:
            st.warning("❌ No se encontró el código o nombre ingresado.")

st.markdown("## 📌 Selección de gremios (máximo 2)")
gremio1 = st.selectbox("Gremio 1", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)
gremio2 = st.selectbox("Gremio 2", ["Ninguno", "AMET", "SADOP", "SUTEF"], index=0)

if st.button("Calcular sueldo"):
    if not cargos_seleccionados:
        st.error("Debe ingresar al menos un cargo.")
    else:
        total, detalle = calcular_salario(antiguedad, cargos_seleccionados)

        st.markdown("## 📊 Resultados")
        st.write(f"**Total Remunerativo Estimado:** ${total:,.2f}")

        st.markdown("## 🧾 Detalle por cargo")
        for item in detalle:
            st.markdown(f"**Código {item['codigo']} x{item['cantidad']}**")
            st.write(f"Cargo: {item['cargo']}")
            st.write(f"Puntaje: {item['puntaje']}")
            st.write(f"Básico: ${item['basico']:,.2f}")
            st.write(f"Función: ${item['funcion']:,.2f}")
            st.write(f"Antigüedad: ${item['antiguedad']:,.2f}")
            st.write(f"Subtotal: ${item['subtotal']:,.2f}")
