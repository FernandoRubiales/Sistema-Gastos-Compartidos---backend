from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser     #Sirve para 

#CLASE USUARIO
class Usuario(AbstractUser):
    edad_usuario = models.IntegerField(max_length=255, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuarios' 
        indexes = [
            models.Index(fields=['auth0_sub']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.email})"


#CLASE GASTO
class Gasto(models.Model):
    #----------------------------------------------
    DIVISION_EQUITATIVA = 'equitativa'
    DIVISION_PERSONALIZADA = 'personalizada'
    
    DIVISION_CHOICES = [
        (DIVISION_EQUITATIVA, 'División Equitativa'),
        (DIVISION_PERSONALIZADA, 'División Personalizada'),
    ]
    ESTADO_ACTIVO = 'activo'
    ESTADO_CERRADO = 'cerrado'
    ESTADO_CANCELADO = 'cancelado'
    
    ESTADO_CHOICES = [
        (ESTADO_ACTIVO, 'Activo'),
        (ESTADO_CERRADO, 'Cerrado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]
    #-------------------------------------------------

    titulo = models.CharField(max_length=150)
    montoTotalGasto = models.DecimalField(decimal_places=2,  validators=[MinValueValidator(Decimal('0.01'))])
    fechaCreacion = models.DateTimeField(auto_now_add= True) #se llena de manera automatica
    fechaActualizacion = models.DateTimeField(auto_now_add=True) #ultima fecha de actualizacion
    link_gasto = models.CharField(max_length=100, unique=True, blank=True,db_index=True)
    division_tipo = models.CharField(max_length=20, choices=DIVISION_CHOICES, default=DIVISION_EQUITATIVA)
    estado= models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ACTIVO)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="gastos_creados")

    class Meta:
        db_table = 'gastos'
        ordering = ['-fechaCreacion']  #ordena de las fecha mas reciente a la menos reciente, para las busquedas
        indexes = [
            models.Index(fields=['link_gasto']), #indices para busquedas mas rapidas
            models.Index(fields=['creador', 'estado']),
            models.Index(fields=['-fechaCreacion']),
        ]

    def __str__(self):
        return f"Gasto: {self.titulo} - ${self.montoTotalGasto}"
    
#CLASE DE CADA PARTICIPANTE EN EL GASTO
class Participante(models.Model):

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_PAGADO = 'pagado'
    ESTADO_RECIBIDO = 'recibido'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_RECIBIDO, 'Recibido'),
    ]
    
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE, related_name="participantes")
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="participaciones")

    #Se puede agregar participantes que no son usuarios del sistema
    nombreParticipante = models.CharField(max_length=150)
    email_partipante = models.EmailField(blank=True)  #opcional para invitados
    monto_a_pagar = models.DecimalField(decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    montoPagado = models.DecimalField(decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    estado_pago = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)

    class Meta:
        db_table = 'participantes'
        unique_together = ['gasto', 'email_participante']
        indexes = [
            models.Index(fields=['gasto', 'usuario']),
            models.Index(fields=['email_participante']),
        ]

#CLASE DE LA TRANSACCION REALIZADA

class Transaccion(models.Model):

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_COMPLETADO = 'completado'
    ESTADO_FALLIDO = 'fallido'
    ESTADO_CANCELADO = 'cancelado'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_COMPLETADO, 'Completado'),
        (ESTADO_FALLIDO, 'Fallido'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE, related_name='transacciones')
    deudor = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='pagos_realizados')
    acreedor = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='pagos_recibidos')
    