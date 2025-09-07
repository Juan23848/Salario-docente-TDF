
import pandas as pd

# Cargar tabla de cargos
tabla_cargos = pd.read_csv("cargos_filtrados.csv")

def buscar_cargo_por_codigo_o_nombre(entrada):
    entrada = entrada.lower().strip()
    resultados = tabla_cargos[
        tabla_cargos["codigo"].astype(str).str.contains(entrada) |
        tabla_cargos["cargo"].str.lower().str.contains(entrada)
    ]
    return resultados

def calcular_salario(antiguedad, cargos):
    total = 0
    detalle = []
    for cargo in cargos:
        codigo = cargo["codigo"]
        cantidad = cargo["cantidad"]
        datos = tabla_cargos[tabla_cargos["codigo"] == codigo]
        if datos.empty:
            continue
        puntaje = datos.iloc[0]["puntaje"]
        basico = puntaje * 89.36004
        funcion = basico * 2.3
        antig = basico * (0.01 * antiguedad)
        subtotal = (basico + funcion + antig) * cantidad
        total += subtotal
        detalle.append({
            "codigo": codigo,
            "cargo": datos.iloc[0]["cargo"],
            "cantidad": cantidad,
            "puntaje": puntaje,
            "basico": basico,
            "funcion": funcion,
            "antiguedad": antig,
            "subtotal": subtotal
        })
    return total, detalle
