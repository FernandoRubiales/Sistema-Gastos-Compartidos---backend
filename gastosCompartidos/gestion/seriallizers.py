from rest_framework import serializers
from gastosCompartidos.gestion.models import Gasto, Participante, Transaccion, Usuario
from decimal import Decimal

class CrearGastoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=150)
    montoTotalGasto = serializers.DecimalField(max_digits = 10, decimal_places = 2)
    division_tipo = serializers.ChoiceField(choices=['equitativa', 'personalizada'], default = 'equitativa')
