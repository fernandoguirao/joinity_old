var ishome = $('#home');
var ismisJoinitys = $('#misJoinitys');

function refresca_notificaciones(data){
	if (data.menu)
		$("#menu_notificaciones").html(data.menu);
}
function marca(data){
	alert("Pon aqui lo que quieras Fernando");
}
function busqueda(data){
	$("#contenedor-resultados").html(data.resultados);
}
function cargaform(data){
	$(".contenedor_formularios").html(data.paginaformulario);

}

$.fn.serializeObject = function()
{
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
  $("#cronologia").html(data.mensajes);
  if(hasescrito) {
    var contain = $('#ajaxbtn');
    contain.attr('value','Enviar');
    contain.removeClass('grisclaro');
    contain.addClass('verde').delay(1000).queue(function(next){
    $(this).removeClass("verde");
    next();
    });
    $('#fadingBarsG',contain.parent()).remove();
    hasescrito=false;
  }
}
function enviar_mensaje(data){
  if (data.error){
    $("#mensaje_error").show();
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
function refrescar_joinitys(data){
	$("#cronologia").html(data.muro);
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
  else{
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

/* Abrir menú lateral en móvil */

$('.abreOculto').toggle(function(){
  $('.menu-oculto-adaptativo').stop().animate({'left':'0px'});
  $('.contenedorAdaptativo').stop().animate({'left':'105%'});
},function(){
  $('.menu-oculto-adaptativo').stop().animate({'left':'-105%'});
  $('.contenedorAdaptativo').stop().animate({'left':'0px'});
})

/* Buscador */

$('#buscador-principal').fadeOut();
$('a.iconos.buscador').click(function(){
  $('#buscador-principal').fadeIn();
  $('.buscaform').addClass('zoomout');
})

$('html').click(function() {
  $('#buscador-principal').fadeOut();
  $('.buscaform').removeClass('zoomout');
});

$('#appendedInputButton-01,.buscarbtn,.zoomout button,a.iconos.buscador,#contenedor-resultados a,.busc-peq').click(function(event){
  event.stopPropagation();
});

$('.buscarbtn').click(function(){
  $('#appendedInputButton-01').hide();
  $('#contenedor-resultados,.busc-peq').show();
})

/* Comentar: ocultar/mostrar */

$(".comentariosJoinity .btn.grisclaro").click(function() {
  $(this).parent().children('.escribe-input').removeClass('oculto');
  $(this).addClass('oculto');
  $(this).parent().children('.escribe-input').children('.input-append').children('.elboton').children('.btn').click(function(){
    $(this).parent().parent().parent().addClass('oculto');
    $(this).parent().parent().parent().parent().children('.btn.grisclaro').removeClass('oculto');
  });
})

/* Selects */

$("select[name='herolist'],select[name='comprar2'],select[name='comprar3'],select[name='aficion2'],select[name='reserva2']").selectpicker({style: 'btn btn-small', menuStyle: 'dropdown-menu'});

/* EL DIAL */
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
    })
  } else {
    
  }
}
donutfunction();

/* SELECTOR HOME */


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

/* AUTOSCROLL HOME */

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
    $('.tipo2,.tipo1,.tipo3').slideDown();
  });
  $(".aficat").click(function(){
    $('.famcat,.compracat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo3').slideDown();
    $('.tipo2,.tipo1').slideUp();
  });
  $(".compracat").click(function(){
    $('.famcat,.aficat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo2').slideDown();
    $('.tipo3,.tipo1').slideUp();
  });
  $(".famcat").click(function(){
    $('.compracat,.aficat,.todascat').removeClass('activa');
    $(this).addClass('activa');
    $('.tipo1').slideDown();
    $('.tipo3,.tipo2').slideUp();
  });
}

/* VOTACIONES */

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
  /* escribeform.fadeIn(); */
  formupdate.animate({'height':56});
  escribeform.animate({'top':0,'opacity':1});
});

iniciavot.click(function(){
  $(this).addClass("activado");
  escribemens.removeClass("activado");
  escribeform.animate({'top':155,'opacity':0});
  votaform.animate({'top':-92,'opacity':1});
  /* escribeform.fadeOut(); */
  formupdate.animate({'height':298+jei});
});

/* DUPLICAMOS FORMULARIOS */

  var e = $('.laopcion li');
  for (var i = 0; i < 10; i++) {
    e.clone().appendTo('.laopcion');
    e.addClass('displaynone');
  }

/*

function borrarformularios() {

  $('.laopcion li:lt(7)').addClass('displaynone');

}
*/

var indice;

  $('.addopt').click(function(){
    $(this).parent().next().removeClass('displaynone');
    $(this).hide();
    $(this).parent().next().children('.addopt').show();
    $('#formularios-update').height($('#formularios-update').height()+46);
    jei = jei+46;
    /* opcionvotar(); */
    indice = $(this).parent().index();
    if(indice>8) {
      $('.addopt').hide();
      $('#formularios-update').height($('#formularios-update').height()-46);
      jei = jei-46;
      
    }
  })
  

$('.votafoto').click(function(){
  $(this).hide();
  $(this).parent().find('.fotupload').addClass('inlinee');
  $('#formularios-update').height($('#formularios-update').height()+70);
  jei = jei+70;
});

/* COMENTARIOS Y FOTOS */
/*$('.cambiafoto').click(function(){
  $('.escribeform.prinform').attr('action', '?contenido=foto');
  $('#appendedInputButton-02').prop("type","file");
  $('#appendedInputButton-02,.escribe-input').addClass('hayfoto');
    $('#appendedInputButton-02').addClass('btn');
    $('#hazclick').addClass('confoto');
    
})

$('.cambiatexto').click(function(){
  $('.escribeform.prinform').attr('action', '?contenido=texto');
  $('#appendedInputButton-02').prop("type","text");
  $('#appendedInputButton-02,.escribe-input').removeClass('hayfoto');
    $('#appendedInputButton-02').removeClass('btn');
    $('#hazclick').removeClass('confoto');
})
*/
/* CAROUSEL */

$('.carousel').carousel({interval:7000,pause:false});

/* ZOOM CAROUSEL */

/*
var ddiv = $('#home .carousel .item img');
var sizeNowH = ddiv.height();
var sizeNowW = ddiv.width();


*/

/*
$('#myCarousel').bind('slid', function() {
  $('#myCarousel h1').removeClass('claseizquierda');
  $('#myCarousel p').removeClass('clasederecha');
  },function(){
      $('#myCarousel h1').addClass('claseizquierda');
  $('#myCarousel p').addClass('clasederecha');
  })
*/

/*
$(function(){
		$('#fotoinput').customFileInput();	
});
*/

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
})

/* MENSAJES ENTER */

$(function() {
  $('.inputajax').keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      $('#ajaxbtn').click();
      return false;
    }
  });
})