from rest_framework import viewsets
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import process_elevators
from django.shortcuts import render, redirect

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

process_elevators()

@api_view(['GET', 'POST'])
def home(request):
    if request.method == 'POST':
        num_elevators = int(request.data.get('num_elevators'))
        initialize_elevator_system(request._request)
        return redirect('elevator_page')
    return render(request, 'elevator/home.html')

@api_view(['GET', 'POST'])
def elevator_page(request):
    if request.method == 'POST':
        floor = int(request.data.get('floor'))
        submit_request(request._request)
        
        return redirect('elevator_page')

    # Fetch the elevator details for the table
    elevators = Elevator.objects.all()
    serializer = ElevatorSerializer(elevators, many=True)

    return render(request, 'elevator/elevator_page.html', {'elevators': serializer.data})

@api_view(['POST'])
def initialize_elevator_system(request):
    num_elevators = int(request.data.get('num_elevators'))

    existing_elevator_numbers = Elevator.objects.values_list('elevator_number', flat=True)
    max_existing_elevator_number = max(existing_elevator_numbers) if existing_elevator_numbers else 0

    if num_elevators > max_existing_elevator_number:
        # Create new elevators
        for elevator_number in range(max_existing_elevator_number + 1, num_elevators + 1):
            Elevator.objects.create(elevator_number=elevator_number)

        return Response({'message': f'{num_elevators} elevators created'}, status=201)
    elif num_elevators < max_existing_elevator_number:
        # Delete excess elevators
        Elevator.objects.filter(elevator_number__gt=num_elevators).delete()

        return Response({'message': f'{max_existing_elevator_number - num_elevators} elevators deleted'}, status=200)
    else:
        return Response({'message': 'No change in elevator count'}, status=200)

@api_view(['GET'])
def fetch_requests_for_elevator(request, elevator_number):
    # Get the elevator by its number and fetch its requests
    try:
        elevator = Elevator.objects.get(elevator_number=elevator_number)
        requests = Request.objects.filter(elevator=elevator)
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=200)
    except Elevator.DoesNotExist:
        return Response({'message': f'Elevator {elevator_number} does not exist'}, status=404)

@api_view(['POST'])
def mark_elevator_not_operational(request):
    elevator_number = request.data.get('elevator_number')

    # Get the elevator by its number and mark it as not operational
    try:
        elevator = Elevator.objects.get(elevator_number=elevator_number)
        elevator.is_operational = False
        elevator.save()
        return Response({'message': f'Elevator {elevator_number} marked as not operational'}, status=200)
    except Elevator.DoesNotExist:
        return Response({'message': f'Elevator {elevator_number} does not exist'}, status=404)

@api_view(['POST'])
def submit_request(request):
    floor = int(request.data.get('floor'))

    try:
        # Get the optimal elevator
        elevator = get_optimal_elevator(floor)

        if elevator:
            # Create a new request for the elevator
            Request.objects.create(elevator=elevator, floor=floor)

            return Response({'message': f'Request added to Elevator {elevator.elevator_number}'}, status=200)
        else:
            return Response({'message': 'No available elevators'}, status=400)

    except Exception as e:
        return Response({'message': str(e)}, status=500)

@api_view(['GET'])
def get_next_destination(request, elevator_number):
    try:
        elevator = Elevator.objects.get(elevator_number=elevator_number)
        requests = Request.objects.filter(elevator=elevator).order_by('id')

        if requests.exists():
            next_destination = requests.first().floor
            return Response({'next_destination': next_destination}, status=200)
        else:
            return Response({'message': 'No pending requests for the elevator'}, status=200)
    except Elevator.DoesNotExist:
        return Response({'message': 'Invalid elevator number'}, status=404)


@api_view(['GET'])
def get_elevator_status(request, elevator_number):
    try:
        elevator = Elevator.objects.get(elevator_number=elevator_number)
        status = elevator.status
        return Response({'status': status}, status=200)
    except Elevator.DoesNotExist:
        return Response({'message': 'Invalid elevator number'}, status=404)

@api_view(['POST'])
def operate_elevator_door(request):
    elevator_number = request.data.get('elevator_number')
    action = request.data.get('action')

    try:
        elevator = Elevator.objects.get(elevator_number=elevator_number)
    except Elevator.DoesNotExist:
        return Response({'message': f'Elevator with number {elevator_number} does not exist'}, status=404)


    if action == 'open':
        if elevator.is_available:
            elevator.open_door()
            return Response({'message': f'Door of elevator {elevator_number} opened'}, status=200)
        else:
            return Response({'message': f'Door of elevator {elevator_number} busy'}, status=200)
    elif action == 'close':
        if elevator.is_door_opens:
            elevator.close_door()
            return Response({'message': f'Door of elevator {elevator_number} closed'}, status=200)
        else:
            return Response({'message': f'Door of elevator {elevator_number} closed'}, status=200)
    else:
        return Response({'message': 'Invalid action'}, status=400)

def get_optimal_elevator(floor):
    available_elevators = Elevator.objects.filter(is_available=True, is_operational=True)

    if available_elevators.count() > 0:
        nearest_elevator = min(
            available_elevators,
            key=lambda elevator: abs(elevator.floor - floor)
        )

        return nearest_elevator

    else:
        # If no elevator is available, select the one with the least pending requests
        elevators = Elevator.objects.filter(is_operational=True)
        min_pending_requests = float('inf')
        optimal_elevator = None

        for elevator in elevators:
            pending_requests = Request.objects.filter(elevator=elevator).count()

            if pending_requests < min_pending_requests:
                min_pending_requests = pending_requests
                optimal_elevator = elevator

        return optimal_elevator