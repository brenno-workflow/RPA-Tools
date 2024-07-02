//sid_cliente_anexos_table

function extrairDadosAnexos() {
    var conteudoAnexos = document.getElementById("CONTEUDOANEXOS");
    if (conteudoAnexos) {
        var linhasTabela = conteudoAnexos.querySelectorAll("table tbody tr");
        var listaArquivos = [];

        linhasTabela.forEach(function(linha) {
            var cells = linha.cells;
            if (cells.length >= 6) {
                var dataOperacao = cells[0].innerText;
                var dataAcontecimento = cells[1].innerText;
                var usuario = cells[2].innerText;
                var observacao = cells[3].innerText;
                var tipoAnexo = cells[4].innerText;
                var linkAnexo = cells[5].querySelector("a") ? cells[5].querySelector("a").getAttribute("href") : null;

                var arquivo = {
                    dataOperacao: dataOperacao,
                    dataAcontecimento: dataAcontecimento,
                    usuario: usuario,
                    observacao: observacao,
                    tipoAnexo: tipoAnexo,
                    linkAnexo: linkAnexo
                };

                listaArquivos.push(arquivo);
            }
        });

        return listaArquivos;
    } else {
        console.error("Elemento com ID 'CONTEUDOANEXOS' não encontrado.");
        return [];
    }
}

// Para chamar a função e obter a lista de arquivos
return extrairDadosAnexos();
