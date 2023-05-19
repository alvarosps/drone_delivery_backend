from django.test import TestCase
from .models import Drone, Position, Trip
from .api import DroneAPI, TripHistoryAPI
from .routing import calculate_shortest_path
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

class DroneModelTest(TestCase):
    def setUp(self):
        Drone.objects.create(current_position='A1')

    def test_drone_creation(self):
        drone = Drone.objects.get(current_position='A1')
        self.assertEqual(drone.current_position, 'A1')


class PositionModelTest(TestCase):
    def setUp(self):
        Position.objects.create(coordinate='B2')

    def test_position_creation(self):
        position = Position.objects.get(coordinate='B2')
        self.assertEqual(position.coordinate, 'B2')


class TripModelTest(TestCase):
    def setUp(self):
        drone = Drone.objects.create(current_position='A1')
        pickup = Position.objects.create(coordinate='B2')
        delivery = Position.objects.create(coordinate='C3')
        Trip.objects.create(drone=drone, pickup=pickup, destination=delivery, total_time=26.7)

    def test_trip_creation(self):
        trip = Trip.objects.get(drone__current_position='A1')
        self.assertEqual(trip.drone.current_position, 'A1')
        self.assertEqual(trip.pickup.coordinate, 'B2')
        self.assertEqual(trip.destination.coordinate, 'C3')
        self.assertEqual(trip.total_time, 26.7)


class RoutingAlgorithmTest(TestCase):
    def test_calculate_shortest_path(self):
        graph = {'A1': {'B1': 13.42, 'A2': 23.55}, 'B1': {}}
        start = 'A1'
        end = 'B1'
        path, time = calculate_shortest_path(graph, start, end)
        self.assertEqual(path, ['A1', 'B1'])
        self.assertEqual(time, 13.42)


class DroneAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.drone = Drone.objects.create(current_position='A1')
        self.pickup = Position.objects.create(coordinate='B2')
        self.delivery = Position.objects.create(coordinate='C3')
    
    def test_drone_api_post(self):
        response = self.client.post('/api/drone/', {
            'drone_position': self.drone.current_position,
            'pickup_position': self.pickup.coordinate,
            'delivery_position': self.delivery.coordinate
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.drone.current_position, response.data['path'])
        self.assertIn(self.pickup.coordinate, response.data['path'])
        self.assertIn(self.delivery.coordinate, response.data['path'])
        self.assertGreater(response.data['time'], 0)


class TripHistoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_trip_history_api_get(self):
        response = self.client.get('/api/trip_history/')
        self.assertEqual(response.status_code, 200)
