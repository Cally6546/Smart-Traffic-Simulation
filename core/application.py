"""
Main application class following Singleton pattern.
Manages the game loop, state, and high-level coordination.
"""

import pygame
import sys
import os
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DISPLAY, COLORS, FONT_MEDIUM, INTERSECTION
from core.performance import PerformanceMetrics
from core.ui_manager import UIManager
from core.event_handler import EventHandler
from core.system_manager import SystemManager

class AppState(Enum):
    """Possible states of the application."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    RESETTING = "resetting"
    SHUTTING_DOWN = "shutting_down"

class Application:
    """
    Main application controller (Singleton pattern).
    Manages the PyGame window, game loop, and high-level state.
    """

    _instance: Optional['Application'] = None
    _initialized: bool = False

    def __new__(cls):
        """Singleton pattern - ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the application (called only once)."""
        if self._initialized:
            return

        self._initialized = True
        self.state = AppState.INITIALIZING
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.running: bool = True
        self.performance = PerformanceMetrics()

        # Time tracking
        self.delta_time: float = 0.0
        self.elapsed_time: float = 0.0

        # AI mode (smart vs traditional)
        self.ai_mode = True  # Start with AI enabled

        # Initialize subsystems
        self._initialize_pygame()

        # Create managers
        self.system_manager = SystemManager(self)
        self.ui_manager = UIManager(self)
        self.event_handler = EventHandler(self)

        print("🎮 Application initialized successfully")

    def _initialize_pygame(self) -> None:
        """Initialize PyGame subsystems."""
        try:
            pygame.init()

            # Create the main window
            self.screen = pygame.display.set_mode(
                (DISPLAY.WIDTH, DISPLAY.HEIGHT),
                pygame.DOUBLEBUF | pygame.HWSURFACE  # Performance flags
            )
            pygame.display.set_caption("Smart Traffic Simulation with AI")

            # Initialize the clock for frame rate control
            self.clock = pygame.time.Clock()

            # Enable key repeat for better UX
            pygame.key.set_repeat(500, 50)

            self.state = AppState.RUNNING

        except pygame.error as e:
            print(f"❌ Failed to initialize PyGame: {e}")
            sys.exit(1)

    def toggle_pause(self) -> None:
        """Toggle between paused and running states."""
        if self.state == AppState.RUNNING:
            self.state = AppState.PAUSED
            print("⏸️ Simulation paused")
        elif self.state == AppState.PAUSED:
            self.state = AppState.RUNNING
            print("▶️ Simulation resumed")

    def reset(self) -> None:
        """Reset the simulation to initial state."""
        print("🔄 Resetting simulation...")
        self.state = AppState.RESETTING
        self.elapsed_time = 0.0

        # Reset systems
        self.system_manager.reset()

        self.state = AppState.RUNNING
        print("✅ Simulation reset complete")

    def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        print("🛑 Shutting down...")
        self.state = AppState.SHUTTING_DOWN
        self.running = False

    def update(self) -> None:
        """Update game logic based on current state."""
        if self.state == AppState.RUNNING:
            self.elapsed_time += self.delta_time
            self.system_manager.update(self.delta_time)

    def render(self) -> None:
        """Render the current frame."""
        if not self.screen:
            return

        # Clear screen
        self.screen.fill(COLORS.NIGHT_SKY)

        # Render all systems
        self.system_manager.render(self.screen)

        # Render UI
        self.ui_manager.render(self.screen)

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        self._print_welcome_message()

        while self.running:
            # Calculate delta time (time since last frame in seconds)
            self.delta_time = self.clock.tick(DISPLAY.FPS) / 1000.0

            # Update performance metrics
            frame_time = self.clock.get_time()
            self.performance.update(frame_time)

            # Process events
            self.event_handler.handle_events()

            # Update game state
            self.update()

            # Render frame
            self.render()

        self._cleanup()

    def _print_welcome_message(self) -> None:
        """Print welcome message and controls."""
        print("=" * 70)
        print("🚦 SMART TRAFFIC SIMULATION WITH ARTIFICIAL INTELLIGENCE")
        print("=" * 70)
        print("🤖 AI FEATURES (CONSERVATIVE MODE):")
        print("  • Switches only when 2x more traffic on other side")
        print("  • Minimum 15 seconds per phase")
        print("  • Emergency vehicles get immediate priority")
        print("  • Shows car counts and traffic scores")
        print("")
        print("🎮 CONTROLS:")
        print("  SPACE: Pause/Resume simulation")
        print("  R: Reset simulation")
        print("  A: Toggle AI Mode (Smart vs Traditional)")
        print("  E: Toggle emergency mode (ambulance)")
        print("  1: Force North-South green")
        print("  2: Force East-West green")
        print("  3: Cycle to next phase")
        print("  4/5/6/7: Vehicle spawn rate (Low/Med/High/Very High)")
        print("  F1: Debug mode")
        print("  F2: Take screenshot")
        print("  ESC: Quit")
        print("=" * 70)
        print("Starting simulation...")
        print("🚗 Vehicles will spawn automatically")
        print("🚦 AI makes conservative decisions")
        print("🚑 Emergency vehicles get priority")
        print("🤖 Watch AI thinking in the display!")

    def _cleanup(self) -> None:
        """Clean up resources before exit."""
        print("🧹 Cleaning up resources...")
        pygame.quit()
        print("👋 Goodbye!")
        sys.exit(0)

# Global access point for the application
def get_app() -> Application:
    """Get the singleton application instance."""
    return Application()

if __name__ == "__main__":
    # Test the application standalone
    app = get_app()
    app.run()
