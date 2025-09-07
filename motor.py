from antiguedad import calcular_antiguedad_factor

# --- Gremios y descuentos sindicales ---
GREMIOS = {
    "AMET": 0.015,    # 1.5%
    "SUTEF": 0.02,    # 2.0%
    "SUETRA": 0.02,   # 2.0%
    "ATE": 0.022,     # 2.2%
    "UDAF": 0.013,    # 1.3%
    "UDA": 0.015,     # 1.5%
    "UPCN": 0.022     # 2.2%
}

# --- Códigos especiales ---
BONIF_DOCENTE = {101, 102, 201}   # Ejemplo, reemplazar con los códigos reales
JERARQUICOS = {301, 302, 303}     # Ejemplo, reemplazar con los códigos reales


# --- Cálculo de remunerativos ---
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


# --- Cálculo de FOID ---
def calcular_foid(cargos_simples, horas_catedra):
    # máximo 90.000
    monto_cargos = min(cargos_simples, 2) * 45000
    monto_horas = min(horas_catedra, 30) * 3000
    return min(monto_cargos + monto_horas, 90000)


# --- Cálculo de Ayuda Material ---
def calcular_ayuda_material(cargos_simples, horas_catedra):
    # $71.300 por cargo simple (máx 2) o proporcional en horas cátedra
    monto_cargos = min(cargos_simples, 2) * 71300

    valor_hora = 71300 / 19
    if horas_catedra <= 19:
        monto_horas = horas_catedra * valor_hora
    elif horas_catedra <= 38:
        monto_horas = horas_catedra * valor_hora
    else:
        monto_horas = 142600

    return max(monto_cargos, monto_horas)


# --- Descuentos obligatorios + gremiales ---
def calcular_descuentos(bruto_remunerativo, gremios=None):
    if gremios is None:
        gremios = []

    jubilacion = bruto_remunerativo * 0.16
    obra_social = bruto_remunerativo * 0.03
    seguro = 3000

    descuentos_gremiales = []
    for g in gremios[:2]:  # solo hasta 2 gremios
        if g in GREMIOS:
            monto = bruto_remunerativo * GREMIOS[g]
            descuentos_gremiales.append((g, monto))

    total_gremial = sum(monto for _, monto in descuentos_gremiales)
    total = jubilacion + obra_social + seguro + total_gremial

    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "gremiales": descuentos_gremiales,
        "total": total
    }
