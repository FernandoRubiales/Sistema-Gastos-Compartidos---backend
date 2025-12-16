from decimal import Decimal
from django.db import transaction
from gastosCompartidos.gestion.models import Gasto, Participante
from django.core.exceptions import ValidationError


#-----Servicio que maneja la logica de negocio de gastos-----
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
                monto_a_pagar = monto_cada_participante[i])
        return gasto
    
    #Funcion que valida las reglas de negocio
    def validarDatosGastos(monto_total, participantes_datos, division_tipo):
        #Tiene que haber dos participantes minimos para realizar un gasto compartido
        if len(participantes_datos < 2):
            raise ValidationError("El gasto debe tener al menos 2 participantes")                   #con raise lanzamos el error si falla
        
        #La suma del monto pagado, debe ser menor o igual al monto_total
        suma_pagada = Decimal('0.00')
        for p in participantes_datos:
            monto_pagado = Decimal(str(p.get('montoPagado', 0)))
            suma_pagada = suma_pagada + monto_pagado

        if (suma_pagada > monto_total):
            raise ValidationError("La suma de montos pagados no puede ser mayor al monto total de la cuenta")
        
        #Si la division es personalizada, validar los montos
        if division_tipo == Gasto.DIVISION_PERSONALIZADA:
            for participante in participantes_datos:
                if 'monto_a_pagar' not in participante:
                    raise ValidationError("Si la division es personalizada, debes especificar monto a pagar para cada participante")
                
            #La suma de los montos a pagar debe ser igual al total
            suma_debe_pagar = sum(
                Decimal(str(p['monto_a_pagar'])) 
                for p in participantes_datos
            )

            if (suma_debe_pagar != monto_total):
                raise ValidationError("La suma de montos a pagar debe ser igual al monto total")

    #Funcion para calcular los montos que tiene que pagar cada participante
    def calcular_montos_pagar(monto_total, num_participantes, division_tipo, participantes_datos):

        if division_tipo == Gasto.DIVISION_EQUITATIVA:
            monto_por_persona = monto_total / num_participantes
            return [monto_por_persona] * num_participantes
        
        elif division_tipo == Gasto.DIVISION_PERSONALIZADA:
            
            return [
                Decimal(str(p['monto_a_pagar'])) 
                for p in participantes_data
            ]
        
        else:
            raise ValidationError(f"Tipo de división inválido")