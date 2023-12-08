import csv
import os
from collections import defaultdict


class ProcesadorCSV:
    def __init__(self, archivo_csv):
        #self.archivo_csv = archivo_csv
        self.archivo_csv = os.path.join(os.path.dirname(__file__), 'transacciones.csv')
        self.transacciones = []
    
    def cargar_transacciones(self):
        with open(self.archivo_csv, newline='') as archivo:
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv:
                fecha = fila['Date']
                monto = float(fila['Transaccion'])
                self.transacciones.append((fecha, monto))

    def procesar_transacciones(self):
        saldo = 0.0
        for fecha, monto in self.transacciones:
            saldo += monto

        return saldo

    def generar_resumen(self):
        saldo_total = self.procesar_transacciones()
        transacciones_por_mes = defaultdict(list)

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

        for mes, montos in transacciones_por_mes.items():
            num_transacciones = len(montos)
            monto_promedio_credito = sum(monto for monto in montos if monto > 0) / num_transacciones if num_transacciones > 0 else 0
            monto_promedio_debito = sum(monto for monto in montos if monto < 0) / num_transacciones if num_transacciones > 0 else 0

            resumen['Número de transacciones por mes'][mes] = num_transacciones
            resumen['Monto promedio del crédito por mes'][mes] = monto_promedio_credito
            resumen['Monto promedio del débito por mes'][mes] = monto_promedio_debito

            # Acumular débitos para el cálculo del Importe medio del débito
            total_debito += sum(monto for monto in montos if monto < 0)
            total_transacciones_debito += num_transacciones

        # Calcular el Importe medio del débito
        resumen['Importe medio del débito'] = total_debito / total_transacciones_debito if total_transacciones_debito > 0 else 0

        return resumen
    
    


