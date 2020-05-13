$(function(){
$.getJSON("login_usuarios.json", function(data) {
    var mydata = data.data;
  
    for (i = 0; i < data.length; i++) {
      saida += data[i];
      //saida += '<div class="row">';
      //saida += '<div class="col-lg-4 band-img">';
      //saida += '<img src="' + bands[i].picture + '" alt="' + bands[i].name + '" title="' + bands[i].name + '">';
      //saida += '</div>';
      //saida += '</div>';
    }
  
    document.getElementById('tela').innerHTML = saida;
  });
});
