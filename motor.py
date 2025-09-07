
from antiguedad import calcular_antiguedad_factor

GREMIOS = {
    "AMET": 0.015, "SUTEF": 0.02, "SUETRA": 0.02,
    "ATE": 0.022, "UDAF": 0.013, "UDA": 0.015, "UPCN": 0.022
}

BONIF_DOCENTE = {"2001", "3001"}
JERARQUICOS = {"1001", "1002"}

def calcular_remunerativos_multiples(cargos, valor_indice, antiguedad):
    total_remunerativo = 0.0
    detalle = []

    for c in cargos:
        codigo = c["codigo"]
        puntaje = c["puntaje"]
        cant = c["cantidad"]

        basico = puntaje * valor_indice * cant
        funcion = basico * 2.30
        transformacion = basico * 1.23
        antig = basico * calcular_antiguedad_factor(antiguedad)
        bonif_docente = basico * 0.2775 if codigo in BONIF_DOCENTE else 0.0
        adic_jerarquico = basico * 0.30 if codigo in JERARQUICOS else 0.0

        subtotal = basico + funcion + transformacion + antig + bonif_docente + adic_jerarquico
        total_remunerativo += subtotal

        detalle.append({
            "codigo": codigo,
            "cantidad": cant,
            "basico": basico,
            "funcion": funcion,
            "transformacion": transformacion,
            "antiguedad": antig,
            "bonif_docente": bonif_docente,
            "adic_jerarquico": adic_jerarquico,
            "subtotal": subtotal
        })

    return total_remunerativo, detalle

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

def calcular_descuentos(remunerativo, gremios):
    jubilacion = remunerativo * 0.16
    obra_social = remunerativo * 0.03
    seguro = 3000
    gremiales = {g: remunerativo * GREMIOS[g] for g in gremios if g in GREMIOS}
    total = jubilacion + obra_social + seguro + sum(gremiales.values())

    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "gremiales": gremiales,
        "total": total
    }
