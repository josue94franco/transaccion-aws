from transaccion import ProcesadorCSV

def generar_y_mostrar_resumen():
    archivo_csv = "transacciones.csv"
    procesador = ProcesadorCSV(archivo_csv)
    procesador.cargar_transacciones()

    resumen = procesador.generar_resumen()

    # Retornar el resumen como cadena de texto
    resumen_str = f"El saldo total es {resumen['Saldo total']:.2f}\n"

    for mes, num_transacciones in resumen['Número de transacciones por mes'].items():
        resumen_str += f"Número de transacciones en {mes}: {num_transacciones}\n"

    for mes, monto_promedio in resumen['Monto promedio del crédito por mes'].items():
        resumen_str += f"Monto promedio del crédito en {mes}: {monto_promedio:.2f}\n"

    for mes, monto_promedio in resumen['Monto promedio del débito por mes'].items():
        resumen_str += f"Monto promedio del débito en {mes}: {monto_promedio:.2f}\n"

    resumen_str += f"Importe medio del débito: {resumen['Importe medio del débito']:.2f}"

    return resumen_str

# Llamada a la función para obtener el resumen
resumen = generar_y_mostrar_resumen()
print(resumen)  






