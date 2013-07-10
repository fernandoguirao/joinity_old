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
  if(seleccionPrim.text()=="comprar") {
    $('.select.comprar').show();
    $('.select.aficion,.select.reserva').hide();
  } else if (seleccionPrim.text()=="Practicar una afición") {
    $('.select.aficion').show();
    $('.select.comprar,.select.reserva').hide();
  } else {
    $('.select.reserva').show();
    $('.select.aficion,.select.comprar').hide();
  }
});