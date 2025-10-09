const sensor = {
    'url': 'http://127.0.0.1:3000',
    'obterDados': async () => {
        const resposta = await fetch(sensor.url)
        const dados = await resposta.json()
    
        return dados
    },
    'atualizarModelo': dados => {
        console.log(dados)
        sensor.dados = [...dados]
    },
    'dados': []
}
