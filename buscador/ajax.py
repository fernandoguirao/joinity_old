from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from joinitys.models import Joinitys, Compras, Aficiones
from joinitys.eventos.models import Usuarios_Evento
@dajaxice_register
def buscador(request, s):
    cadena=str(s)
    frase=cadena.split()
    resultados_usuarios=[]
    resultados_joinitys=[]
    resultados_categorias_aficiones=[]
    resultados_categorias_compras=[]
    resultados_eventos=[]
    for palabra in frase:
        for usuario in User.objects.filter(first_name__icontains=palabra):
            if usuario not in resultados_usuarios:
                resultados_usuarios.append(usuario)
        for usuario in User.objects.filter(last_name__icontains=palabra):
            if usuario not in resultados_usuarios:
                resultados_usuarios.append(usuario)
        for joinity in Joinitys.objects.filter(nombre__icontains=palabra):
            if joinity not in resultados_joinitys:
                resultados_joinitys.append(joinity)
        for compra in Compras.objects.filter(subcategoria__nombre__icontains=palabra):
            if compra.joinity not in resultados_categorias_compras:
                resultados_categorias_compras.append(compra.joinity)
        for compra in Compras.objects.filter(subcategoria__categoria__nombre__icontains=palabra):
            if compra.joinity not in resultados_categorias_compras:
                resultados_categorias_compras.append(compra.joinity)
        for aficion in Aficiones.objects.filter(subcategoria__nombre__icontains=palabra):
            if aficion.joinity not in resultados_categorias_aficiones:
                resultados_categorias_aficiones.append(aficion.joinity)
        for aficion in Aficiones.objects.filter(subcategoria__categoria__nombre__icontains=palabra):
            if aficion.joinity not in resultados_categorias_aficiones:
                resultados_categorias_aficiones.append(aficion.joinity)
        for evento in Usuarios_Evento.objects.filter(usuario=request.user, evento__titulo__icontains=palabra):
            if evento.evento not in resultados_eventos:
                resultados_eventos.append(evento.evento)
            
                
    context={"usuarios":resultados_usuarios, "joinitys":resultados_joinitys, 
             "categorias_compras":resultados_categorias_compras, "categoria_aficiones":resultados_categorias_aficiones,
             "eventos": resultados_eventos}
    pagina_resultados=render_to_string("persistentes/pagina_resultados.html", context)
    return simplejson.dumps({'resultados':pagina_resultados})
