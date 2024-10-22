# Interface Segregation Principle Example
class VehicleRegistrar:
    def __init__(self, fee_calculater, status_reporter):
        self.vehicles = []
        self.fee_calculater = fee_calculater
        self.status_reporter = status_reporter

    def register_vehicle(self, name, vehicle_type, price=None, exemption=None):
        if name in self.vehicles:
            self.status_reporter.set_status("Already registered", name, 0)
        else:
            self.vehicles.append(name)
            # Calls the new `calculate_fee` method which now handles both price and exemption
            fee = self.fee_calculater.calculate_fee(vehicle_type, price, exemption)
            self.status_reporter.set_status("Registered", name, fee)


class StatusReporter:
    def set_status(self, status, vehicle_name, fee):
        print(f"Vehicle {vehicle_name}: {status}, price: {fee}kr")


class FeeCalculater:
    def __init__(self):
        self.price_strategies = {}  # NEW - Holds strategies based on price
        self.exemption_strategies = {}  # NEW - Holds strategies based on exemption

    def add_price_strategy(self, vehicle_type, strategy):
        self.price_strategies[vehicle_type] = strategy

    def add_exemption_strategy(self, vehicle_type, strategy):
        self.exemption_strategies[vehicle_type] = strategy

    def calculate_fee(self, vehicle_type, price=None, exemption=None):
        if vehicle_type in self.price_strategies:
            return self.price_strategies[vehicle_type].calculate(price)
        elif vehicle_type in self.exemption_strategies:
            return self.exemption_strategies[vehicle_type].calculate(exemption)
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


class ExemptFromFeeStrategy:
    def calculate(self, exemption):
        if exemption == "Valid":
            return 0
        else:
            raise Exception("Not exempt from fee")


# Example usage with the new structure

# Creating the fee calculator
fee_calculater = FeeCalculater()

# Adding price-based strategies (CHANGED)
fee_calculater.add_price_strategy("Electric", ElectricVehicleStrategy())
fee_calculater.add_price_strategy("Gas", GasVehicleStrategy())
fee_calculater.add_price_strategy("Diesel", DieselVehicleStrategy())

# Adding exemption-based strategy (NEW)
fee_calculater.add_exemption_strategy("Exempt", ExemptFromFeeStrategy())

# Creating a status reporter
status_reporter = StatusReporter()

# Creating the vehicle registrar
registrar = VehicleRegistrar(fee_calculater, status_reporter)

# Registering different vehicles
registrar.register_vehicle("Tesla", "Electric", 10000)  # Uses price-based strategy
registrar.register_vehicle("Ford", "Gas", 10000)  # Uses price-based strategy
registrar.register_vehicle("Kia", "Diesel", price=10000)  # Uses price-based strategy
registrar.register_vehicle("Skoda", "Exempt", exemption="Valid")  # Uses exemption-based strategy