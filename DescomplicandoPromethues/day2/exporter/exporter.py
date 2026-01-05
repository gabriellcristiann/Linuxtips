import requests
import time
from prometheus_client import start_http_server, Gauge

# Definimos a métrica globalmente para evitar reinicializações
GAUGE_ASTRONAUTS = Gauge('number_astronauts', 'Number of astronauts in space')
URL_API = "http://api.open-notify.org/astros.json"

def get_number_astronauts():
    """
    Busca o número de astronautas com timeout e tratamento de erro.
    """
    # Definimos um timeout de 5 segundos para a conexão e leitura
    response = requests.get(URL_API, timeout=5)
    response.raise_for_status() # Lança erro se o status for 4xx ou 5xx
    data = response.json()
    return data['number']

def update_metrics():
    """
    Loop infinito que atualiza a métrica sem derrubar o serviço.
    """
    print("Iniciando coleta de dados...")
    while True:
        try:
            # Pegamos o valor uma única vez
            valor = get_number_astronauts()
            GAUGE_ASTRONAUTS.set(valor)
            print(f"Métrica atualizada: {valor} astronautas no espaço.")
        except Exception as e:
            # Logamos o erro, mas o loop continua vivo
            print(f"Erro ao coletar dados: {e}. Tentando novamente em 10s...")
        
        time.sleep(10)

def init_exporter():
    try:
        start_http_server(8899)
        print("HTTP server iniciado na porta 8899")
    except Exception as e:
        print(f"Erro ao iniciar o servidor HTTP: {e}")
        exit(1)

def main():
    init_exporter()
    update_metrics()

if __name__ == "__main__":
    main()