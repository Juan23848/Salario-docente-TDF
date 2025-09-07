import pandas as pd
from antiguedad import calcular_antiguedad_factor

VALOR_INDICE = 89.36004  # Agosto 2025

BONIF_DOCENTE = {...}  # pegá acá todos los códigos de bonif docente
JERARQUICOS = {...}    # pegá acá todos los códigos jerárquicos

def cargar_cargos(path="data/cargos_mayo_2025.csv"):
    df = pd.read_csv(path, sep=";", encoding="latin1")
    df["puntaje"] = df["puntaje"].astype(str).str.replace(",", ".").astype(float)
    return df

def calcular_remunerativo(cargo_codigo, puntaje, antiguedad):
    basico = puntaje * VALOR_INDICE
    funcion = basico * 2.30
    transformacion = basico * 1.23
    antig = basico * calcular_antiguedad_factor(antiguedad)

    bonif_docente = basico * 0.2775 if cargo_codigo in BONIF_DOCENTE else 0.0
    adic_jerarquico = basico * 0.30 if cargo_codigo in JERARQUICOS else 0.0

    subtotal = basico + funcion + transformacion + antig + bonif_docente + adic_jerarquico
    zona = subtotal
    remunerativo = subtotal + zona

    return {
        "básico": basico,
        "función docente": funcion,
        "transformación educativa": transformacion,
        "antigüedad": antig,
        "bonificación docente": bonif_docente,
        "adicional jerárquico": adic_jerarquico,
        "subtotal": subtotal,
        "zona": zona,
        "remunerativo": remunerativo
    }

def calcular_foid(cargos_simples, horas_catedra):
    if cargos_simples > 0:
        return min(cargos_simples, 2) * 45000
    else:
        return min(horas_catedra, 30) * 3000

def calcular_ayuda_material(cargos_simples, horas_catedra):
    if cargos_simples > 0:
        return min(cargos_simples, 2) * 71300
    else:
        valor_hora = 71300 / 19
        return min(horas_catedra, 38) * valor_hora

def calcular_descuentos(remunerativo):
    jubilacion = remunerativo * 0.16
    obra_social = remunerativo * 0.03
    seguro = 3000
    return {
        "jubilación": jubilacion,
        "obra social": obra_social,
        "seguro": seguro,
        "total": jubilacion + obra_social + seguro
    }
