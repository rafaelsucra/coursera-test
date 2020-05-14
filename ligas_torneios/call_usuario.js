function loadJSON(callback) {   

    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'login_usuarios.json', true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    for (i = 0; i < data.length; i++) {
        saida += data[i];
    }
    document.getElementById('tela').innerHTML = saida;
    xobj.send(null);  
 }


 function readTextFile(file='login_usuarios.json', callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

//usage:
readTextFile("dados.json", function(text){
    var dados = JSON.parse(text);
	
	var nome = document.getElementById('nome');
	nome.innerHTML = dados.nomeV;
	
	var bloco = document.getElementById('bloco');
	bloco.innerHTML = dados.blocoV + " - " + dados.aptoV;
	
	var rg = document.getElementById('rg');
	rg.innerHTML = dados.rgV;
	
	var veiculo = document.getElementById('veiculo');
	veiculo.innerHTML = dados.veiculoV + dados.placaV;
	
	var empresa = document.getElementById('empresa');
	empresa.innerHTML = dados.empresaV;
	
	var datahora = document.getElementById('datahora');
	datahora.innerHTML = dados.datahoraV;
	
    console.log(dados);
});