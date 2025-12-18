from rest_framework import serializers
from gastosCompartidos.gestion.models import Gasto, Participante, Transaccion, Usuario
from decimal import Decimal
from django.core.exceptions import ValidationError

class ParticipanteDatosSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    email = serializers.CharField(required=False, allow_blank=True)
    usuario_id = serializers.IntegerField(required=False, allow_null = True)
    montoPagado = serializers.DecimalField(max_digits = 10, decimal_places = 2, default = Decimal('0.00'))

    def validate_montoPagado(self, montoPagado):
        if montoPagado < 0:
            raise ValidationError("El monto pagado por el participante no puede ser negativo")
        return montoPagado


class CrearGastoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=150)
    montoTotalGasto = serializers.DecimalField(max_digits = 10, decimal_places = 2)
    division_tipo = serializers.ChoiceField(choices=['equitativa', 'personalizada'], default = 'equitativa')
    participantes = ParticipanteDatosSerializer(many=True)

    #Debemos validar que el titulo no este vacio, validate lo ejecuta automatica Django
    def validate_titulo(self, titulo):
        titulo_sin_espacios = titulo.strip()

        if titulo_sin_espacios == "":
            raise ValidationError("El titulo no puede estar vacio")
        
        return titulo_sin_espacios
    

    #Debemos validar que el monto total del gasto sea positivo
    def validate_montoTotalGasto(self, montoTotalGasto):
        if montoTotalGasto <= 0:
            raise ValidationError("El monto debe ser mayor a $0")
        return montoTotalGasto
    

    #Debemos validar que haya al menos 2 participantes en el gasto
    def validate_participantes(self, participantes):
        if len(participantes) < 2:
            raise ValidationError("El gasto debe tener al menos 2 participantes")
        return participantes

#Devolucion de los datos del gasto creado
