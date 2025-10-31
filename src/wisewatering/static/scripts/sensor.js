const sensor = {
    'url': 'http://192.168.1.70:3000/api/dados',
    'urlAcao': 'http://192.168.1.70:3000/api/acoes',
    'obterDados': async () => {
        const resposta = await fetch(sensor.url);

        if (!resposta.ok) {
          throw new Error("Erro na obtenção de dados.");
        }

        const dados = await resposta.json();
    
        return dados;
    },
    'solicitarAcao': async carga => {
        opcoes = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(carga)
          };
        const resposta = await fetch(sensor.urlAcao, opcoes);
        const sucesso = await resposta.json();

        return sucesso;
    }
}
