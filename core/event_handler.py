"""
Handles all user input events (keyboard, mouse, etc.)
"""

import pygame
from config.settings import DISPLAY
from core.vehicle_manager import SpawnRate

class EventHandler:
    """Handles all application events."""

    def __init__(self, app):
        self.app = app

    def handle_events(self) -> None:
        """Process all events in the event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.shutdown()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keyboard key press events."""
        if event.key == pygame.K_ESCAPE:
            self.app.shutdown()
        elif event.key == pygame.K_SPACE:
            self.app.toggle_pause()
        elif event.key == pygame.K_r:
            self.app.reset()
        elif event.key == pygame.K_F1:
            self._toggle_debug_mode()
        elif event.key == pygame.K_F2:
            self._take_screenshot()
        elif event.key == pygame.K_e:
            self.app.system_manager.toggle_emergency_mode()
        elif event.key == pygame.K_1:
            self.app.system_manager.force_phase('NS')
        elif event.key == pygame.K_2:
            self.app.system_manager.force_phase('EW')
        elif event.key == pygame.K_3:
            self.app.system_manager.cycle_phase()
        elif event.key == pygame.K_4:
            self.app.system_manager.set_spawn_rate(SpawnRate.LOW)
        elif event.key == pygame.K_5:
            self.app.system_manager.set_spawn_rate(SpawnRate.MEDIUM)
        elif event.key == pygame.K_6:
            self.app.system_manager.set_spawn_rate(SpawnRate.HIGH)
        elif event.key == pygame.K_7:
            self.app.system_manager.set_spawn_rate(SpawnRate.VERY_HIGH)
        elif event.key == pygame.K_a:
            self.app.ai_mode = not self.app.ai_mode
            status = "ENABLED 🧠" if self.app.ai_mode else "DISABLED ⏱️"
            print(f"🤖 AI Mode: {status}")

    def _toggle_debug_mode(self) -> None:
        """Toggle debug information display."""
        print("🔧 Debug mode toggle (not yet implemented)")

    def _take_screenshot(self) -> None:
        """Save a screenshot of the current frame."""
        try:
            timestamp = pygame.time.get_ticks()
            filename = f"screenshot_{timestamp}.png"
            pygame.image.save(self.app.screen, filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Failed to save screenshot: {e}")

    def _handle_keyup(self, event: pygame.event.Event) -> None:
        """Handle keyboard key release events."""
        pass  # Can be implemented for smooth controls

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """Handle mouse click events."""
        pass  # Will be implemented when we add UI controls
