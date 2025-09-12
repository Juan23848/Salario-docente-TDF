
import pandas as pd

# ---------------------------
# Función principal de cálculo
# ---------------------------
def calcular_salario(cargos, antiguedad, gremio1, gremio2, VI):
    """
    cargos: lista de diccionarios con {codigo, nombre, cantidad, puntaje}
    antiguedad: años de antigüedad docente
    gremio1, gremio2: strings con el gremio seleccionado
    VI: valor índice fijo
    """

    # ---------------------------
    # Validaciones legales
    # ---------------------------
    total_horas = sum(c["cantidad"] for c in cargos)
    advertencias = []
    if total_horas > 54:
        advertencias.append("❌ Supera el máximo absoluto de 54 horas.")
    elif total_horas > 48:
        advertencias.append("⚠️ Supera el máximo excepcional de 48 horas.")
    elif total_horas > 42:
        advertencias.append("⚠️ Supera el máximo general de 42 horas.")

    # ---------------------------
    # Cálculo de haberes
    # ---------------------------
    basico = sum(c["puntaje"] * VI * c["cantidad"] for c in cargos)
    funcion = basico * 0.10  # Ejemplo: 10% adicional
    transformacion = basico * 0.05
    antiguedad_monto = basico * (antiguedad * 0.01)
    foid = basico * 0.02
    ayuda_material = 5000  # fijo, ejemplo

    bruto = basico + funcion + transformacion + antiguedad_monto + foid + ayuda_material

    # ---------------------------
    # Descuentos legales
    # ---------------------------
    jubilacion = bruto * 0.16
    obra_social = bruto * 0.03
    seguro_vida = 3000

    # ---------------------------
    # Descuentos gremiales
    # ---------------------------
    descuentos_gremiales = 0
    gremios = [g for g in [gremio1, gremio2] if g != "Ninguno"]
    for g in gremios:
        if g in ["AMET", "SADOP", "SUTEF"]:
            descuentos_gremiales += bruto * 0.02  # 2% ejemplo

    descuentos_totales = jubilacion + obra_social + seguro_vida + descuentos_gremiales
    neto = bruto - descuentos_totales

    # ---------------------------
    # Resultado estructurado
    # ---------------------------
    resultado = {
        "Total horas": total_horas,
        "Básico": round(basico, 2),
        "Función": round(funcion, 2),
        "Transformación": round(transformacion, 2),
        "Antigüedad": round(antiguedad_monto, 2),
        "FOID": round(foid, 2),
        "Ayuda material": round(ayuda_material, 2),
        "Bruto": round(bruto, 2),
        "Jubilación (16%)": round(jubilacion, 2),
        "Obra social (3%)": round(obra_social, 2),
        "Seguro de vida": round(seguro_vida, 2),
        "Descuentos gremiales": round(descuentos_gremiales, 2),
        "Descuentos totales": round(descuentos_totales, 2),
        "Neto": round(neto, 2),
        "Advertencias": advertencias
    }

    return resultado

