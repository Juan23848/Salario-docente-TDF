
def calcular_salario(codigos_cantidad, antiguedad, gremios):
    resultados = []
    total_remunerativo = 0
    total_descuentos = 0
    total_neto = 0
    vi = 89.36  # Valor índice fijo

    puntajes = {
        312: 68.23,
        421: 68.23,
        456: 68.23,
        852: 68.23,
        100: 68.23
    }

    for codigo, cantidad in codigos_cantidad:
        if cantidad == 0:
            continue
        puntaje = puntajes.get(codigo, 68.23)
        basico_unitario = puntaje * vi
        funcion_unitaria = basico_unitario * 2.3
        transformacion_unitaria = basico_unitario * 1.23
        antiguedad_unitaria = basico_unitario * (antiguedad * 0.07)

        basico = basico_unitario * cantidad
        funcion = funcion_unitaria * cantidad
        transformacion = transformacion_unitaria * cantidad
        antiguedad_total = antiguedad_unitaria * cantidad

        subtotal = basico + funcion + transformacion + antiguedad_total
        total_remunerativo += subtotal

        resultados.append({
            'codigo': codigo,
            'cantidad': cantidad,
            'puntaje': puntaje,
            'basico': basico,
            'funcion': funcion,
            'transformacion': transformacion,
            'antiguedad': antiguedad_total,
            'subtotal': subtotal
        })

    # Agregados fijos
    foid = 90000
    ayuda_material = 142600
    total_remunerativo += foid + ayuda_material

    # Descuentos
    descuento_jubilacion = total_remunerativo * 0.16
    descuento_obra_social = total_remunerativo * 0.03
    descuento_seguro = 3000
    descuento_gremial = 0
    if "AMET" in gremios:
        descuento_gremial += total_remunerativo * 0.02
    if "SUTEF" in gremios:
        descuento_gremial += total_remunerativo * 0.02

    total_descuentos = descuento_jubilacion + descuento_obra_social + descuento_seguro + descuento_gremial
    total_neto = total_remunerativo - total_descuentos

    return {
        "detalles": resultados,
        "foid": foid,
        "ayuda_material": ayuda_material,
        "total_remunerativo": total_remunerativo,
        "descuentos": {
            "jubilacion": descuento_jubilacion,
            "obra_social": descuento_obra_social,
            "seguro_vida": descuento_seguro,
            "gremial": descuento_gremial,
            "total": total_descuentos
        },
        "neto": total_neto
    }
