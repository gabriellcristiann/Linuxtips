import requests
import time
from prometheus_client import start_http_server, Gauge

# Definimos a métrica globalmente para evitar reinicializações
URL_API = "http://api.open-notify.org/astros.json"
URL_LOCAL_ISS = "http://api.open-notify.org/iss-now.json"

def get_location():
  """
  Busca a latitude e longitude da ISS
  """
  try:
      response = requests.get(URL_LOCAL_ISS, timeout=5)
      data = response.json()
      return data['iss_position']
  except Exception as e:
        print(f"Erro ao buscar localização da ISS: {e}")
        raise e

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


    astronauts = Gauge('number_astronauts', 'Number of astronauts in space')
    longitude = Gauge('longitude_iss', 'Longitude of the ISS')
    latitude = Gauge('latitude_iss', 'Latitude of the ISS')
    while True:
        try:
            number_astronauts_now = get_number_astronauts()
            location_iss = get_location()
            astronauts.set(number_astronauts_now)
            longitude.set(float(location_iss['longitude']))
            latitude.set(float(location_iss['latitude']))

            print(f"Métrica atualizada: {number_astronauts_now} astronautas no espaço.")
            print(f"Localização da ISS - Latitude: {location_iss['latitude']}, Longitude: {location_iss['longitude']}")
        except Exception as e:
            print(f"Erro ao coletar dados: {e}. Tentando novamente em 10s...")
        
        time.sleep(20)

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