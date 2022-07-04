from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('petCareApi/productos', views.ProductView.as_view(), name="lista_productos"),
    path('petCareApi/productos/<int:idProd>', views.ProductView.as_view(), name="proceso_productos"),
    path('', views.inicio, name="inicio"),
    path('productos/', views.productos, name="productos"),
    path('productos/<idProd>', views.producto, name="producto"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('registrarse', views.registrarse, name="registrarse"),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),
    path('administrar', views.administrar, name="administrar"),
    path('administrar_productos', views.administrar_productos, name="administrar_productos"),
    path('editar_productos/<idProd>', views.editar_productos, name="editar_productos"),
    path('eliminar_producto/<idProd>', views.eliminar_producto, name="eliminar_producto"),
    path('administrar_usuarios', views.administrar_usuarios, name="administrar_usuarios"),
    path('editar_usuario/<idUs>', views.editar_usuario, name="editar_usuario"),
    path('eliminar_usuario/<idUs>', views.eliminar_usuario, name="eliminar_usuario"),
    path('administrar_ventas', views.administrar_ventas, name="administrar_ventas"),
    path('administrar_venta/<idFact>', views.administrar_venta, name="administrar_venta"),
    path('despachar/<idFact>', views.despachar, name="despachar"),
    path('entregar/<idFact>', views.entregar, name="entregar"),
    path('pagar/<idProd>', views.pagar, name="pagar"),
    path('poblarbase', views.poblar_db, name="poblarbase")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)