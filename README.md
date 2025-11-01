# Wise Watering

Trata-se de uma aplicação que possibilita o acesso remoto aos dados coletados por um dispositivo, bem como o controle de seus atuadores. No contexto da aplicação, é monitorada a umidade do solo e controlada a irrigação deste, que é representado por um LED.
Este projeto foi desenvolvido para fins educacionais e com estrutura pensada de modo a facilitar a exploração.

## Instalação de dependências

Após clonar o repositório, crie um ambiente virtual de acordo com seu sistema operacional.

```
# macOS/Linux
# You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
python3 -m venv .venv

# Windows
# You can also use `py -3 -m venv .venv`
python -m venv .venv
```
*Fonte:* [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)

Ative o ambiente virtual, fazendo:

```
source venv/bin/activate
```

e então, execute

```
pip install -r requirements.txt
```

para instalar as bibliotecas utilizadas pela aplicação.

## Como utilizar

Primeiramente, recomendo alterar os endereços IP em static/scripts/sensor.js, escrita_atuador.py e leitura_sensor.py, eles estão configurados pela minha rede, então provavelmente não funcionará sem configurar. Os demais endereços da aplicação estão configurados para localhost, mas não há acesso remoto caso todos os endpoints sejam postos desse jeito.

Os arquivos a serem executados são server.py e main.py, em terminais diferentes. O server.py lidará com as requisições e main.py criará uma thread para leitura da porta serial onde o dispositivo estará conectado.

## Screenshots

![Captura de tela](/src/wisewatering/static/images/demo.png)