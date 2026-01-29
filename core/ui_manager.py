"""
Manages all UI rendering and display.
"""

import pygame
from config.settings import DISPLAY, COLORS, FONT_MEDIUM

class UIManager:
    """Manages all UI rendering."""

    def __init__(self, app):
        self.app = app

    def render(self, screen: pygame.Surface) -> None:
        """Render all UI elements."""
        # Render traffic information
        self._render_traffic_info(screen)

        # Render UI overlay
        self._render_ui_overlay(screen)

    def _render_traffic_info(self, screen: pygame.Surface) -> None:
        """Render traffic-specific information."""
        if not hasattr(self.app.system_manager, 'traffic_lights'):
            return

        font = pygame.font.SysFont('Arial', 20)
        center_x, center_y = DISPLAY.CENTER

        # Draw phase indicator
        phase = self.app.system_manager.traffic_lights.current_phase
        phase_text = f"{phase} - {'GREEN' if self.app.system_manager.traffic_lights.phase_timer < 30 else 'YELLOW' if self.app.system_manager.traffic_lights.phase_timer < 33 else 'RED'}"
        phase_surface = font.render(f"Phase: {phase_text}", True,
                                  COLORS.GREEN if 'GREEN' in phase_text else
                                  COLORS.YELLOW if 'YELLOW' in phase_text else
                                  COLORS.RED)

        # Position near intersection
        info_x = center_x - 100
        info_y = center_y - 200

        # Background for readability
        bg_rect = pygame.Rect(info_x - 10, info_y - 5,
                            phase_surface.get_width() + 20,
                            phase_surface.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100, 200), bg_rect, 2, border_radius=5)

        screen.blit(phase_surface, (info_x, info_y))

        # Draw time to change
        time_text = f"Change in: {self.app.system_manager.next_phase_change:.1f}s"
        time_surface = font.render(time_text, True, COLORS.TEXT_WHITE)
        screen.blit(time_surface, (info_x, info_y + 30))

        # Draw emergency status
        if self.app.system_manager.emergency_mode:
            emergency_surface = font.render("🚨 EMERGENCY MODE ACTIVE", True, COLORS.RED)
            screen.blit(emergency_surface, (info_x, info_y + 60))

        # Draw AI Mode status
        ai_color = COLORS.GREEN if self.app.ai_mode else COLORS.RED
        ai_status = "🤖 AI: ON" if self.app.ai_mode else "🤖 AI: OFF"
        ai_surface = font.render(ai_status, True, ai_color)
        screen.blit(ai_surface, (info_x, info_y + 90))

        # Draw AI thinking (if enabled)
        if self.app.ai_mode and self.app.system_manager.current_ai_decision:
            decision = self.app.system_manager.current_ai_decision

            # AI recommendation
            rec_color = COLORS.GREEN if decision['recommended_phase'] == 'NS' else COLORS.YELLOW
            ai_text = f"AI suggests: {decision['recommended_phase']}"
            ai_surface = font.render(ai_text, True, rec_color)
            screen.blit(ai_surface, (info_x, info_y + 120))

            # Traffic counts
            ns_cars = decision.get('ns_cars', 0)
            ew_cars = decision.get('ew_cars', 0)
            count_text = f"Cars: NS={ns_cars} | EW={ew_cars}"
            count_surface = font.render(count_text, True, COLORS.TEXT_WHITE)
            screen.blit(count_surface, (info_x, info_y + 150))

            # Traffic scores
            ns_score = decision.get('ns_score', 0)
            ew_score = decision.get('ew_score', 0)
            score_text = f"Scores: NS={ns_score:.1f} | EW={ew_score:.1f}"
            score_surface = font.render(score_text, True, COLORS.TEXT_WHITE)
            screen.blit(score_surface, (info_x, info_y + 180))

            # AI decision reason (shortened)
            if decision['has_emergency']:
                reason_text = "🚨 EMERGENCY PRIORITY"
            else:
                # Shorten reason if too long
                reason = decision['reason'][:40] + "..." if len(decision['reason']) > 40 else decision['reason']
                reason_text = f"Reason: {reason}"

            reason_surface = font.render(reason_text, True, COLORS.TEXT_WHITE)
            screen.blit(reason_surface, (info_x, info_y + 210))

        # Draw vehicle statistics
        if hasattr(self.app.system_manager, 'vehicle_manager'):
            stats = self.app.system_manager.vehicle_manager.get_statistics()

            # Vehicle count
            vehicle_text = f"Total Vehicles: {stats['current_count']} | Passed: {stats['total_passed']}"
            vehicle_surface = font.render(vehicle_text, True, COLORS.TEXT_WHITE)
            screen.blit(vehicle_surface, (info_x, info_y + 240))

            # Wait times
            if stats['total_passed'] > 0:
                wait_text = f"Wait: Avg={stats['average_wait_time']:.1f}s | Max={stats['max_wait_time']:.1f}s"
                wait_surface = font.render(wait_text, True, COLORS.TEXT_WHITE)
                screen.blit(wait_surface, (info_x, info_y + 270))

    def _render_ui_overlay(self, screen: pygame.Surface) -> None:
        """Render the UI overlay with current status."""
        # Status bar background
        status_bar = pygame.Surface((DISPLAY.WIDTH, 60), pygame.SRCALPHA)
        status_bar.fill((*COLORS.UI_BACKGROUND[:3], 220))  # Slightly more opaque
        screen.blit(status_bar, (0, 0))

        # Add separator line
        pygame.draw.line(screen, (100, 100, 100), (0, 60), (DISPLAY.WIDTH, 60), 2)

        # Status text
        status_lines = [
            f"State: {self.app.state.value}",
            f"Time: {self.app.elapsed_time:.1f}s",
            f"FPS: {self.app.clock.get_fps():.0f}",
            f"AI: {'ON 🧠' if self.app.ai_mode else 'OFF ⏱️'}"
        ]

        for i, line in enumerate(status_lines):
            text_surface = FONT_MEDIUM.render(line, True, COLORS.TEXT_WHITE)
            screen.blit(text_surface, (10, 5 + i * 15))

        # Controls help (expanded)
        controls = [
            "SPACE: Pause/Resume",
            "R: Reset",
            "E: Emergency",
            "A: AI Toggle",
            "1/2: Force Phase",
            "3: Cycle Phase",
            "4/5/6/7: Spawn Rate",
            "F2: Screenshot",
            "ESC: Quit"
        ]

        # Draw controls in two columns
        control_x = DISPLAY.WIDTH - 350
        for i, control in enumerate(controls):
            row = i % 5
            col = i // 5
            x = control_x + (col * 170)
            y = 5 + row * 15

            control_surface = FONT_MEDIUM.render(control, True, COLORS.TEXT_DIM)
            screen.blit(control_surface, (x, y))
