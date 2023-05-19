from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Drone, Position, Trip
from .routing import calculate_shortest_path
import requests
import json

class DroneAPI(APIView):
    def post(self, request):
        # Extract the drone's current position, pickup position, and destination position from the request
        data = request.data
        drone_position = data.get('drone_position')
        pickup_position = data.get('pickup_position')
        delivery_position = data.get('delivery_position')

        # Get the drone object. If it does not exist, create a new one
        drone, created = Drone.objects.get_or_create(current_position=drone_position)

        # Get the pickup position object. If it does not exist, create a new one
        pickup, created = Position.objects.get_or_create(coordinate=pickup_position)

        # Get the delivery position object. If it does not exist, create a new one
        delivery, created = Position.objects.get_or_create(coordinate=delivery_position)

        # Send a GET request to the given API endpoint to get the time required to move between all the immediate vertical and horizontal coordinates
        api_uri = 'https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f'
        response = requests.get(api_uri)
        data = json.loads(response.text)

        # Calculate the fastest path and total time taken using the routing algorithm
        path_to_pickup, time_to_pickup = calculate_shortest_path(data, drone_position, pickup_position)
        path_to_delivery, time_to_delivery = calculate_shortest_path(data, pickup_position, delivery_position)

        # Merge the paths and calculate the total time
        # We remove the pickup position from the second path to avoid duplication
        total_path = path_to_pickup + path_to_delivery[1:]
        total_time = time_to_pickup + time_to_delivery

        # Create a new trip
        trip = Trip.objects.create(drone=drone, pickup=pickup, destination=delivery, total_time=total_time)

        # Return the fastest path and total time taken
        return Response({'path': total_path, 'time': total_time})

class TripHistoryAPI(APIView):
    def get(self, request):
        # Get the last 10 trips performed by the drone
        trips = Trip.objects.order_by('-created_at')[:10]

        # Extract the details of each trip
        trip_details = [{'drone': trip.drone.current_position, 'pickup': trip.pickup.coordinate, 'destination': trip.destination.coordinate, 'total_time': trip.total_time} for trip in trips]

        # Return the trip details
        return Response(trip_details)
