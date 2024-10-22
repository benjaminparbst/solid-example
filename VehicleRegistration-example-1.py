# Single Responsibility Example
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
    def calculate_fee(self, vehicle_type, price):
        if vehicle_type == "Electric":
            return price * 1.1
        elif vehicle_type == "Gas":
            return price * 1.2
        elif vehicle_type == "Diesel":
            return price * 1.3
        else:
            raise Exception(f"Unknown vehicle type: {vehicle_type}")

# Example usage
status_reporter = StatusReporter()
fee_calculater = FeeCalculater()
registrar = VehicleRegistrar(fee_calculater,status_reporter)
registrar.register_vehicle("Tesla", "Electric", 10000)
registrar.register_vehicle("Ford", "Gas", 10000)
registrar.register_vehicle("Tesla", "Electric", 10000)