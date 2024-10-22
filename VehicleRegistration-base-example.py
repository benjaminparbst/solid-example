# Base Example before SOLID
class VehicleRegistrar:
    def __init__(self):
        self.vehicles = []

    def register_vehicle(self, name, vehicle_type, price):
        if name in self.vehicles:
            self.set_status("Already registered", name, 0)
        else:
            self.vehicles.append(name)
            fee = self.calculate_fee(vehicle_type, price)
            self.set_status("Registered", name, fee)

    def set_status(self, status, vehicle_name, fee):
        print(f"Vehicle {vehicle_name}: {status}, price: {fee}kr")

    def calculate_fee(self, vehicle_type, price):
        if vehicle_type == "Electric":
            return price * 1.1
        elif vehicle_type == "Gas":
            return price * 1.2
        else:
            raise Exception(f"Unknown vehicle type: {vehicle_type}")

# Example usage
registrar = VehicleRegistrar()

registrar.register_vehicle("Tesla", "Electric", 10000)
registrar.register_vehicle("Ford", "Gas", 10000)
registrar.register_vehicle("Tesla", "Electric", 10000)