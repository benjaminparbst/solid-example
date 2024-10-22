# Open/Closed Principle Example
class VehicleRegistrar:
    def __init__(self,fee_calculater,status_reporter):
        self.vehicles = []
        self.fee_calculater = fee_calculater
        self.status_reporter = status_reporter

    def register_vehicle(self, name, vehicle_type, price):
        if name in self.vehicles:
            self.status_reporter.set_status("Already registered", name, 0)
        else:
            self.vehicles.append(name)
            fee = self.fee_calculater.calculate_fee(vehicle_type, price)
            self.status_reporter.set_status("Registered", name, fee)

class StatusReporter:
    def set_status(self, status, vehicle_name, fee):
        print(f"Vehicle {vehicle_name}: {status}, price: {fee}kr")

class FeeCalculater:
    def __init__(self):
        self.strategies = {}

    def add_strategy(self, vehicle_type, strategy):
        self.strategies[vehicle_type] = strategy

    def calculate_fee(self, vehicle_type, price):
        if vehicle_type in self.strategies:
            return self.strategies[vehicle_type].calculate(price)
        else:
            raise Exception(f"Unknown vehicle type: {vehicle_type}")

class ElectricVehicleStrategy:
    def calculate(self, price):
        return price * 1.1
    
class GasVehicleStrategy:
    def calculate(self, price):
        return price * 1.2
    
class DieselVehicleStrategy:
    def calculate(self, price):
        return price * 1.3

# Example usage
fee_calculater = FeeCalculater()
fee_calculater.add_strategy("Electric", ElectricVehicleStrategy())
fee_calculater.add_strategy("Gas", GasVehicleStrategy())
fee_calculater.add_strategy("Diesel", DieselVehicleStrategy())

status_reporter = StatusReporter()

registrar = VehicleRegistrar(fee_calculater,status_reporter)
registrar.register_vehicle("Tesla", "Electric", 10000)
registrar.register_vehicle("Ford", "Gas", 10000)
registrar.register_vehicle("Tesla", "Electric", 10000)
registrar.register_vehicle("Kia", "Diesel", 10000)