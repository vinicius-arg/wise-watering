// Campos do documento
const monitor = document.querySelector('#monitor-umidade');
const variacao = document.querySelector('#variacao');
const autoIrrigacao = document.querySelector('#auto-irrigacao');
const qtdAgua = document.querySelector('#qtd-agua');

const botaoIrrigar = document.querySelector('#irrigar');
const botaoSalvar = document.querySelector('#salvar');

botaoIrrigar.addEventListener('click', e => {
    e.preventDefault();
    sensor.solicitarAcao({'carga': 'irrigar'});
})

let listaDados = [];

const atualizarMonitor = async () => {
    try {
        listaDados = await sensor.obterDados();
        const ultimoDado = listaDados.at(listaDados.lenght-1);
        monitor.innerHTML = ultimoDado.data.umidade;
    } catch (e) {
        console.error("Erro na obtenção de dados.");
    }
}

const atualizarVariacao = () => {
    if (listaDados.length >= 2) {
        ultimo = listaDados.at(listaDados.length - 1).data.umidade;
        penultimo = listaDados.at(listaDados.length - 2).data.umidade;
        variacaoBackward = (ultimo - penultimo) / 2;

        variacao.innerHTML = variacaoBackward;
    }
}

const loopPrincipal = () => {
    atualizarMonitor();
    atualizarVariacao();
};

const loop = setInterval(loopPrincipal, 1000);