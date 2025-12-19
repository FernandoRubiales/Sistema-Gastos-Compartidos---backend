from rest_framework import serializers
from gastosCompartidos.gestion.models import Gasto, Participante, Transaccion, Usuario
from decimal import Decimal
from django.core.exceptions import ValidationError

#Entrada de datos para la creacion de un gasto
class ParticipanteSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    email = serializers.CharField(required=False, allow_blank=True)
    usuario_id = serializers.IntegerField(required=False, allow_null = True)
    montoPagado = serializers.DecimalField(max_digits = 10, decimal_places = 2, default = Decimal('0.00'))

    def validate_montoPagado(self, montoPagado):
        if montoPagado < 0:
            raise ValidationError("El monto pagado por el participante no puede ser negativo")
        return montoPagado


class GastoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=150)
    montoTotalGasto = serializers.DecimalField(max_digits = 10, decimal_places = 2)
    division_tipo = serializers.ChoiceField(choices=['equitativa', 'personalizada'], default = 'equitativa')
    participantes = ParticipanteSerializer(many=True)

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

#Respuesta de datos para la visualizacion de un gasto
class ParticipanteResponseSerializer(serializers.ModelSerializer):
    
    monto_pendiente = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    debe_dinero = serializers.BooleanField(read_only=True)
    le_deben_dinero = serializers.BooleanField(read_only=True)
    quedo_saldado = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Participante
        fields = [
            'id',                     
            'nombreParticipante',     
            'email_partipante',        
            'montoPagado',             
            'monto_a_pagar',          
            'monto_pendiente',        
            'debe_dinero',             
            'le_deben_dinero',        
            'quedo_saldado',          
            'estado_pago'              
        ]
        read_only_fields = [
            'id',
            'nombreParticipante',
            'email_partipante',
            'montoPagado',
            'monto_a_pagar',
            'monto_pendiente',
            'debe_dinero',
            'le_deben_dinero',
            'quedo_saldado',          
            'estado_pago'              
        ]


class GastoResponseSerializer(serializers.ModelSerializer):
    
    # URL para compartir
    url_compartible = serializers.SerializerMethodField()
    
    # Nombre del usuario creador 
    creador_nombre = serializers.CharField(source='creador.username', read_only=True)
    
    # Anida los participantes con toda su información
    participantes = ParticipanteResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Gasto
        fields = [
            'id',                     
            'titulo',                 
            'montoTotalGasto',        
            'division_tipo',           
            'estado',                  
            'link_gasto',              
            'url_compartible',         
            'creador_nombre',         
            'fechaCreacion',           
            'participantes'            
        ]
        read_only_fields = [
            'id',
            'titulo',
            'montoTotalGasto',
            'division_tipo',
            'estado',
            'link_gasto',
            'url_compartible',
            'creador_nombre',
            'fechaCreacion',
            'participantes'
        ]
    
   # def get_url_compartible(self, obj):
       
       # from django.conf import settings
        
        # Obtener URL del frontend desde settings
       # base_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        # Retornar URL completa
       # return f"{base_url}/gasto/{obj.link_gasto}"
