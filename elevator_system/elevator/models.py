from django.db import models
import time
# Create your models here.
class Elevator(models.Model):
    elevator_number = models.IntegerField()
    floor = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    is_door_opens = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_operational = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ('UP', 'Up'),
            ('DOWN', 'Down'),
            ('IDLE', 'Idle')
        ),
        default='IDLE'
    )

    def handle_requests(self):
        print("got it")
        requests = Request.objects.filter(elevator=self)
        print(requests)

        for request in requests:
            destination_floor = request.floor
            print(destination_floor)
            if destination_floor > self.floor:
                self.move_up(destination_floor)
            elif destination_floor < self.floor:
                self.move_down(destination_floor)

            # After reaching the destination floor, remove the request
            print("hello")
            request.delete()

        # Mark the elevator as available once all requests are processed
        self.is_available = True
        self.save()

    def move_up(self,destination):
        # Logic to move the elevator up
        self.is_available = False
        self.is_door_opens = False
        self.status = 'UP'
        self.save()

        current_floor = self.floor
        while current_floor < destination:
            time.sleep(5)  # Simulate elevator movement time
            
            current_floor += 1
            self.floor = current_floor
            self.save()
        
        self.open_door()
        # Wait for 2 seconds
        time.sleep(2)
        self.close_door()

        self.status = 'IDLE'
        self.is_available = True
        self.save()
        
        

    def move_down(self,destination):
        print("dowm")
        self.is_available = False
        self.is_door_opens = False
        self.status = 'DOWN'
        self.save()

        current_floor = self.floor
        while current_floor > destination:
            time.sleep(5)  # Simulate elevator movement time
            
            current_floor -= 1
            self.floor = current_floor
            self.save()
        
        self.open_door()
        # Wait for 2 seconds
        time.sleep(2)
        self.close_door()
        self.status = 'IDLE'
        self.is_available = True
        self.save()

    def open_door(self):
        print("hey")
        self.is_door_opens = True
        self.save()
        print("saved")


    def close_door(self):
        self.is_door_opens = False
        self.save()



class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.IntegerField()