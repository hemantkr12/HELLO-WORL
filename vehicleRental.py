from datetime import datetime
import math


class Vehicle:
    def __init__(self, vehicle_id, location, rate):
        self.vehicle_id = vehicle_id
        self.location = location
        self.available = True
        self.rate = rate

    def rent_vehicle(self):
        self.available = False

    def return_vehicle(self, return_station):
        self.available = True
        self.location = return_station

    def refuel(self, amount):
        pass


class Motorbike(Vehicle):
    def __init__(self, vehicle_id, location):
        super().__init__(vehicle_id, location, 1.5)
        self.capacity = 80
        self.fuel_level = 0

    def refuel(self, amount):
        self.fuel_level+=amount
        if self.fuel_level>self.capacity:
            self.capacity=self.fuel_level
        print(f'Your motorbike has been refueled to {self.fuel_level}L')


class ElectricScooter(Vehicle):
    def __init__(self, vehicle_id, location):
        super().__init__(vehicle_id, location, 1.1)
        self.battery_level = 0

    def refuel(self, amount):
        if self.check_battery_low():
            self.battery_level+=amount
            if self.battery_level>100:
                self.battery_level=100
            return f'Your scooter has been recharged to {self.battery_level}'
        else:
            pass

    def check_battery_low(self):
        if self.battery_level<20:
            print("ALERT: Time to recharge!")
            return True
        else:
            print(f"Battery level is at {self.battery_level}. so your scooter doesn't need charging")
            return False



class VehicleRental:
    motorbikes = [
        Motorbike('MB1', 'Selly Oak'),
        Motorbike('MB2', 'Bournville'),
        Motorbike('MB3', 'Harborne')
    ]
    scooters = [
        ElectricScooter('ES1', 'Selly Oak'),
        ElectricScooter('ES2', 'Bournville'),
        ElectricScooter('ES3', 'Harborne')
    ]

    def __init__(self):
        self.vehicle = None
        self.depart_station = None
        self.rent_time = None
        self.return_station = None
        self.return_time = None

    def rent_vehicle(self, vehicle):
        self.vehicle=vehicle
        vehicle.rent_vehicle()
        self.depart_station=vehicle.location
        self.rent_time=datetime.now()
        print(f'You have successfully rented vehicle {self.vehicle.vehicle_id} from {self.depart_station}')

    def return_vehicle(self, return_station):
        fare = 0
        self.return_station=return_station
        self.return_time=datetime.now()
        self.vehicle.return_vehicle(return_station)
        fare=self.calculate_fare()
        print(f'You have successfully returned vehicle {self.vehicle.vehicle_id} to {self.return_station}')
        print(f'The fare for this rental is £{fare:.2f}')


    def calculate_fare(self):
        rent_time = datetime.datetime.strptime(self.rent_time, '%H:%M:%S')
        return_time = datetime.datetime.strptime(self.return_time, '%H:%M:%S')

        # Calculate the difference in seconds
        time_diff_seconds = (return_time - rent_time).total_seconds()

        # Convert seconds to hours and round up
        rent_duration_hours = math.ceil(time_diff_seconds / 3600)

        fare = rent_duration_hours * self.vehicle.rate
        return fare


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.current_rental = None
        self.rental_history = []

    def rent_vehicle(self, vehicle: Vehicle):
        self.current_rental=VehicleRental()
        self.current_rental.rent_vehicle(vehicle)
        self.rental_history.append(self.current_rental)

    def return_vehicle(self, return_station):
        self.current_rental.return_vehicle(return_station)
        self.current_rental=None

    def display_rental_history(self):
        print(f'Rental history for {self.name} with ID: {self.user_id}')
        for rental in self.rental_history:
            print(f'Vehicle {rental.vehicle.vehicle_id}')
            print(f'  Rented from: {rental.depart_station} at {rental.rent_time}')
            if rental.return_station:
                print(f'  Returned to: {rental.return_station} at {rental.return_time}')
            else:
                print(f'  Status: Currently rented')
            print('-' * 55)


def display_available_vehicles():
    for vehicle in VehicleRental.motorbikes:
        print (f'Motorbike {vehicle.vehicle_id} is available from {vehicle.location}')
    for vehicle in VehicleRental.scooters:
        print(f'Scooter {vehicle.vehicle_id} is available from {vehicle.location}')


def main():
    users = {
        'U1': User('U1', 'Evie'),
        'U2': User('U2', 'Nathan')
    }
    current_user = None
    while True:
        if not current_user:
            user_id = input('Please enter your user ID: ')
            if user_id in users:
                current_user=users[user_id]
                print(f'Welcome {current_user.name}')

            else:
                print(f'No user exists with Id {user_id}')
                continue
        try:
            choice = int(input('Book a Motorbike or an Electric Scooter\n'
                               '1. Display available vehicles\n'
                               '2. Rent a vehicle\n'
                               '3. Return a vehicle\n'
                               '4. Refuel / Recharge a vehicle\n'
                               '5. Display user history\n'
                               '6. Logout\n'
                               '7. Exit\n'))
        except ValueError:
            print('You must enter a number from 1-7')
            continue

        match choice:
            case 1:
                display_available_vehicles()
            case 2:
                if not current_user.current_rental:
                    borrow_station = input('Please enter your current station: ')
                    vehicle_type = input('Would you like to rent a (b)ike or a (s)cooter: ')
                    if vehicle_type=='b' or vehicle_type=='s':
                        for motorbike in VehicleRental.motorbikes:
                            if borrow_station==motorbike.location and vehicle_type=='b':
                                pass
                            else:
                                print(f'No motorbikes are available to rent at {borrow_station}')
                                continue
                        for scooter in VehicleRental.scooters:
                            if borrow_station==scooter.location and vehicle_type=='s':
                                pass
                            else:
                                print(f'No scooters are available to rent at {borrow_station}')
                    else:
                        print(f"Invalid option, you must pick 'b' (bike) or a 's' (scooter)")
                        break
                    for i,motorbike in enumerate(VehicleRental.motorbikes,1):
                        if motorbike.location==borrow_station:
                            print(f'{i}. {motorbike}')
                            current_user.rent_vehicle(motorbike)
                    for i,scooter in enumerate(VehicleRental.scooters,1):
                        if scooter.location==borrow_station:
                            print(f'{i}. {scooter}')
                            current_user.rent_vehicle(scooter)

                else:
                    print("You've already got a vehicle on loan")

            case 3:
                if current_user.current_rental:
                    return_station = input('Please enter the returning station: ')
                    current_user.return_vehicle(return_station)
                else:
                    print("You've not got a vehicle on loan, so can't return anything")
            case 4:
                if current_user.current_rental:
                    current_user.vehicle.refuel(50)
                else:
                    print("You've not got a vehicle on loan, so can't refuel/recharge anything")
            case 5:
                current_user.display_rental_history()
            case 6:
                current_user = None
            case 7:
                break
            case _:
                print('Invalid choice entered. You must enter a number from 1-7')


if __name__ == '__main__':
    main()
