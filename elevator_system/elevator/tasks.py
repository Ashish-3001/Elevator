from background_task import background
from .models import Elevator
import time

@background(schedule=1)
def process_elevators():
    while True:
        print("hey")
        
        elevators = Elevator.objects.all()
        for elevator in elevators:
            if elevator.is_available:
                print("sent")
                elevator.handle_requests()
        time.sleep(2)