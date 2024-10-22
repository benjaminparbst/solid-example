# Dependency Inversion Principle Example
from abc import ABC, abstractmethod

# 1. Abstraction for Price-Based Fee Calculation (NEW)
class PriceBasedFeeStrategy(ABC):  # Abstract base class for price-based strategies
    @abstractmethod
    def calculate(self, price):
        pass


# 2. Abstraction for Exemption-Based Fee Calculation (NEW)
class ExemptionBasedFeeStrategy(ABC):  # Abstract base class for exemption-based strategies
    @abstractmethod
    def calculate(self, exemption):
        pass


# 3. Abstraction for Fee Calculater (CHANGED to handle both price and exemption strategies)
class FeeCalculaterInterface(ABC):  
    @abstractmethod
    def calculate_fee(self, vehicle_type, price=None, exemption=None):
        pass


# 4. Abstraction for StatusReporter (Unchanged)

class StatusReporterInterface(ABC):
    @abstractmethod
    def set_status(self, status, vehicle_name, fee):
        pass


# 5. High-level class VehicleRegistrar (Unchanged, still depends on abstractions)
class VehicleRegistrar:
    def __init__(self, fee_calculater: FeeCalculaterInterface, status_reporter: StatusReporterInterface):
        self.vehicles = []
        self.fee_calculater = fee_calculater
        self.status_reporter = status_reporter

    def register_vehicle(self, name, vehicle_type, price=None, exemption=None):
        if name in self.vehicles:
            self.status_reporter.set_status("Already registered", name, 0)
        else:
            self.vehicles.append(name)
            fee = self.fee_calculater.calculate_fee(vehicle_type, price, exemption)
            self.status_reporter.set_status("Registered", name, fee)


# 6. Concrete StatusReporter Class (Unchanged)

class StatusReporter(StatusReporterInterface):
    def set_status(self, status, vehicle_name, fee):
        print(f"Vehicle {vehicle_name}: {status}, price: {fee}kr")


class FileStatusReporter(StatusReporterInterface):
    def set_status(self, status, vehicle_name, fee):
        print(f"LOG: Vehicle {vehicle_name}: {status}, price: {fee}kr")



# 7. Concrete FeeCalculater Class (CHANGED to handle separate strategies for price and exemption)
class FeeCalculater(FeeCalculaterInterface):
    def __init__(self):
        self.price_strategies = {}  # Stores strategies for price-based vehicles
        self.exemption_strategies = {}  # Stores strategies for exemption-based vehicles

    def add_price_strategy(self, vehicle_type, strategy: PriceBasedFeeStrategy):
        self.price_strategies[vehicle_type] = strategy

    def add_exemption_strategy(self, vehicle_type, strategy: ExemptionBasedFeeStrategy):
        self.exemption_strategies[vehicle_type] = strategy

    def calculate_fee(self, vehicle_type, price=None, exemption=None):
        if vehicle_type in self.price_strategies:
            return self.price_strategies[vehicle_type].calculate(price)
        elif vehicle_type in self.exemption_strategies:
            return self.exemption_strategies[vehicle_type].calculate(exemption)
        else:
            raise Exception(f"Unknown vehicle type: {vehicle_type}")


# 8. Concrete Strategy for Electric Vehicles (CHANGED: Implements PriceBasedFeeStrategy)
class ElectricVehicleStrategy(PriceBasedFeeStrategy):
    def calculate(self, price):
        return price * 1.1


# 9. Concrete Strategy for Gas Vehicles (CHANGED: Implements PriceBasedFeeStrategy)
class GasVehicleStrategy(PriceBasedFeeStrategy):
    def calculate(self, price):
        return price * 1.2


# 10. Concrete Strategy for Diesel Vehicles (CHANGED: Implements PriceBasedFeeStrategy)
class DieselVehicleStrategy(PriceBasedFeeStrategy):
    def calculate(self, price):
        return price * 1.3


# 11. Concrete Strategy for Exempt Vehicles (CHANGED: Implements ExemptionBasedFeeStrategy)
class ExemptFromFeeStrategy(ExemptionBasedFeeStrategy):
    def calculate(self, exemption):
        if exemption == "Valid":
            return 0
        else:
            raise Exception("Not exempt from fee")


# 12. Example Usage with the Refactored Design

# Creating the fee calculator (Unchanged)
fee_calculater = FeeCalculater()

# Adding strategies (CHANGED: Separate price and exemption-based strategies)
fee_calculater.add_price_strategy("Electric", ElectricVehicleStrategy())
fee_calculater.add_price_strategy("Gas", GasVehicleStrategy())
fee_calculater.add_price_strategy("Diesel", DieselVehicleStrategy())
fee_calculater.add_exemption_strategy("Exempt", ExemptFromFeeStrategy())

# Creating a status reporter (Unchanged)
status_reporter = StatusReporter()
file_reporter = FileStatusReporter()

# Creating the vehicle registrar (Unchanged)
registrar = VehicleRegistrar(fee_calculater, file_reporter)

# Registering different vehicles
registrar.register_vehicle("Tesla", "Electric", price=10000)  # Uses price-based strategy
registrar.register_vehicle("Ford", "Gas", 10000)  # Uses price-based strategy
registrar.register_vehicle("Kia", "Diesel", 10000)  # Uses price-based strategy
registrar.register_vehicle("Skoda", "Exempt", exemption="Valid")  # Uses exemption-based strategy