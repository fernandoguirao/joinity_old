//======================
//! VARIABLES PÁGINAS
//======================


var ishome = $('#home');
var ismisJoinitys = $('#misJoinitys');
var ismensajes = $('#misMensajes');
var isfamily = $('.jfamily');
var iscompras = $('#header-compras');


//======================
//! FUNCIONES AJAX
//======================
function crear_pago_joinity(data){
	if (data.ok){
		alert("Pago creado correctamente. Puede cerrar estas ventanas.");
	}
}

function crear_categoria(data){
	if (data.ok){
		alert("Categoría creada");
	}
}
function refresca_puntuacion(data){
	$('#div_puntuacion').html(data.puntuacion);
    $('.estrellas i:lt('+ laPuntuacion +')').addClass('hovers');
    location.reload();
}
function puntuar_joinity(data){
	if (data.ok){
		Dajaxice.joinitys.recargar_puntuacion(refresca_puntuacion, {'joinity_id':data.joinity_id});
	}
}

function asignar_compra(data){
  if (data.ok){
    alert("Compra asignada");
  }
}

function reserva_hotel(data){
  if (data.ok){
    alert("Reserva enviada");
  }
}
function reserva_restaurante(data){
  if (data.ok){
    alert("Reserva enviada");
  }
}

function seguir_brand(data){
  //En esta funcion mete lo que tenga que hacer tras darle al boton de seguir un brand, quita el return. 
  return true;
}
function dejar_de_seguir_brand(data){
  //En esta funcion mete lo que tenga que hacer tras darle al boton de dejar de seguir un brand, quita el return. 
  return true;
}

function carga_pago(data){
  var cronologia = $("#cronologia");
  cronologia.html(data.pago);
}

function actualiza_usuario(data){
  var estadousuario = $("#estadousuario_lista_"+data.id_usuario);
  estadousuario.html("Ya invitado");
}
function busquedausuarios(data){
  var resbusuario = $("#resultadosbusquedausuarios");
  resbusuario.html(data.resultados);
}

function anyadir_lugar(data){
  var listlugares = $("#lista_lugares");
  listlugares.html(data.lista);
}
function cargar_subcategoria(data){
  var selsubcat = $("#select_subcategorias");
  selsubcat.html(data.select);
}

function refresca_notificaciones(data){
  var menunotif = $("#menu_notificaciones");
  if (data.menu)
    menunotif.html(data.menu);
}

function marca(data){
  /* alert("Pon aqui lo que quieras Fernando"); */
}

function busqueda(data){
	var resultados_usuarios = $("#res-usuarios");
	var resultados_joinitys=$("#res-joinitys");
	var resultados_aficiones=$("#res-aficiones");
	var resultados_eventos=$("#res-eventos");
	var resultados_lugares=$("#res-lugares");
	var uno = $('#tabFiltro > li:nth(0) a');
	var dos = $('#tabFiltro > li:nth(1) a');
	var tres = $('#tabFiltro > li:nth(2) a');
	var cuatro = $('#tabFiltro > li:nth(3) a');
	var cinco = $('#tabFiltro > li:nth(4) a');
	if (data.usuarios){
		resultados_usuarios.html(data.usuarios);
		dos.trigger('click');
	}
	else{
		resultados_usuarios.html("");
	}
	if (data.joinitys){
		resultados_joinitys.html(data.joinitys);
		uno.trigger('click');
	}
	else{
		resultados_joinitys.html("");
	}
	if (data.aficiones){
		resultados_aficiones.html(data.aficiones);
		cuatro.trigger('click');
	}
	else{
		resultados_aficiones.html("");
	}
	if (data.eventos){
		resultados_eventos.html(data.eventos);
		tres.trigger('click');
	}
	else{
		resultados_eventos.html("");
	}
	if (data.lugares){
		resultados_lugares.html(data.lugares);
		cinco.trigger('click');
	}
	else{
		resultados_lugares.html("");
	}
}

function cargaform(data){
  var contenedor_formularios = $(".contenedor_formularios");
  contenedor_formularios.html(data.paginaformulario);
}

function busqueda_usuarios(data){
	if(data.resultados){
		$("#resultados_busqueda_amigos").html(data.resultados);
	}
}

$.fn.serializeObject = function() {
  var o = {};
  var a = this.serializeArray();
  $.each(a, function() {
    if (o[this.name]) {
      if (!o[this.name].push) {
        o[this.name] = [o[this.name]];
      }
      o[this.name].push(this.value || '');
    } else {
      o[this.name] = this.value || '';
    }
  });
  return o;
};

var hasescrito = false;

function refrescar_mensajes(data){
  var cronologia = $("#cronologia");
  cronologia.html(data.mensajes);
  if(hasescrito) {
    var contain = $('#ajaxbtn');
    contain.attr('value','Enviar');
    contain.removeClass('grisclaro');
    contain.addClass('verde').delay(1000).queue(function(next){
    $(this).removeClass("verde");
      next();
    });
    var fadingBar = $('#fadingBarsG',contain.parent());
    fadingBar.remove();
    hasescrito=false;
  }
}

function enviar_mensaje(data){
  if (data.error){
    var mensajeerror = $("#mensaje_error");
    mensajeerror.show();
    var contain = $('#ajaxbtn');
    contain.attr('value','Enviar');
    contain.removeClass('grisclaro');
    $('#fadingBarsG',contain.parent()).remove();
  }
  else {
    $("#appendedInputButton-02").val("");
    Dajaxice.mensajes.refrescar(refrescar_mensajes, {'conversador_id':data.conversador_id});
    hasescrito=true;
  }
}

function postear(data){
  if (data.error){
    $("#mensaje_error").append("<p><b>"+data.error+"</b></p>");
  }
  else{
    $("#appendedInputButton-02").val("");
    Dajaxice.joinitys.refrescar(refrescar_joinitys, {'joinity_id':data.joinity_id})
  }
}
function comentar(data){
	  if (data.error){
		  alert("No se pudo procesar la solicitud");
	  }
	  else{
	    $(".inputcomentario").val("");
	    Dajaxice.joinitys.refrescar(refrescar_joinitys, {'joinity_id':data.joinity_id})
	  }
	}

function refrescar_joinitys(data){
  $("#cronologia").html(data.muro);
  timeLineDinamica();
}

var identificador;
var textoidentificador;
var identificadorprev;

function cargadormensajes() {
  var contain = $('#ajaxbtn');
  contain.attr('value','');
  $('.ocultarcargador #fadingBarsG').clone().appendTo(contain.parent());
  contain.addClass('grisclaro');
}

function cargador() {
  var contain = $(identificador);
  contain.html('');
  $('.ocultarcargador #fadingBarsG').clone().appendTo(contain);
  contain.addClass('grisclaro');
  contain.removeClass('amarillo');
}

function cargarfiltro() {
  $(identificadorprev).html(textoidentificador);
  identificadorprev = identificador;
  var contain = $(identificador);
  textoidentificador = contain.html();
  contain.html('');
  $('.ocultarcargador #fadingBarsG').clone().appendTo(identificador);
  contain.parent().children('.filtros').removeClass('activo');
}

function filtrar(data){
  if (data.categoria==3){
    n=data.n;
    order=data.order;
  }
  else if (data.categoria==2){
    n_compras=data.n;
    order_compras=data.order;
  }
  else {
    n_family=data.n;
    order_family=data.order;
  }
  var contain = $(identificador);
  contain.addClass('activo');
  contain.parent().parent().parent().children('.contenedor-los-joinitys').html(data.joinitys);
  $('#fadingBarsG',identificador).remove();
  contain.html(textoidentificador);
  donutfunction();
  if(data.joinitys.length==0) {
    contain.parent().parent().parent().children('.contenedor-los-joinitys').html('No hay joinitys que coincidan con esta selección :(');
  }
}

function filtrar_brands(data){
	  n=data.n;
	  order=data.order;
	  var contain = $(identificador);
	  contain.addClass('activo');
	  contain.parent().parent().parent().children('.contenedor-los-joinitys').html(data.joinitys);
	  $('#fadingBarsG',identificador).remove();
	  contain.html(textoidentificador);
	  donutfunction();
	  if(data.joinitys.length==0) {
	    contain.parent().parent().parent().children('.contenedor-los-joinitys').html('No hay joinitys que coincidan con esta selección :(');
	  }
	}
function cargar_mas(data){
  if (data.categoria==3){
    n=data.n;
  }
  else if (data.categoria==2){
    n_compras=data.n;
  }
  else{
    n_family=data.n;
  }
  var contain = $(identificador);
  contain.parent().prev().append(data.joinitys);
  contain.removeClass('grisclaro');
  contain.addClass('amarillo');
  contain.children('#fadingBarsG').remove();
  contain.html('Quiero ver más');
  donutfunction();
  if(data.joinitys.length==0) {
    contain.html('No hay más joinitys');
    contain.removeClass('amarillo');
    contain.removeClass('btn-embossed');
    contain.addClass('claro');
  }
}
function cargar_mas_brands(data){
	  n=data.n;
	  var contain = $(identificador);
	  contain.parent().prev().append(data.joinitys);
	  contain.removeClass('grisclaro');
	  contain.addClass('amarillo');
	  contain.children('#fadingBarsG').remove();
	  contain.html('Quiero ver más');
	  donutfunction();
	  if(data.joinitys.length==0) {
	    contain.html('No hay más joinitys');
	    contain.removeClass('amarillo');
	    contain.removeClass('btn-embossed');
	    contain.addClass('claro');
	  }
	}

/* Fin de ajax */


//===============
//! EL BUSCADOR
//===============


$('#buscador-principal').fadeOut();
$('a.iconos.buscador').click(function(){
  $('#buscador-principal').fadeIn();
  $('.buscaform').addClass('zoomout');
})

$('.vuelve').click(function() {
  $('#buscador-principal').fadeOut();
  $('.buscaform').removeClass('zoomout');
});

/*
$('#appendedInputButton-01,.buscarbtn,.zoomout button,a.iconos.buscador,#contenedor-resultados a,#filtros,ul#tabFiltro li').click(function(event){
  event.stopPropagation();
});
*/

$('.buscarbtn').click(function(){
  $('#appendedInputButton-01').addClass('busc-peq inputNormal');
  $('#contenedor-resultados').show();
  $('#contenedor-resultados').css({'display':'inherit'});
  
})

/* Fin de buscador */


//===================
//! LOS COMENTARIOS
//===================

function timeLineDinamica() {
$(".comentariosJoinity .btn.grisclaro").click(function() {
  $(this).parent().children('.escribe-input').removeClass('oculto');
  $(this).addClass('oculto');
  $(this).parent().children('.escribe-input').children('.input-append').children('.elboton').children('.btn').click(function(){
    $(this).parent().parent().parent().addClass('oculto');
    $(this).parent().parent().parent().parent().children('.btn.grisclaro').removeClass('oculto');
  });
});
}

timeLineDinamica();


//===============
//! LOS SELECTS
//===============


$("select[name='herolist'],select[name='listahoras'],select[name='comprar2'],select[name='comprar3'],select[name='aficion2'],select[name='reserva2'],select[name='selectprueba']").selectpicker({style: 'btn btn-small', menuStyle: 'dropdown-menu'});

/* EL SELECTOR DE HOME */

var seleccionbtn = $('.primerselect .dropdown-menu a');
var seleccionPrim = $(".primerselect button").find('span');
var selector = $('.selectoresgrupo');

seleccionbtn.click(function(){
  if($(this).text()=="Comprar") {
    selector.animate({'top':'0px'});
    $('.selector.comprar').fadeTo('slow',1);
    $('.selector.aficion,.selector.reserva').fadeTo('slow',0);
  } else if ($(this).text()=="Practicar una afición") {
    selector.animate({'top':'-45px'});
    $('.selector.aficion').fadeTo('slow',1);
    $('.selector.comprar,.selector.reserva').fadeTo('slow',0);
  } else if ($(this).text()=="Realizar una reserva"){
    selector.animate({'top':'-111px'});
    $('.selector.reserva').fadeTo('slow',1);
    $('.selector.aficion,.selector.comprar').fadeTo('slow',0);
  }
});

var selectreserva = $('.selectreserva .dropdown-menu a');
var elrestaurante = $('.botonRestaurante');
var elhotel = $('.botonHotel');

selectreserva.click(function(){
  if($(this).text()=="un restaurante") {
    elrestaurante.show();
    elhotel.hide();
  } else if ($(this).text()=="un hotel") {
    elrestaurante.hide();
    elhotel.show();
  }
})

if (ishome.length > 0) {
  $('.primerselect ul li:first-child,.segundoselect ul li:first-child,.tercerselect ul li:first-child').children().trigger('click');
}

/* Fin selector home */

/* Fin de selects */


//============================
//! LA RUEDA DE LOS JOINITYS
//============================


function donutfunction(){
  if (ishome.length > 0) {
    $(".donutchart").donutchart();
    $(".donutchartcompras").donutchart({'bgColor':'#aa252b'});
    $(".donutchartfandfriends").donutchart({'bgColor':'#08705b'});
    $('.los-joinity').hover (function(){
      $(".donutchart",this).stop().donutchart("animate");
      $(".donutchartcompras",this).stop().donutchart("animate");
      $(".donutchartfandfriends",this).stop().donutchart("animate");
    })
  } else if (ismisJoinitys.length > 0) {
    $(".donutchart").donutchart({'bgColor':'rgba(0,0,0,.2)'});
    $('.los-joinity').hover (function(){
      $(".donutchart",this).stop().donutchart("animate");
      $(".donutchartcompras",this).stop().donutchart("animate");
      $(".donutchartfandfriends",this).stop().donutchart("animate");
    });
  }
}
donutfunction();


//===================
//! AUTOSCROLL HOME
//===================


if(ishome.length > 0) {
  $(".aficat").click(function(){
    $('html,body').animate({scrollTop:$(".faficiones").offset().top},1200);
  });
  $(".compracat").click(function(){
    $('html,body').animate({scrollTop:$(".fcompras").offset().top},1200);
  });
  $(".famcat").click(function(){
    $('html,body').animate({scrollTop:$(".fandfriends").offset().top},1200);
  });
} else if (ismisJoinitys.length > 0){
  $(".todascat").click(function(){
    $('.famcat,.compracat,.aficat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo3,.tipo2,.tipo1').removeClass('invisible');
    $('.tipo2,.tipo1,.tipo3').slideDown();
  });
  $(".aficat").click(function(){
    $('.famcat,.compracat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo3').removeClass('invisible');
    $('.tipo3').slideDown();
    $('.tipo1,.tipo2').addClass('invisible');
    $('.tipo2,.tipo1').slideUp();
  });
  $(".compracat").click(function(){
    $('.famcat,.aficat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo2').removeClass('invisible');
    $('.tipo2').slideDown();
    $('.tipo3,.tipo1').addClass('invisible');
    $('.tipo3,.tipo1').slideUp();
  });
  $(".famcat").click(function(){
    $('.compracat,.aficat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo1').removeClass('invisible');
    $('.tipo1').slideDown();
    $('.tipo3,.tipo2').addClass('invisible');
    $('.tipo3,.tipo2').slideUp();
  });
}


//==============
//! VOTACIONES
//==============

/* PASAR NÚMERO DE RESPUESTAS y CREAR CADA RESPUESTA CON UN N */

var jei = 0;
var escribemens = $('.escribe-mensaje');
var iniciavot = $('.inicia-votacion');
var votaform = $('.votaform');
var escribeform = $('.escribeform');
var formupdate = $('#formularios-update');

escribemens.click(function(){
  $(this).addClass("activado");
  iniciavot.removeClass("activado");
  votaform.animate({'top':0,'opacity':0});
  formupdate.animate({'height':56});
  escribeform.animate({'top':0,'opacity':1});
});

iniciavot.click(function(){
  $(this).addClass("activado");
  escribemens.removeClass("activado");
  escribeform.animate({'top':155,'opacity':0});
  votaform.animate({'top':-92,'opacity':1});
  formupdate.animate({'height':298+jei});
});

/* DUPLICAMOS FORMULARIOS */

var e = $('.laopcion li');
for (var i = 0; i < 10; i++) {
  e.clone().appendTo('.laopcion');
  e.addClass('displaynone');
}

var indice;

$('.addopt').click(function(){
  $(this).parent().next().removeClass('displaynone');
  $(this).hide();
  $(this).parent().next().children('.addopt').show();
  $('#formularios-update').height($('#formularios-update').height()+46);
  jei = jei+46;
  indice = $(this).parent().index();
  if(indice>8) {
    $('.addopt').hide();
    $('#formularios-update').height($('#formularios-update').height()-46);
    jei = jei-46;
  }
});

$('.votafoto').click(function(){
  $(this).hide();
  $(this).parent().find('.fotupload').addClass('inlinee');
  $('#formularios-update').height($('#formularios-update').height()+70);
  jei = jei+70;
});

/* Fin de votaciones */


//============
//! CAROUSEL
//============

if (ishome.length > 0) {
  $('.carousel').carousel({interval:7000,pause:false});
}

//===========================
//! ESTILOS PARA INPUT FILE
//===========================


$(function() {
  $('input[type=file]').change(function(){
    var data=$(this).val();
    var esto = $(this);
    var nuevo = esto.parent().find('.customFileInput');
    nuevo.text(data);
    esto.parent().width(nuevo.width()+40);
  })
});

var altor = $('.right-side').height();
$('.left-side').height(altor+56);
$('.valor06 .btn.azul').toggle(function(){
  $('.lefti').animate({"opacity":"0"});
  $(this).addClass('menos');
},function(){
  $('.lefti').animate({"opacity":"1"});
  $(this).removeClass('menos');
});

/* Fin de input file */


//======================================
//! MENSAJES: ESCRIBIR CON TECLA ENTER
//======================================


$(function() {
  if (ismensajes.length > 0) {
    $('.inputajax').keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        $('#ajaxbtn').click();
        return false;
      }
    });
  }
})


//============================================
//! CREAR CHECKBOX QUE OCULTA Y MUESTRA DIVS
//============================================


function creaCheckbox (divinicio,leyenda,idcheck) {
  enElDiv = $(divinicio);
  enElDiv.hide();
  idche = enElDiv.prev();
  enElDiv.before('<label class="checkbox checkMuestra" for="'+idcheck+'"><input type="checkbox" value="" id="'+idcheck+'" data-toggle="checkbox"><span class="txtlabel">' + leyenda + '</span></label>');
}

creaCheckbox('#cuantos-participan','¿Hay limitación de participantes?','checknuevo');
creaCheckbox('.diafin','¿Dura más de un día?','checktermina');
creaCheckbox('.seRepite','¿Se repetirá?','checkrepite');
creaCheckbox('.cnivel','¿Es necesario conocimientos previos?','checknivel');
creaCheckbox('.crequisitos','¿Hay algún otro requisito?','checkrequisito');

$('.checkMuestra').toggle(function(){
  $(this).next().slideDown();
  $(this).addClass('checked');
},function(){
  $(this).next().slideUp();
  $(this).removeClass('checked');
});

/* Fin de crea checkbox */


//=======================================
//! FUNCIÓN PARA PUNTUAR CON ESTRELLAS
//=======================================


$( ".estrellas i" ).each(function( index ) {
  laPuntuacion = $('.estrellas').data('estrellas');
  /* Si vamos a votar */
  if (laPuntuacion == '0'){
    $('.estrellas').addClass('point');
    $(this).hover(function(){
      $('.estrellas i:lt('+index+')').addClass('hovers');
      $('.estrellas i:gt('+index+')').removeClass('hovers');
    })
    $(this).click(function(){
      Dajaxice.joinitys.puntuar(puntuar_joinity, {'joinity_id':joinity_id, 'puntuacion':index});
      $('.estrellas i:lt('+ laPuntuacion +')').addClass('hovers');
    })
    /* Si ya hemos votado */
  } else {
    $('.estrellas i:lt('+ laPuntuacion +')').addClass('hovers');
    /*$(this).click(function(){
    	
        Dajaxice.joinitys.puntuar(puntuar_joinity, {'joinity_id':joinity_id, 'puntuacion':index});
     });*/
  }
});


//===========
//! COLORES
//===========


/* SI ES FAMILY & FRIENDS */



/* SI ES COMPRAS */

if(iscompras.length > 0) {
  $('html').addClass("isCompras"); 
}

if(isfamily.length > 0) {
  $('html').addClass("isFamily");
  $('html').removeClass("isCompras");
}