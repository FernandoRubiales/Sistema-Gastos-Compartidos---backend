from decimal import Decimal
from django.db import transaction

#Servicio que maneja la logica de negocio de gastos
class GastoService:
    @staticmethod
    @transaction.atomic  #no deja datos inconsistentes
    def crearGastoCompleto(creador, datos):
        #Primero extraemos los datos del formulario
        titulo = datos.get('titulo')
        monto_total = Decimal(str(datos.get('montoTotalGasto')))
        division_tipo = datos.get('division_tipo', Gasto.DIVISION_EQUITATIVA)
        participantes_datos = datos.get('participantes', [])
        