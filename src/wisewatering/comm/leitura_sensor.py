import requests

class Leitura:
    @staticmethod
    def enviar_pro_servidor(pacote: dict):
        url = "http://127.0.0.1:3000/api/dados"
        requests.post(url, json=pacote)