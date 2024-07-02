//sid_cliente_anexos_table

var conteudoAnexos = document.getElementById("CONTEUDOANEXOS");
var linhasTabela = conteudoAnexos.querySelectorAll("table tbody tr");
var listaArquivos = [];

linhasTabela.forEach(function(linha) {
    var dataOperacao = linha.cells[0].innerText;
    var dataAcontecimento = linha.cells[1].innerText;
    var usuario = linha.cells[2].innerText;
    var observacao = linha.cells[3].innerText;
    var tipoAnexo = linha.cells[4].innerText;
    var linkAnexo = linha.cells[5].querySelector("a").getAttribute("href");

    var arquivo = {
        dataOperacao: dataOperacao,
        dataAcontecimento: dataAcontecimento,
        usuario: usuario,
        observacao: observacao,
        tipoAnexo: tipoAnexo,
        linkAnexo: linkAnexo
    };

    listaArquivos.push(arquivo);
});

return listaArquivos;
