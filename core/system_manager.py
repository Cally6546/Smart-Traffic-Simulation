"""
Manages all game systems (traffic lights, vehicles, AI, etc.)
"""

import pygame
from config.settings import DISPLAY, INTERSECTION
from core.intersection import IntersectionRenderer
from core.traffic_light import TrafficLightSystem
from core.vehicle_manager import VehicleManager, SpawnRate
from core.traffic_analyzer import TrafficAnalyzer

class SystemManager:
    """Manages all game systems."""

    def __init__(self, app):
        self.app = app
        self.emergency_mode = False
        self.next_phase_change = 0.0
        self.current_ai_decision = {
            'recommended_phase': 'NS',
            'reason': 'Starting up...',
            'action': 'Initializing AI',
            'ns_score': 0,
            'ew_score': 0,
            'ns_cars': 0,
            'ew_cars': 0,
            'has_emergency': False,
            'should_switch': False
        }

        # Create subsystems
        self._create_systems()

    def _create_systems(self) -> None:
        """Create all intersection components."""
        # Create intersection renderer
        self.intersection_renderer = IntersectionRenderer()

        # Create traffic light system
        center_x, center_y = DISPLAY.CENTER
        self.traffic_lights = TrafficLightSystem(center_x, center_y, INTERSECTION.ROAD_WIDTH)

        # Create vehicle manager
        self.vehicle_manager = VehicleManager(self.traffic_lights)
        self.vehicle_manager.set_spawn_rate(SpawnRate.MEDIUM)

        # Create traffic analyzer
        self.traffic_analyzer = TrafficAnalyzer()

        # Calculate next phase change time
        self._update_next_phase_change()

    def _update_next_phase_change(self) -> None:
        """Update the time until next phase change."""
        if self.traffic_lights:
            self.next_phase_change = self.traffic_lights.get_time_until_change()

    def toggle_emergency_mode(self) -> None:
        """Toggle emergency vehicle priority mode."""
        if self.traffic_lights:
            if not self.emergency_mode:
                # Activate emergency from north
                self.traffic_lights.set_emergency('north')
                self.emergency_mode = True
                print("🚨 EMERGENCY MODE: Ambulance approaching from NORTH")
            else:
                # Deactivate emergency
                self.traffic_lights.set_emergency(None)
                self.emergency_mode = False
                print("✅ Emergency mode deactivated")

    def force_phase(self, phase: str) -> None:
        """Force a specific traffic light phase."""
        if self.traffic_lights:
            self.traffic_lights.current_phase = phase
            self.traffic_lights.phase_timer = 0
            self._update_next_phase_change()
            print(f"🔧 Forced phase: {phase}")

    def cycle_phase(self) -> None:
        """Cycle to next phase immediately."""
        if self.traffic_lights:
            current = self.traffic_lights.current_phase
            next_phase = 'EW' if current == 'NS' else 'NS'
            self.force_phase(next_phase)

    def set_spawn_rate(self, rate: SpawnRate) -> None:
        """Set vehicle spawn rate."""
        if self.vehicle_manager:
            self.vehicle_manager.set_spawn_rate(rate)
            rate_names = {
                SpawnRate.LOW: "LOW (night time)",
                SpawnRate.MEDIUM: "MEDIUM (normal)",
                SpawnRate.HIGH: "HIGH (rush hour)",
                SpawnRate.VERY_HIGH: "VERY HIGH (gridlock)"
            }
            print(f"🚗 Spawn rate: {rate_names.get(rate, 'UNKNOWN')}")

    def _apply_ai_decision(self) -> None:
        """Apply AI decision to traffic lights with conservative switching."""
        if not self.traffic_lights or not self.current_ai_decision:
            return

        decision = self.current_ai_decision

        # Only apply if AI recommends switching
        if decision['should_switch']:
            # Check conditions for switching
            current_phase = self.traffic_lights.current_phase
            recommended_phase = decision['recommended_phase']

            # Don't switch if we just switched recently (min 15 seconds per phase)
            if self.traffic_lights.phase_timer < 15:
                return

            # For emergency, switch immediately
            if decision['has_emergency']:
                self.traffic_lights.current_phase = recommended_phase
                self.traffic_lights.phase_timer = 0
                self._update_next_phase_change()
                print(f"🚨 EMERGENCY: Switching to {recommended_phase}")

            # For normal traffic, only switch if significant difference
            elif current_phase != recommended_phase:
                # Get traffic scores
                ns_score = decision.get('ns_score', 0)
                ew_score = decision.get('ew_score', 0)
                ns_cars = decision.get('ns_cars', 0)
                ew_cars = decision.get('ew_cars', 0)

                if current_phase == 'NS':
                    # Only switch from NS to EW if EW has 2x more traffic OR NS has no cars
                    should_switch = (ew_cars > 0 and ns_cars == 0) or (ew_score > ns_score * 2.0)
                    if should_switch:
                        self.traffic_lights.current_phase = 'EW'
                        self.traffic_lights.phase_timer = 0
                        self._update_next_phase_change()
                        print(f"🧠 AI: Switching to EW (NS:{ns_cars} cars, EW:{ew_cars} cars)")
                else:  # current_phase == 'EW'
                    # Only switch from EW to NS if NS has 2x more traffic OR EW has no cars
                    should_switch = (ns_cars > 0 and ew_cars == 0) or (ns_score > ew_score * 2.0)
                    if should_switch:
                        self.traffic_lights.current_phase = 'NS'
                        self.traffic_lights.phase_timer = 0
                        self._update_next_phase_change()
                        print(f"🧠 AI: Switching to NS (EW:{ew_cars} cars, NS:{ns_cars} cars)")

    def update(self, delta_time: float) -> None:
        """Update all systems."""
        if self.app.state.name == "RUNNING":
            # Update traffic lights
            if self.traffic_lights:
                self.traffic_lights.update(delta_time)
                self._update_next_phase_change()

            # Update vehicles
            if self.vehicle_manager:
                self.vehicle_manager.update(delta_time)

            # Update AI traffic analysis
            if (self.traffic_analyzer and self.vehicle_manager and
                self.traffic_lights and self.app.ai_mode):

                # Get AI recommendation
                vehicles = self.vehicle_manager.vehicles
                current_phase = self.traffic_lights.current_phase
                phase_timer = self.traffic_lights.phase_timer

                self.current_ai_decision = self.traffic_analyzer.update(
                    vehicles, current_phase, phase_timer
                )

                # Apply AI decision (if it recommends switching)
                self._apply_ai_decision()

    def render(self, screen: pygame.Surface) -> None:
        """Render all systems."""
        # Render intersection
        if hasattr(self, 'intersection_renderer'):
            self.intersection_renderer.render(screen)

        # Render traffic lights
        if self.traffic_lights:
            self.traffic_lights.draw(screen)

        # Render vehicles
        if self.vehicle_manager:
            self.vehicle_manager.draw(screen)

    def reset(self) -> None:
        """Reset all systems."""
        self.emergency_mode = False

        # Reset traffic lights
        center_x, center_y = DISPLAY.CENTER
        self.traffic_lights = TrafficLightSystem(center_x, center_y, INTERSECTION.ROAD_WIDTH)

        # Reset vehicle manager
        self.vehicle_manager.reset()
        self.vehicle_manager = VehicleManager(self.traffic_lights)
        self.vehicle_manager.set_spawn_rate(SpawnRate.MEDIUM)

        # Reset traffic analyzer
        self.traffic_analyzer = TrafficAnalyzer()

        # Reset AI decision
        self.current_ai_decision = {
            'recommended_phase': 'NS',
            'reason': 'Starting up...',
            'action': 'Initializing AI',
            'ns_score': 0,
            'ew_score': 0,
            'ns_cars': 0,
            'ew_cars': 0,
            'has_emergency': False,
            'should_switch': False
        }

        self._update_next_phase_change()
