from django.db import models

# Create your models here.
class Elevator(models.Model):
    floor = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    is_door_open = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_operational = models.BooleanField(default=True)

    def move_up(self):
        # Logic to move the elevator up
        pass

    def move_down(self):
        # Logic to move the elevator down
        pass

    def open_door(self):
        # Logic to open the elevator door
        pass

    def close_door(self):
        # Logic to close the elevator door
        pass

    def start_running(self):
        # Logic to start the elevator running
        pass

    def stop_running(self):
        # Logic to stop the elevator running
        pass

    def display_status(self):
        # Logic to display the current elevator status
        pass

class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.IntegerField()