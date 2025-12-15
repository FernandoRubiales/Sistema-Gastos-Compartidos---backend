from decimal import Decimal
from django.db import transaction
from gastosCompartidos.gestion.models import Gasto, Participante

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
        
        #Validar las reglas de negocio
        GastoService.validarDatosGasto(monto_total= monto_total, participantes_datos = participantes_datos, division_tipo = division_tipo)

        #Crear el gasto en la BD
        gasto = Gasto.objects.create(
            creador = creador, 
            titulo = titulo,
            montoTotalGasto = monto_total,
            division_tipo = division_tipo
        )

        #Calcular el monto para cada participante
        monto_cada_participante = GastoService.calcular_montos_pagar(
            monto_total = monto_total,
            num_participantes = len(participantes_datos),
            division_tipo = division_tipo,
            participantes_datos = participantes_datos
        )

        #Creamos los participantes del gasto
        for i, participantes_datos in enumerate(participantes_datos):
            Participante.objects.create(
                gasto = gasto,
                usuario = participantes_datos.get('usuario'),
                nombreParticipante = participantes_datos['nombre'],
                email_partipante = participantes_datos.get('email',''),
                montoPagado = Decimal(str(participantes_datos.get('montoPagado', 0)))
                monto_a_pagar = monto_cada_participante[i]
            )
        return gasto
    
    #Funcion que valida las reglas de negocio
    