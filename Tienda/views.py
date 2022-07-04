from .models import Producto, PerfilUsuario, Factura
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import RegistrarUsuarioForm, ProductoForm, EditarPerfilUsuarioForm, EditarUsuarioForm
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from urllib import response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
# Create your views here.
class ProductView(View):
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, idProd = 0):
        data = {'message': 'Producto(s) no encontrado(s):('}
        if(idProd > 0):
            products = list(Producto.objects.filter(idProducto=idProd).values())
            if(len(products) > 0):
                data = products[0]
        else:
            products = list(Producto.objects.values())
            data = {'message': 'Success', 'products': products}

        return JsonResponse(data)
   
    def post(self, request):
        jd = json.loads(request.body)
        Producto.objects.create(
            nomProducto = jd["nomProducto"],
            nomCategoria = jd["nomCategoria"],
            descripcion = jd["descripcion"],
            precio = jd["precio"],
            porcDesctoSubscriptor = jd["porcDesctoSubscriptor"],
            porDesctoOferta = jd["porcDesctoOferta"],
            urlImagenProducto = jd["urlImagenProducto"]
        )
        data = {'message': 'Success'}
        return JsonResponse(data)

    def put(self, request, idProd):
        data = {'message': 'Product(s) not found :('}
        jd = json.loads(request.body)
        products = list(Producto.objects.filter(idProducto=idProd).values())
        if(len(products) > 0):
            product = Producto.objects.get(idProducto = idProd)
            product.nomProducto = jd["nomProducto"]
            product.nomCategoria = jd["nomCategoria"]
            product.descripcion = jd["descripcion"]
            product.precio = jd["precio"]
            product.porcDesctoSubscriptor = jd["porcDesctoSubscriptor"]
            product.porDesctoOferta = jd["porcDesctoOferta"]
            product.urlImagenProducto = jd["urlImagenProducto"]
            product.save()
            data = {'message': 'Success'}
            
        return JsonResponse(data)

    def delete(self, request, idProd):
        data = {'message': 'Product(s) not found :('}
        products = list(Producto.objects.filter(idProducto=idProd).values())
        if(len(products) > 0):
            Producto.objects.filter(idProducto=idProd).delete()
            data = {'message': 'Success'}
        return JsonResponse(data)



def inicio(request):
    return render(request, 'usuarios/index.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'usuarios/productos.html', {'productos': productos})

def producto(request, idProd):
    producto = Producto.objects.get(idProducto = idProd)
    return render(request, 'usuarios/producto.html', {'producto': producto})

def nosotros(request):
    return render(request, 'usuarios/nosotros.html')

@csrf_exempt
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    data = {"mesg": ""}
    if(request.method == 'POST'):
        usname = request.POST.get("username")
        contrasena = request.POST.get("contrasena")
        user = authenticate(username=usname, password=contrasena)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(inicio)
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
        else:
            data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, 'usuarios/logear.html', data)

@csrf_exempt
def registrarse(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            imgUser = request.POST.get("userImg")
            sub = 'No'
            suscripcion = request.POST.get("suscripcion")
            if(suscripcion == 'on'):
                sub = 'Si'
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, direccion=direccion, esSubscriptor=sub, urlImagenUsuario=imgUser)
            return redirect(inicio)
    form = RegistrarUsuarioForm()
    return render(request, 'usuarios/registro.html', context={'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect(inicio)

def administrar(request):
    return render(request, 'administrador/administrar.html')

def administrar_productos(request):
    productos = Producto.objects.all()
    form = ProductoForm(request.POST or None, request.FILES or None)
    if(request.method == 'POST'):
        form.save()
        return redirect(administrar_productos)
    return render(request, 'administrador/administrar_productos.html', {'productos': productos, 'form': form})

def editar_productos(request, idProd):
    producto = Producto.objects.get(idProducto=idProd)
    productos = Producto.objects.all()
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if(request.method == 'POST'):
        form.save()
        return redirect(administrar_productos)
    return render(request, 'administrador/editar_productos.html', {'productos': productos, 'form': form, 'pro': producto})

def eliminar_producto(request, idProd):
    producto = Producto.objects.get(idProducto=idProd)
    producto.delete()
    return redirect(administrar_productos)

def administrar_usuarios(request):
    usuarios = PerfilUsuario.objects.all()
    formPerfil = EditarPerfilUsuarioForm(request.POST or None, request.FILES or None)
    formUser = EditarUsuarioForm(request.POST or None, request.FILES or None)
    return render(request, 'administrador/administrar_usuarios.html', {'usuarios': usuarios, 'fperfil': formPerfil, 'fuser': formUser})

def editar_usuario(request, idUs):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    # Forms
    userProfile = PerfilUsuario.objects.get(user_id=idUs)
    formPerfil = EditarPerfilUsuarioForm(request.POST or None, request.FILES or None, instance=userProfile)
    userData = User.objects.get(id=idUs)
    formUser = EditarUsuarioForm(request.POST or None, request.FILES or None, instance=userData)
    suscriber = userProfile.esSubscriptor
    staff = userData.is_staff
    if request.method == 'POST':
        # Profile Data
        userRut = request.POST.get("rut")
        userAddress = request.POST.get("direccion")
        userImg = request.POST.get("urlImagenUsuario")
        userSuscription = request.POST.get("consubscripcion")
        suscriber = 'No'
        if(userSuscription == 'on'):
            suscriber = 'Si'

        #Auth User Data
        usName = request.POST.get("username")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        userEmail = request.POST.get("email")
        userRole = request.POST.get("isStaff")
        staffRole = False
        if(userRole == 'on'):
            staffRole = True
        # Updates
        PerfilUsuario.objects.filter(id=idUs).update(
            rut=userRut, 
            direccion=userAddress, 
            urlImagenUsuario=userImg, 
            esSubscriptor =suscriber
        )

        User.objects.filter(id=idUs).update(
            username=usName,
            first_name=firstName,
            last_name=lastName,
            email=userEmail,
            is_staff=staffRole
        )
        return redirect(administrar_usuarios)
    return render(request, 'administrador/editar_usuarios.html', 
    {'fperfil': formPerfil, 'fuser': formUser, 
    'suscriber': suscriber, 'staff': staff, 'us': userProfile})

def eliminar_usuario(request, idUs):
    usuario = PerfilUsuario.objects.get(user=idUs)
    usuario.delete()
    us = User.objects.get(id=idUs)
    us.delete()
    return redirect(administrar_usuarios)

def administrar_ventas(request):
    ventas = Factura.objects.all()
    return render(request, 'administrador/administrar_ventas.html', {'ventas': ventas})

def pagar(request, idProd):
    producto = Producto.objects.get(idProducto=idProd)
    us = User.objects.get(id = request.user.id)
    usuario = PerfilUsuario.objects.get(user = us)
    precio = producto.precio
    if(usuario.esSubscriptor == 'Si'):
        precio = int(producto.precio*0.95)
    Factura.objects.create(idUsuario=us, idProd=producto, montoTotal=precio, estadoActual='En Bodega')
    return redirect(productos)

def administrar_venta(request, idFact):
    factura = Factura.objects.get(nroFactura = idFact)
    return render(request, 'administrador/administrar_venta.html', {'venta': factura})

def despachar(request, idFact):
    Factura.objects.filter(nroFactura=idFact).update(estadoActual='Despachado')
    return redirect(administrar_ventas)

def entregar(request, idFact):
    Factura.objects.filter(nroFactura=idFact).update(estadoActual='Entregado')
    return redirect(administrar_ventas)


# Script poblar db 
def poblar_db(request):
    Producto.objects.create(nomCategoria="Perros", nomProducto='Saco DogChow', descripcion="Saco de comida para perro 1kg", precio=25000, porcDesctoSubscriptor=2, porDesctoOferta=0, urlImagenProducto='https://bodegadispal.cl/wp-content/uploads/2021/06/765.png')
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Saco Whiskas', descripcion="Saco de comida para gato 1kg", precio=15000, porcDesctoSubscriptor=2, porDesctoOferta=0, urlImagenProducto='https://www.whiskas.cl/wp-content/uploads/2019/12/Hogare%C3%B1os-Adulto-e1581093305603.jpg')
    Producto.objects.create(nomCategoria="Perros", nomProducto='Collar RuffWear', descripcion="Collar para perros", precio=25000, porcDesctoSubscriptor=2, porDesctoOferta=0, urlImagenProducto='https://www.amigales.cl/pub/media/catalog/product/cache/c687aa7517cf01e65c009f6943c2b1e9/t/o/top-rope-collar-sunset_1_3.jpg')
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Cat Love Super Mix Arena', precio=19990, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Cat Love Arena Super Mix contiene bentonita de sodio lo que la hace una arena excelente aglutinando, perfecta controlando olores y de muy fácil limpieza.", urlImagenProducto="https://dojiw2m9tvv09.cloudfront.net/11787/product/supermix-arenasanitaria18kg3989.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Royal Canin Alimento Húmedo Gatitos', precio=2190, porcDesctoSubscriptor=5, porDesctoOferta= 15, descripcion= "Royal Canin Alimento Húmedo Gatitos es una deliciosa combinación de sabores de pescado y atún, en un suave y agradable paté que tendrán a tu gato esperando con impaciencia la hora de comer todos los días.", urlImagenProducto="https://cdn.royalcanin-weshare-online.io/4lbvLnIBBKJuub5qMHG7/v5/cl-l-producto-kitten-pouch-feline-health-nutrition-humedo")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Bravery Chicken Adult Cat', precio=39990, porcDesctoSubscriptor=5, porDesctoOferta= 10, descripcion= "Bravery Adult Cat Chicken es un alimento premium para gatos desde 1 año de edad. Su fórmula es libre de grano, monoproteico e hipoalergénico. Hecho con productos 100% naturales a base de proteínas y antioxidantes. Entrega todos los nutrientes necesarios para mantener una vida sana y activa.", urlImagenProducto="https://dojiw2m9tvv09.cloudfront.net/11787/product/braverychickenadultcat0194.jpg")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Dispensador Snail', precio=23900, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Dispensador de agua y comida con diseño innovador para perros.", urlImagenProducto="https://spzcdn01.akamaized.net/assets/uploads/productos/sliders/d5cfc-dispensador-snail-002_thumbs.jpg")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Plato Crock Metálico', precio=15192, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Cuenco de acero inoxidable para perros.", urlImagenProducto="https://s.cornershopapp.com/product-images/5815397.jpg?versionId=eTajKuCyfBhsXg.4iGeerCtc6Olf3OgV")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Zeedog Arnés Ajustable Ella', precio=26990, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Arnés de pecho de malla ajustable y transpirable para perro.", urlImagenProducto="https://s3.us-east-2.amazonaws.com/media-attachments.ambar.pet/wp-content/uploads/2022/02/04041459/14510-ella-1_air_mesh_ajustavel.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Oxyfresh Shampoo Para Mascotas', precio=13900, porcDesctoSubscriptor=5, porDesctoOferta= 25, descripcion= "El shampoo para mascotas Oxyfresh es definitivamente el mejor que vas a encontrar. Diseñamos nuestra fórmula con pH balanceado para apoyar y calmar la delicada piel de las mascotas que sufren de alergia, ya que es clave para la salud general de las mascotas. Es crucial cuidar su defensa natural contra descamamiento, la picazón, la sequedad y el olor.", urlImagenProducto="https://felinus.cl/1234-large_default/oxyfresh-shampoo-para-mascotas.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Leonardo Quality Selection Kitten', precio=37900, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Alimento húmedo completo para gatitos.", urlImagenProducto="https://http2.mlstatic.com/D_NQ_NP_763510-MLA48462210776_122021-O.webp")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Desparasitante Bravecto', precio=41592, porcDesctoSubscriptor=5, porDesctoOferta= 0, descripcion= "Comprimido masticable contra pulgas y garrapatas en perros.", urlImagenProducto="https://www.amigales.cl/pub/media/catalog/product/cache/c687aa7517cf01e65c009f6943c2b1e9/a/n/antiparasitario_bravecto_perros_01.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Churu De Atún Con Ostiones', precio=13450, porcDesctoSubscriptor=5, porDesctoOferta= 50, descripcion= "Alimento cremoso e irresistible para gatos sabor atún con ostiones.", urlImagenProducto="https://felinus.cl/915-large_default/inaba-churu-sabor-atun-con-ostiones.jpg")
    return redirect(inicio)