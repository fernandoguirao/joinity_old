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
    #resultados_categorias_compras=[]
    resultados_eventos=[]
    resultados_lugares=[]
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
        #for compra in Compras.objects.filter(subcategoria__nombre__icontains=palabra):
        #    if compra.joinity not in resultados_categorias_compras:
        #        resultados_categorias_compras.append(compra.joinity)
        #for compra in Compras.objects.filter(subcategoria__categoria__nombre__icontains=palabra):
        #    if compra.joinity not in resultados_categorias_compras:
        #        resultados_categorias_compras.append(compra.joinity)
        for aficion in Aficiones.objects.filter(subcategoria__nombre__icontains=palabra):
            if aficion.joinity not in resultados_categorias_aficiones:
                resultados_categorias_aficiones.append(aficion.joinity)
        for aficion in Aficiones.objects.filter(subcategoria__categoria__nombre__icontains=palabra):
            if aficion.joinity not in resultados_categorias_aficiones:
                resultados_categorias_aficiones.append(aficion.joinity)
        for evento in Usuarios_Evento.objects.filter(usuario=request.user, evento__titulo__icontains=palabra):
            if evento.evento not in resultados_eventos:
                resultados_eventos.append(evento.evento)
        for lugar in Joinitys.objects.filter(lugares__lugar__icontains=palabra):
            if lugar not in resultados_lugares:
                resultados_lugares.append(lugar)
            
    if resultados_usuarios:
        context={"usuarios":resultados_usuarios}
        pagina_usuarios=render_to_string("persistentes/resultados_usuarios.html",context)
    else:
        pagina_usuarios=False
    if resultados_joinitys:
        context={"joinitys":resultados_joinitys}
        pagina_joinitys=render_to_string("persistentes/resultados_joinitys.html", context)
    else:
        pagina_joinitys=False
    if resultados_categorias_aficiones:
        context={"joinitys":resultados_categorias_aficiones}
        pagina_aficiones=render_to_string("persistentes/resultados_joinitys.html", context)
    else:
        pagina_aficiones=False
    if resultados_eventos:
        context={"eventos":resultados_eventos}
        pagina_eventos=render_to_string("persistentes/resultados_eventos.html", context)
    else:
        pagina_eventos=False
    if resultados_lugares:
        context={"joinitys":resultados_lugares}
        pagina_lugares=render_to_string("persistentes/resultados_joinitys.html", context)
    else:
        pagina_lugares=False
    #if resultados_categorias_compras:
    #    context={"joinitys":resultados_categorias_compras}
    #    pagina_compras=render_to_string("persistentes/resultados_joinitys.html", context)
    #else:
    #    pagina_compras=False

    return simplejson.dumps({'usuarios':pagina_usuarios, 'joinitys':pagina_joinitys,
                              'aficiones':pagina_aficiones, 'eventos':pagina_eventos, 'lugares':pagina_lugares})
