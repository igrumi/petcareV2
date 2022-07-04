from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Producto(models.Model):
    idProducto = models.IntegerField(primary_key=True, verbose_name="ID de producto")
    nomProducto = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre del producto")
    nomCategoria = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre Categoría")
    descripcion = models.CharField(max_length=300, blank=False, null=False, verbose_name="Descripción del producto")
    precio = models.IntegerField(blank=False, null=False, verbose_name="Precio")
    porcDesctoSubscriptor = models.IntegerField(blank=False, null=False, verbose_name="Descuento Subscriptor")
    porDesctoOferta = models.IntegerField(blank=False, null=False, verbose_name="Descuento Oferta")
    urlImagenProducto = models.CharField(max_length=300, blank=False, null=False, verbose_name="Imágen Producto")

    def __str__(self):
        return f"{self.nomProducto} - {self.descripcion} - {self.precio}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=80, blank=True, null=True, verbose_name="Rut")
    direccion = models.CharField(max_length=80, blank=True, null=True, verbose_name="Dirección")
    urlImagenUsuario = models.CharField(max_length=300, blank=True, null=True, verbose_name="Imágen Usuario")
    esSubscriptor = models.CharField(max_length=2, blank=True, null=True, verbose_name="Es Suscriptor")

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name} ({self.user.email})"
        
class Factura(models.Model):
    nroFactura = models.IntegerField(primary_key=True, verbose_name="Nro. de factura")
    idProd = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, verbose_name="ID de Producto")
    idUsuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="ID de usuario")
    fecha = models.DateTimeField(auto_now=True, verbose_name="Fecha")
    montoTotal = models.IntegerField(blank=False, null=False, verbose_name="Monto total")
    estadoActual = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado actual")