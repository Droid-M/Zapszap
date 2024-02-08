import time

def regressive_counter(max_seconds):
    for i in range(max_seconds, 0, -1):
        print(f"Aguarde {i} segundos...\n")
        time.sleep(1)