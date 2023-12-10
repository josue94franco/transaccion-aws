import csv
import os
from collections import defaultdict


class ProcesadorCSV:
    def __init__(self, archivo_csv):
        #self.archivo_csv = archivo_csv
        self.archivo_csv = os.path.join(os.path.dirname(__file__), 'transacciones.csv')
        self.transacciones = []
    
     # Carga las transacciones desde el archivo CSV y las almacena en la lista transacciones
    def cargar_transacciones(self):
        date = {
            "1": "enero",
            "2": "febrero",
            "3": "marzo",
            "4": "abril",
            "5": "mayo",
            "6": "junio",
            "7": "julio",
            "8": "agosto",
            "9": "septiembre",
            "10": "octubre",
            "11": "noviembre",
            "12": "diciembre"
        }
        with open(self.archivo_csv, newline='') as archivo:
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv:
                fecha = fila['Date']
                monto = float(fila['Transaccion'])
                self.transacciones.append((fecha, monto))

    # Calcula y devuelve el saldo total de todas las transacciones
    def procesar_transacciones(self):
        saldo = 0.0
        for fecha, monto in self.transacciones:
            saldo += monto

        return saldo
    # Genera un resumen financiero que incluye el saldo total, número de transacciones por mes, monto promedio por mes.
    def generar_resumen(self):
        saldo_total = self.procesar_transacciones()
        transacciones_por_mes = defaultdict(list)
        
        # Agrupa las transacciones por mes
        for fecha, monto in self.transacciones:
            mes = fecha.split('/')[0]
            transacciones_por_mes[mes].append(monto)

        resumen = {
            'Saldo total': saldo_total,
            'Número de transacciones por mes': {},
            'Monto promedio del crédito por mes': {},
            'Monto promedio del débito por mes': {},
            'Importe medio del débito': 0.0
        }

        total_debito = 0
        total_transacciones_debito = 0

        # Calcula estadísticas por mes (número de transacciones, monto promedio de crédito y débito)
        for mes, montos in transacciones_por_mes.items():
            num_transacciones = len(montos)
            monto_promedio_credito = sum(monto for monto in montos if monto > 0) / num_transacciones if num_transacciones > 0 else 0
            monto_promedio_debito = sum(monto for monto in montos if monto < 0) / num_transacciones if num_transacciones > 0 else 0

            resumen['Número de transacciones por mes'][mes] = num_transacciones
            resumen['Monto promedio del crédito por mes'][mes] = monto_promedio_credito
            resumen['Monto promedio del débito por mes'][mes] = monto_promedio_debito

            # Acumula débitos para el cálculo del Importe medio del débito
            total_debito += sum(monto for monto in montos if monto < 0)
            total_transacciones_debito += num_transacciones

        # Calcula el Importe medio del débito
        resumen['Importe medio del débito'] = total_debito / total_transacciones_debito if total_transacciones_debito > 0 else 0

        return resumen
    
    


