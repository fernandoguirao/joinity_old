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

$("select[name='herolist']").selectpicker({style: 'btn btn-small', menuStyle: 'dropdown-menu'});

/* EL DIAL */

$(".donutchart").donutchart();
$(".donutchartcompras").donutchart({'bgColor':'#aa252b'});
$(".donutchartfandfriends").donutchart({'bgColor':'#08705b'});
$('.los-joinity').hover (function(){
  $(".donutchart",this).stop().donutchart("animate");
  $(".donutchartcompras",this).stop().donutchart("animate");
  $(".donutchartfandfriends",this).stop().donutchart("animate");
})

/* SELECTOR HOME */


var seleccionbtn = $('.primerselect .dropdown-menu a');
var seleccionPrim = $(".primerselect button").find('span');

seleccionbtn.click(function(){
  if($(this).text()=="Comprar") {
    $('.selector.comprar').show("fast");
    $('.selector.aficion,.selector.reserva').hide("fast");
  } else if ($(this).text()=="Practicar una afición") {
    $('.selector.aficion').show("fast");
    $('.selector.comprar,.selector.reserva').hide("fast");
  } else if ($(this).text()=="Realizar una reserva"){
    $('.selector.reserva').show("fast");
    $('.selector.aficion,.selector.comprar').hide("fast");
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
  borrarformularios();
});

iniciavot.click(function(){
  $(this).addClass("activado");
  escribemens.removeClass("activado");
  escribeform.animate({'top':155,'opacity':0});
  votaform.animate({'top':-92,'opacity':1});
  /* escribeform.fadeOut(); */
  formupdate.animate({'height':298});
  crearformularios();
});

/* DUPLICAMOS FORMULARIOS */

  var e = $('.laopcion li');
  for (var i = 0; i < 10; i++) {
    e.clone().appendTo('.laopcion');
    e.addClass('displaynone');
  }


function borrarformularios() {

  $('.laopcion li:lt(7)').addClass('displaynone');

}

var indice;

  $('.addopt').click(function(){
    $(this).parent().next().removeClass('displaynone');
    $(this).hide();
    $(this).parent().next().children('.addopt').show();
    $('#formularios-update').height($('#formularios-update').height()+46);
    /* opcionvotar(); */
    indice = $(this).parent().index();
    if(indice>8) {
      $('.addopt').hide();
      $('#formularios-update').height($('#formularios-update').height()-46);
      
    }
  })
  

$('.votafoto').click(function(){
  $(this).hide();
  $(this).parent().find('.fotupload').addClass('inlinee');
  $('#formularios-update').height($('#formularios-update').height()+70);
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