
import streamlit as st
import pandas as pd
from motor import (
    calcular_remunerativos_multiples,
    calcular_foid,
    calcular_ayuda_material,
    calcular_descuentos
)

st.set_page_config(page_title="Simulador Salarial Docente", layout="centered")
st.title("📘 Simulador Salarial Docente – Tierra del Fuego")

# --- Cargar tabla de cargos ---
cargos_df = pd.read_csv("Tabla_de_cargos.csv")
cargos_df["opcion"] = cargos_df["codigo"].astype(str) + " - " + cargos_df["cargo"]

# --- Parámetros fijos ---
valor_indice = 89.36004
st.markdown(f"**Valor Índice Fijo (VI):** {valor_indice}")

antiguedad = st.number_input("Años de antigüedad", min_value=0, max_value=50, value=0)
cargos_simples = st.number_input("Cantidad de cargos simples", min_value=0, max_value=2, value=0)
horas_catedra = st.number_input("Cantidad de horas cátedra", min_value=0, max_value=54, value=0)

st.subheader("🛠️ Carga de hasta 4 espacios de cargos/horas")

cargos = []
for i in range(4):
    st.markdown(f"**Espacio #{i+1}**")
    col1, col2 = st.columns([4, 1])
    with col1:
        seleccion = st.selectbox("Buscar por código o nombre", cargos_df["opcion"], key=f"cargo_{i}")
    with col2:
        cantidad = st.number_input("Cantidad", min_value=0, max_value=10, step=1, key=f"cantidad_{i}")

    codigo = str(cargos_df.loc[cargos_df["opcion"] == seleccion, "codigo"].values[0])
    puntaje = float(cargos_df.loc[cargos_df["opcion"] == seleccion, "puntaje"].values[0])
    if cantidad > 0:
        cargos.append({"codigo": codigo, "puntaje": puntaje, "cantidad": cantidad})

# --- Gremios ---
st.subheader("📌 Selección de gremios (máximo 2)")
colg1, colg2 = st.columns(2)
gremio1 = colg1.selectbox("Gremio 1", ["Ninguno", "AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])
gremio2 = colg2.selectbox("Gremio 2", ["Ninguno", "AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])
gremios = [g for g in [gremio1, gremio2] if g != "Ninguno"]

# --- Botón principal ---
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

    # --- Validación acumulación (Ley 761) ---
    total_horas = horas_catedra + cargos_simples * 15  # suposición: cada cargo simple ~15 hs
    if total_horas > 54:
        st.error("❌ Exceso de carga: supera el máximo legal de 54 horas (incluso con excepción).")
    elif total_horas > 42:
        st.warning("⚠️ Advertencia: está excediendo el máximo general de 42 horas. Solo permitido por excepción.")
    else:
        st.info("✅ Dentro del régimen legal de acumulación (Ley 761).")
