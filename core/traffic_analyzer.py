"""
Analyzes traffic patterns and provides data for AI decisions.
"""

from typing import Dict, List, Tuple
from enum import Enum
from dataclasses import dataclass
import time

from core.vehicle import VehicleDirection


class TrafficPriority(Enum):
    """Traffic priority levels for AI decision making."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5
    EMERGENCY = 10


@dataclass
class ApproachData:
    """Data collected for one intersection approach."""
    vehicle_count: int = 0
    total_wait_time: float = 0.0
    max_wait_time: float = 0.0
    average_wait_time: float = 0.0
    longest_waiting_vehicle: float = 0.0
    emergency_vehicles: int = 0

    def update(self, wait_time: float, is_emergency: bool = False) -> None:
        """Update statistics for this approach."""
        self.vehicle_count += 1
        self.total_wait_time += wait_time
        self.max_wait_time = max(self.max_wait_time, wait_time)

        if wait_time > self.longest_waiting_vehicle:
            self.longest_waiting_vehicle = wait_time

        if is_emergency:
            self.emergency_vehicles += 1

        if self.vehicle_count > 0:
            self.average_wait_time = self.total_wait_time / self.vehicle_count

    def get_priority_score(self) -> float:
        """Calculate a priority score for this approach."""
        # Base score from vehicle count
        count_score = min(self.vehicle_count * 2, 20)  # Cap at 20

        # Wait time score (more weight for long waits)
        wait_score = min(self.longest_waiting_vehicle * 0.5, 15)  # Cap at 15

        # Emergency vehicle bonus (highest priority)
        emergency_score = self.emergency_vehicles * 25

        return count_score + wait_score + emergency_score

    def reset(self) -> None:
        """Reset statistics for new analysis period."""
        self.vehicle_count = 0
        self.total_wait_time = 0.0
        self.max_wait_time = 0.0
        self.average_wait_time = 0.0
        self.longest_waiting_vehicle = 0.0
        self.emergency_vehicles = 0


class TrafficAnalyzer:
    """
    Analyzes traffic patterns at the intersection.
    Collects data for AI decision making.
    """

    def __init__(self):
        # Data for each approach
        self.approach_data = {
            VehicleDirection.NORTH: ApproachData(),
            VehicleDirection.SOUTH: ApproachData(),
            VehicleDirection.EAST: ApproachData(),
            VehicleDirection.WEST: ApproachData()
        }

        # Analysis timing
        self.last_analysis_time = time.time()
        self.analysis_interval = 2.0  # Analyze every 2 seconds
        self.current_phase_duration = 0.0

        # AI decision history
        self.decision_history: List[Dict] = []

    def update(self, vehicles, current_phase: str, phase_timer: float) -> Dict:
        """
        Update traffic analysis.

        Returns:
            Dictionary with analysis results and recommendations
        """
        current_time = time.time()
        self.current_phase_duration = phase_timer

        # Reset data if it's time for new analysis
        if current_time - self.last_analysis_time >= self.analysis_interval:
            self._analyze_traffic(vehicles, current_phase)
            self.last_analysis_time = current_time

        # Generate recommendation
        return self._generate_recommendation(current_phase)

    def _analyze_traffic(self, vehicles, current_phase: str) -> None:
        """Analyze current traffic situation."""
        # Reset all approach data
        for approach in self.approach_data.values():
            approach.reset()

        # Collect data from vehicles
        for vehicle in vehicles:
            if not vehicle.has_passed and vehicle.wait_time > 0:
                direction = vehicle.direction
                is_emergency = vehicle.type.name == "EMERGENCY"

                self.approach_data[direction].update(
                    vehicle.wait_time,
                    is_emergency
                )

        # Log analysis
        self._log_analysis(current_phase)

    def _log_analysis(self, current_phase: str) -> None:
        """Log current traffic analysis."""
        total_vehicles = sum(d.vehicle_count for d in self.approach_data.values())

        if total_vehicles > 0:
            # Calculate North-South vs East-West totals
            ns_vehicles = (self.approach_data[VehicleDirection.NORTH].vehicle_count +
                          self.approach_data[VehicleDirection.SOUTH].vehicle_count)
            ew_vehicles = (self.approach_data[VehicleDirection.EAST].vehicle_count +
                          self.approach_data[VehicleDirection.WEST].vehicle_count)

            ns_wait = max(self.approach_data[VehicleDirection.NORTH].longest_waiting_vehicle,
                         self.approach_data[VehicleDirection.SOUTH].longest_waiting_vehicle)
            ew_wait = max(self.approach_data[VehicleDirection.EAST].longest_waiting_vehicle,
                         self.approach_data[VehicleDirection.WEST].longest_waiting_vehicle)

            print(f"📊 Traffic Analysis: NS={ns_vehicles} cars ({ns_wait:.1f}s wait) | "
                  f"EW={ew_vehicles} cars ({ew_wait:.1f}s wait) | "
                  f"Current: {current_phase}")

    def _generate_recommendation(self, current_phase: str) -> Dict:
        """Generate AI recommendation for light changes."""
        # Calculate priority scores (only for vehicles NOT passed)
        ns_score = 0
        ew_score = 0
        has_emergency = False
        emergency_direction = None

        # Initialize car counts (will be calculated in all cases)
        ns_cars = sum(self.approach_data[d].vehicle_count
                     for d in [VehicleDirection.NORTH, VehicleDirection.SOUTH])
        ew_cars = sum(self.approach_data[d].vehicle_count
                     for d in [VehicleDirection.EAST, VehicleDirection.WEST])

        for direction, data in self.approach_data.items():
            # Only count vehicles that haven't passed yet
            if data.vehicle_count > 0:
                score = data.get_priority_score()

                if direction in [VehicleDirection.NORTH, VehicleDirection.SOUTH]:
                    ns_score += score
                else:
                    ew_score += score

                if data.emergency_vehicles > 0:
                    has_emergency = True
                    emergency_direction = direction

        # Determine recommended action
        if has_emergency and emergency_direction:
            # Emergency override
            emergency_is_ns = emergency_direction in [VehicleDirection.NORTH, VehicleDirection.SOUTH]
            recommended_phase = 'NS' if emergency_is_ns else 'EW'
            reason = f"🚨 EMERGENCY VEHICLE detected from {emergency_direction.value}"
            action = f"Switch to {recommended_phase} immediately"

        elif current_phase == 'NS':
            if ns_score == 0 and ew_score > 10:  # Only switch if significant traffic
                recommended_phase = 'EW'
                reason = f"No cars waiting NS, but {ew_cars} cars waiting EW"
                action = "Switch to EW to reduce wait times"
            elif ew_score > ns_score * 2.0 and self.current_phase_duration > 20:  # More conservative
                recommended_phase = 'EW'
                reason = f"EW has {ew_cars} cars ({ew_score:.1f}) vs NS {ns_cars} cars ({ns_score:.1f})"
                action = "Switch to EW - significantly more traffic"
            else:
                recommended_phase = 'NS'
                reason = f"NS has {ns_cars} cars, EW has {ew_cars} cars"
                action = f"Continue NS green ({max(5, 35 - int(self.current_phase_duration))}s remaining)"

        else:  # current_phase == 'EW'
            if ew_score == 0 and ns_score > 10:  # Only switch if significant traffic
                recommended_phase = 'NS'
                reason = f"No cars waiting EW, but {ns_cars} cars waiting NS"
                action = "Switch to NS to reduce wait times"
            elif ns_score > ew_score * 2.0 and self.current_phase_duration > 20:  # More conservative
                recommended_phase = 'NS'
                reason = f"NS has {ns_cars} cars ({ns_score:.1f}) vs EW {ew_cars} cars ({ew_score:.1f})"
                action = "Switch to NS - significantly more traffic"
            else:
                recommended_phase = 'EW'
                reason = f"EW has {ew_cars} cars, NS has {ns_cars} cars"
                action = f"Continue EW green ({max(5, 35 - int(self.current_phase_duration))}s remaining)"

        # Create recommendation
        recommendation = {
            'recommended_phase': recommended_phase,
            'reason': reason,
            'action': action,
            'ns_score': ns_score,
            'ew_score': ew_score,
            'ns_cars': ns_cars,
            'ew_cars': ew_cars,
            'has_emergency': has_emergency,
            'emergency_direction': emergency_direction.value if emergency_direction else None,
            'current_phase': current_phase,
            'should_switch': recommended_phase != current_phase
        }

        # Add to history
        self.decision_history.append(recommendation)
        if len(self.decision_history) > 10:
            self.decision_history.pop(0)

        return recommendation

    def get_traffic_summary(self) -> Dict:
        """Get summary of current traffic situation."""
        summary = {}

        for direction, data in self.approach_data.items():
            summary[direction.value] = {
                'vehicles': data.vehicle_count,
                'avg_wait': data.average_wait_time,
                'max_wait': data.max_wait_time,
                'emergencies': data.emergency_vehicles,
                'priority': data.get_priority_score()
            }

        return summary


# Test the traffic analyzer
if __name__ == "__main__":
    print("🧠 Traffic Analyzer Test")
    print("=" * 50)

    analyzer = TrafficAnalyzer()

    # Simulate some traffic data
    class MockVehicle:
        def __init__(self, direction, wait_time, is_emergency=False):
            self.direction = direction
            self.wait_time = wait_time
            self.has_passed = False
            self.type = type('MockType', (), {'name': 'EMERGENCY' if is_emergency else 'CAR'})()

    # Create test vehicles
    test_vehicles = [
        MockVehicle(VehicleDirection.NORTH, 15.0),
        MockVehicle(VehicleDirection.NORTH, 20.0),
        MockVehicle(VehicleDirection.SOUTH, 10.0),
        MockVehicle(VehicleDirection.EAST, 30.0, is_emergency=True),  # Emergency!
        MockVehicle(VehicleDirection.WEST, 5.0),
        MockVehicle(VehicleDirection.WEST, 8.0),
    ]

    # Test analysis
    result = analyzer.update(test_vehicles, 'NS', 25.0)

    print("Analysis Result:")
    print(f"Recommended Phase: {result['recommended_phase']}")
    print(f"Reason: {result['reason']}")
    print(f"Action: {result['action']}")
    print(f"NS Score: {result['ns_score']:.1f}")
    print(f"EW Score: {result['ew_score']:.1f}")
    print(f"Has Emergency: {result['has_emergency']}")

    print("\nTraffic Summary:")
    summary = analyzer.get_traffic_summary()
    for direction, data in summary.items():
        print(f"  {direction}: {data['vehicles']} cars, "
              f"avg wait: {data['avg_wait']:.1f}s, "
              f"priority: {data['priority']:.1f}")

    print("✅ Traffic analyzer test completed!")
