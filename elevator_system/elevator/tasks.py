from background_task import background
from .models import Elevator
import time
import threading

@background(schedule=1)
def process_elevators():
    elevators = Elevator.objects.filter(is_available=True)
    threads = []

    for elevator in elevators:
        thread = threading.Thread(target=process_elevator, args=(elevator,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def process_elevator(elevator):
    while True:
        if elevator.is_available:
            elevator.handle_requests()
        time.sleep(2)