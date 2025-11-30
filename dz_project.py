import threading
import time
import random

# Глобальна змінна команди
command = None
condition = threading.Condition()

# Список живих робітників
alive_workers = []

# Робітник
def worker(worker_id):
    global command, alive_workers
    while True:
        condition.acquire()
        try:
            print(f"Worker {worker_id}: чекаю на команду...")
            condition.wait()  # чекаємо сигналу диспетчера
            print(f"Worker {worker_id}: отримав команду '{command}'")
            if command == "shutdown":
                print(f"Worker {worker_id}: завершую роботу.")
                break
        finally:
            condition.release()  # звільняємо лок після пробудження
        time.sleep(0.5)  # симуляція роботи
    # Робітник завершує роботу — видаляємо його зі списку
    alive_workers.remove(threading.current_thread())

# Диспетчер
def dispatcher():
    global command, alive_workers
    commands = ["load", "process", "shutdown"]
    while True:
        time.sleep(5)
        condition.acquire()
        try:
            if not alive_workers:
                print("Dispatcher: всі робітники завершили роботу. Завершення диспетчера.")
                break
            command = random.choice(commands)
            print(f"\nDispatcher: змінив команду на '{command}'")
            condition.notify()  # звільняємо один робітник
        finally:
            condition.release()

# Створюємо робітників
num_workers = 3
threads = []
for i in range(num_workers):
    t = threading.Thread(target=worker, args=(i+1,))
    alive_workers.append(t)
    t.start()
    threads.append(t)

# Запускаємо диспетчера
dispatcher_thread = threading.Thread(target=dispatcher)
dispatcher_thread.start()

# Чекаємо завершення всіх робітників
for t in threads:
    t.join()

# Чекаємо завершення диспетчера
dispatcher_thread.join()

print("Всі потоки завершено. Програма завершила роботу.")
