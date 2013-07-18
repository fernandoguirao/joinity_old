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
function refrescar(data){
	$("#cronologia").html(data.mensajes);
}
function enviar_mensaje(data){
	if (data.error){
		for (error in data.error){
			$("#mensaje_error").append("<p><b>"+error+"</b></p>");
		}
	}
	else{
		Dajaxice.mensajes.refrescar(refrescar, {'conversador_id':data.conversador_id})
	}
}
function cargador(contenedor) {
  $(contenedor).html('');
  $('.ocultarcargador #fadingBarsG').clone().appendTo(contenedor);
  $(contenedor).addClass('grisclaro');
  $(contenedor).removeClass('amarillo');
}

var identificador;
var textoidentificador;
var identificadorprev;

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
	  alert("Aficiones");
  	n=data.n;
  }
  else if (data.categoria==2){
	  n_compras=data.n;
  }
  else{
	  n_family=data.n;
  }
  $('.contenedor-los-joinitys').append(data.joinitys);
  $('.los-join-footer button').removeClass('grisclaro');
  $('.los-join-footer button').addClass('amarillo');
  $('.losjoin-footer button #fadingBarsG').remove();
  $('.los-join-footer button').html('Quiero ver más');
  donutfunction();
  if(data.joinitys.length==0) {
    $('.los-join-footer button').html('No hay más joinitys');
    $('.los-join-footer button').removeClass('amarillo');
    $('.los-join-footer button').removeClass('btn-embossed');
    $('.los-join-footer button').addClass('claro');
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

$('#appendedInputButton-01,.buscarbtn,.zoomout button,a.iconos.buscador').click(function(event){
  event.stopPropagation();
});

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
$(".donutchart").donutchart();
$(".donutchartcompras").donutchart({'bgColor':'#aa252b'});
$(".donutchartfandfriends").donutchart({'bgColor':'#08705b'});
$('.los-joinity').hover (function(){
  $(".donutchart",this).stop().donutchart("animate");
  $(".donutchartcompras",this).stop().donutchart("animate");
  $(".donutchartfandfriends",this).stop().donutchart("animate");
})
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

$(".aficat").click(function(){
  $('html,body').animate({scrollTop:$(".faficiones").offset().top});
});
$(".compracat").click(function(){
  $('html,body').animate({scrollTop:$(".fcompras").offset().top});
});
$(".famcat").click(function(){
  $('html,body').animate({scrollTop:$(".fandfriends").offset().top});
});

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
$('.cambiafoto').click(function(){
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




/* DROPZONE */

/*
  Dropzone.options.dropform = {
    init: function() {
    }
  };
  
  Dropzone.autoDiscover = false;
  
  $(function() {
  
    var myDropzone = new Dropzone("#dropform");
  
    myDropzone.on("addedfile", function(file) {

      $('.botonsubir').show();
    });
    $('.botonsubir.amarillo').click(function(){
      myDropzone.removeAllFiles();
      $('.botonsubir').hide();
    });
    $('#fotovoto').on('hidden', function () {
      myDropzone.removeAllFiles();
      $('.botonsubir').hide();
    })
  })
*/

/* al hacer click en la foto poner input="file" la etiqueta form en  action contenido="foto" */
