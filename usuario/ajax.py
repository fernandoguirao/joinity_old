from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from joinitys.models import Joinitys, Usuarios_Joinity
@dajaxice_register
def buscar(request, usuario, joinity_id):
    joinity=get_object_or_404(Joinitys, pk=joinity_id)
    lista_usuarios=[]
    usuarios_invitados=[]
    usuarios_joinity=Usuarios_Joinity.objects.filter(joinity=joinity)
    for user in usuarios_joinity:
        usuarios_invitados.append(user.usuario)
    for resultado in User.objects.filter(first_name__icontains=usuario):
        if resultado not in lista_usuarios:
            lista_usuarios.append(resultado)
    for resultado in User.objects.filter(last_name__icontains=usuario):
        if resultado not in lista_usuarios:
            lista_usuarios.append(resultado)
    context={"lista_usuarios": lista_usuarios, "usuarios_invitados": usuarios_invitados, "joinity":joinity}
    resultados=render_to_string('single/lista_usuarios.html', context)
    return simplejson.dumps({'resultados':resultados})