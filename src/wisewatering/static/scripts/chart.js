const grafico = document.querySelector('#grafico canvas');

let chartInstance = null;
let labels = [];

function plotarGrafico(historico) {
    const dataPontos = [];
    labels = [];
    
    historico.forEach((item, index) => {
        const umidade = item.data.umidade;
        const numero = item.number;
        
        labels.push(numero);
        dataPontos.push(umidade);
    });
    
    if (chartInstance) {
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].data = dataPontos;
        chartInstance.update();
        return;
    }
    
    chartInstance = new Chart(grafico, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Umidade do Solo',
                data: dataPontos,
                borderColor: 'rgb(28, 55, 175)',
                tension: 0.1,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Umidade'
                    }
                }
            }
        }
    });
}

async function loopGrafico() {
    plotarGrafico(listaDados);
}

const atualizarGrafico = setInterval(loopGrafico, 1000); 

loopPrincipal();