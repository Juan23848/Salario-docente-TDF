
def calcular_basico(puntaje, valor_indice):
    return puntaje * valor_indice

def calcular_funcion(basico):
    return basico * 2.3

def calcular_transformacion(basico):
    return basico * 1.23

def calcular_antiguedad(basico, anios):
    if anios < 0:
        return 0
    tramos = anios // 2
    porcentaje = min(tramos * 0.10, 1.20)  # Hasta 120%
    return basico * porcentaje

def calcular_remunerativos_multiples(cargos, valor_indice, antiguedad):
    total = 0
    detalle = []

    for cargo in cargos:
        codigo = cargo["codigo"]
        puntaje = cargo["puntaje"]
        cantidad = cargo["cantidad"]

        basico = calcular_basico(puntaje, valor_indice) * cantidad
        funcion = calcular_funcion(basico)
        transformacion = calcular_transformacion(basico)
        ant = calcular_antiguedad(basico, antiguedad)

        subtotal = basico + funcion + transformacion + ant

        detalle.append({
            "codigo": codigo,
            "cantidad": cantidad,
            "puntaje": puntaje,
            "basico": basico,
            "funcion": funcion,
            "transformacion": transformacion,
            "antiguedad": ant,
            "subtotal": subtotal
        })

        total += subtotal

    return total, detalle

def calcular_foid(horas_equivalentes, _):
    if horas_equivalentes >= 15:
        return 90000
    return 0

def calcular_ayuda_material(horas_equivalentes, _):
    if horas_equivalentes >= 15:
        return 142600
    return 0

# Gremios con su porcentaje aplicado sobre el remunerativo
porcentajes_gremios = {
    "AMET": 0.015,
    "SUTEF": 0.01,
    "SUETRA": 0.015,
    "ATE": 0.02,
    "UDAF": 0.01,
    "UDA": 0.01,
    "UPCN": 0.02
}

def calcular_descuentos(remunerativo, gremios):
    descuentos = {
        "jubilacion": remunerativo * 0.16,
        "obra_social": remunerativo * 0.03,
        "seguro": 3000,
        "gremiales": {},
    }

    total_gremial = 0
    for gremio in gremios:
        if gremio in porcentajes_gremios:
            monto = remunerativo * porcentajes_gremios[gremio]
            descuentos["gremiales"][gremio] = monto
            total_gremial += monto

    descuentos["total"] = (
        descuentos["jubilacion"]
        + descuentos["obra_social"]
        + descuentos["seguro"]
        + total_gremial
    )
    return descuentos

# Validación detallada por combinación según Ley 761
def validar_acumulacion(cargos):
    cargos_simples = 0
    cargos_completos = 0
    horas = 0

    for cargo in cargos:
        cod = int(cargo["codigo"])
        cant = cargo["cantidad"]

        # Por ejemplo: códigos mayores a 400 se consideran horas cátedra
        if cod >= 400:
            horas += cant
        else:
            if "completo" in cargo.get("descripcion", "").lower():
                cargos_completos += cant
            else:
                cargos_simples += cant

    total_horas = horas

    # Normal
    if (cargos_simples == 2 and horas <= 6) or        (cargos_completos == 1 and horas <= 16) or        (cargos_simples == 1 and horas <= 22):
        return total_horas, "normal"
    # Excepcional
    elif (cargos_simples == 2 and horas <= 12) or          (cargos_completos == 1 and horas <= 22) or          (cargos_simples == 1 and horas <= 28):
        return total_horas, "excepcional"
    # Máximo total con necesidad
    elif (cargos_simples == 2 and horas <= 18) or          (cargos_completos == 1 and horas <= 28) or          (cargos_simples == 1 and horas <= 34):
        return total_horas, "maximo_extremo"
    # Fuera de norma
    return total_horas, "ilegal"
