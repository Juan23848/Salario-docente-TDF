
from antiguedad import calcular_antiguedad_factor

# --- Configuración ---
GREMIOS = {
    "AMET": 0.015,    # 1.5%
    "SUTEF": 0.02,    # 2.0%
    "SUETRA": 0.02,   # 2.0%
    "ATE": 0.022,     # 2.2%
    "UDAF": 0.013,    # 1.3%
    "UDA": 0.015,     # 1.5%
    "UPCN": 0.022     # 2.2%
}

BONIF_DOCENTE = {"2001", "3001"}  # ejemplo de códigos
JERARQUICOS = {"1001", "1002"}    # ejemplo de códigos

# --- Cálculos ---
def calcular_remunerativo(cargo_codigo, puntaje, antiguedad, valor_indice):
    basico = puntaje * valor_indice
    funcion = basico * 2.30
    transformacion = basico * 1.23
    antig = basico * calcular_antiguedad_factor(antiguedad)
    bonif_docente = basico * 0.2775 if cargo_codigo in BONIF_DOCENTE else 0.0
    adic_jerarquico = basico * 0.30 if cargo_codigo in JERARQUICOS else 0.0

    total = basico + funcion + transformacion + antig + bonif_docente + adic_jerarquico

    return {
        "basico": basico,
        "funcion": funcion,
        "transformacion": transformacion,
        "antiguedad": antig,
        "bonif_docente": bonif_docente,
        "adic_jerarquico": adic_jerarquico,
        "total": total
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


def calcular_descuentos(bruto, gremios=[]):
    descuentos = {
        "jubilacion": bruto * 0.16,
        "obra_social": bruto * 0.03,
        "seguro": 3000,
        "gremiales": {}
    }

    for gremio in gremios:
        if gremio in GREMIOS:
            descuentos["gremiales"][gremio] = bruto * GREMIOS[gremio]

    descuentos["total"] = (
        descuentos["jubilacion"]
        + descuentos["obra_social"]
        + descuentos["seguro"]
        + sum(descuentos["gremiales"].values())
    )

    return descuentos
