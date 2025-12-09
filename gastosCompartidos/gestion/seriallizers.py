from rest_framework import serializers
from gastosCompartidos.gestion.models import Gasto, Participante, Transaccion, Usuario

#Serializacion de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["username", "email", "telefono", "edad_usuario", "fecha_registro"]
        read_ononly_fields = ["fecha_registro"]

#Serializacion de Gasto
class GastoSerializer(serializers.ModelSerializer):
    creador_detalle = UsuarioSerializer(source = "creador", read_only = True)
    participantes = ParticipanteSerializer(many=True, read_only = True) # type: ignore
    class Meta:
        model = Gasto
        fields = '__all__'

#Serilizacion de Participante en el gasto
class ParticipanteSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioSerializer(source = "usuario",read_only = True)

    class Meta:
        model = Participante
        fields = ["gasto", "usuario","nombreParticipante", "email_participante", "monto_a_pagar", "montoPagado", "estado_pago"]


#Serializacion de Transaccion realizada
class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'