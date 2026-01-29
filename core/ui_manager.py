"""
Manages all UI rendering and display with polished design.
"""

import pygame
import time
from config.settings import DISPLAY, COLORS, FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_TITLE, FONT_SUBTITLE, BRAND_INFO

class UIManager:
    """Manages all UI rendering with modern design."""

    def __init__(self, app):
        self.app = app
        self.panel_corner_radius = 12
        self.blink_state = False
        self.last_blink_time = 0
        self.logo_animation = 0

        # Create fonts with better typography
        self.title_font = FONT_TITLE
        self.subtitle_font = FONT_SUBTITLE
        self.header_font = FONT_LARGE
        self.body_font = FONT_MEDIUM
        self.small_font = FONT_SMALL

        # Brand information
        self.group_name = BRAND_INFO["group_name"]
        self.creator_name = BRAND_INFO["creator"]
        self.version = BRAND_INFO["version"]
        self.description = BRAND_INFO["description"]

        # Pre-render brand elements for performance
        self._prerender_brand_elements()

    def _prerender_brand_elements(self):
        """Pre-render brand-related elements."""
        # Brand logo/icon
        self.brand_logo = self._create_brand_logo()

        # Create gradient patterns
        self._create_background_patterns()

        # Create decorative elements
        self._create_decorative_elements()

    def _create_brand_logo(self):
        """Create the INNOHUB KE brand logo."""
        logo_size = 32
        logo_surface = pygame.Surface((logo_size, logo_size), pygame.SRCALPHA)

        # Draw a stylized "I" for INNOHUB
        pygame.draw.rect(logo_surface, COLORS.BRAND_PRIMARY,
                        (logo_size//2 - 3, 4, 6, logo_size - 8), border_radius=3)

        # Draw gear/circle element
        center = logo_size // 2
        pygame.draw.circle(logo_surface, COLORS.BRAND_ACCENT, (center, center), 10, 2)

        # Add small dots around the circle
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            x = center + int(10 * pygame.math.Vector2(1, 0).rotate(angle).x)
            y = center + int(10 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(logo_surface, COLORS.BRAND_LIGHT, (x, y), 2)

        return logo_surface

    def _create_background_patterns(self):
        """Create background patterns."""
        # Main background pattern
        self.bg_pattern = pygame.Surface((DISPLAY.WIDTH, DISPLAY.HEIGHT), pygame.SRCALPHA)

        # Subtle grid pattern
        grid_color = (*COLORS.BRAND_PRIMARY[:3], 10)
        for x in range(0, DISPLAY.WIDTH, 80):
            pygame.draw.line(self.bg_pattern, grid_color, (x, 0), (x, DISPLAY.HEIGHT), 1)
        for y in range(0, DISPLAY.HEIGHT, 80):
            pygame.draw.line(self.bg_pattern, grid_color, (0, y), (DISPLAY.WIDTH, y), 1)

        # Corner accents
        corner_size = 200
        for corner in [(0, 0), (DISPLAY.WIDTH, 0), (0, DISPLAY.HEIGHT), (DISPLAY.WIDTH, DISPLAY.HEIGHT)]:
            corner_surf = pygame.Surface((corner_size, corner_size), pygame.SRCALPHA)
            for i in range(corner_size):
                alpha = int(50 * (1 - i/corner_size))
                color = (*COLORS.BRAND_PRIMARY[:3], alpha)
                if corner[0] == 0 and corner[1] == 0:
                    pygame.draw.line(corner_surf, color, (0, i), (i, 0), 1)
                elif corner[0] == DISPLAY.WIDTH and corner[1] == 0:
                    pygame.draw.line(corner_surf, color, (corner_size - i, 0), (corner_size, i), 1)
                elif corner[0] == 0 and corner[1] == DISPLAY.HEIGHT:
                    pygame.draw.line(corner_surf, color, (0, corner_size - i), (i, corner_size), 1)
                else:
                    pygame.draw.line(corner_surf, color, (corner_size - i, corner_size),
                                   (corner_size, corner_size - i), 1)
            self.bg_pattern.blit(corner_surf, (corner[0] - (0 if corner[0] == 0 else corner_size),
                                             corner[1] - (0 if corner[1] == 0 else corner_size)))

    def _create_decorative_elements(self):
        """Create decorative UI elements."""
        # Create a modern button template
        self.button_template = pygame.Surface((150, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.button_template, (*COLORS.BRAND_PRIMARY[:3], 30),
                        (0, 0, 150, 40), border_radius=8)
        pygame.draw.rect(self.button_template, (*COLORS.BRAND_PRIMARY[:3], 150),
                        (0, 0, 150, 40), 2, border_radius=8)

        # Create status indicator templates
        self.indicator_on = self._create_indicator(True)
        self.indicator_off = self._create_indicator(False)

    def _create_indicator(self, is_on):
        """Create status indicator."""
        size = 12
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        if is_on:
            pygame.draw.circle(surf, COLORS.GREEN, (size//2, size//2), size//2)
            pygame.draw.circle(surf, (*COLORS.GREEN[:3], 200), (size//2, size//2), size//2, 2)
        else:
            pygame.draw.circle(surf, (*COLORS.RED[:3], 150), (size//2, size//2), size//2)
            pygame.draw.circle(surf, (*COLORS.RED[:3], 200), (size//2, size//2), size//2, 2)

        return surf

    def _draw_panel(self, screen, rect, color=None, with_border=True, shadow=True):
        """Draw a modern rounded panel with optional shadow."""
        color = color or COLORS.UI_PANEL

        # Draw shadow
        if shadow:
            shadow_rect = rect.move(4, 4)
            shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 80),
                           (0, 0, shadow_rect.width, shadow_rect.height),
                           border_radius=self.panel_corner_radius)
            screen.blit(shadow_surf, shadow_rect)

        # Draw main panel with subtle gradient
        panel_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        # Draw gradient background
        for i in range(rect.height):
            alpha = int(color[3] * (0.9 + 0.1 * (i / rect.height)))
            line_color = (*color[:3], alpha)
            pygame.draw.line(panel_surf, line_color, (0, i), (rect.width, i))

        if with_border:
            # Draw subtle border gradient
            border_color = (*COLORS.BRAND_PRIMARY[:3], 80)
            pygame.draw.rect(panel_surf, border_color,
                           (0, 0, rect.width, rect.height),
                           2, border_radius=self.panel_corner_radius)

            # Draw inner highlight
            highlight_color = (*COLORS.BRAND_LIGHT[:3], 40)
            pygame.draw.rect(panel_surf, highlight_color,
                           (2, 2, rect.width-4, rect.height-4),
                           1, border_radius=self.panel_corner_radius-2)

        screen.blit(panel_surf, rect)
        return rect

    def _draw_header(self, screen):
        """Draw the main header with brand information."""
        header_height = 70
        header_rect = pygame.Rect(0, 0, DISPLAY.WIDTH, header_height)

        # Draw gradient header
        header_surf = pygame.Surface((DISPLAY.WIDTH, header_height), pygame.SRCALPHA)
        for i in range(header_height):
            # Gradient from dark to brand color
            r = int(COLORS.BRAND_PRIMARY[0] * (i / header_height))
            g = int(COLORS.BRAND_PRIMARY[1] * (i / header_height))
            b = int(COLORS.BRAND_PRIMARY[2] * (i / header_height))
            alpha = int(200 * (i / header_height))
            pygame.draw.line(header_surf, (r, g, b, alpha), (0, i), (DISPLAY.WIDTH, i))

        screen.blit(header_surf, header_rect)

        # Draw logo and group name
        logo_x = 25
        logo_y = (header_height - self.brand_logo.get_height()) // 2

        # Draw animated logo
        self.logo_animation = (self.logo_animation + 1) % 360
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.logo_animation).x)
        pulse_size = int(2 * pulse)

        # Logo background glow
        glow_radius = self.brand_logo.get_width()//2 + 4 + pulse_size
        glow_color = (*COLORS.BRAND_ACCENT[:3], 50)
        pygame.draw.circle(screen, glow_color,
                         (logo_x + self.brand_logo.get_width()//2,
                          logo_y + self.brand_logo.get_height()//2),
                         glow_radius)

        screen.blit(self.brand_logo, (logo_x, logo_y))

        # Group name
        group_x = logo_x + self.brand_logo.get_width() + 15
        group_y = logo_y + 5

        # Main group name
        group_text = f"{self.group_name}"
        group_surface = self.title_font.render(group_text, True, COLORS.TEXT_WHITE)
        screen.blit(group_surface, (group_x, group_y))

        # Description
        desc_text = self.description
        desc_surface = self.subtitle_font.render(desc_text, True, COLORS.BRAND_LIGHT)
        screen.blit(desc_surface, (group_x, group_y + 35))

        # Version and creator (right side)
        right_info = f"{self.version} • {self.creator_name}"
        right_surface = self.small_font.render(right_info, True, COLORS.TEXT_DIM)
        right_x = DISPLAY.WIDTH - right_surface.get_width() - 25
        right_y = header_height // 2 - right_surface.get_height() // 2
        screen.blit(right_surface, (right_x, right_y))

        # Draw separator line with glow effect
        sep_y = header_height
        for i in range(3):
            alpha = 100 - i * 30
            color = (*COLORS.BRAND_ACCENT[:3], alpha)
            pygame.draw.line(screen, color, (0, sep_y + i), (DISPLAY.WIDTH, sep_y + i), 1)

    def _draw_traffic_control_panel(self, screen):
        """Draw the main traffic control panel."""
        panel_width = 320
        panel_height = 400
        panel_x = 25
        panel_y = 90

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self._draw_panel(screen, panel_rect, COLORS.UI_PANEL_DARK)

        # Panel header with icon
        header_y = panel_y + 20
        pygame.draw.line(screen, COLORS.BRAND_PRIMARY,
                        (panel_x + 20, header_y + 25),
                        (panel_x + 70, header_y + 25), 3)

        header_text = "TRAFFIC CONTROL CENTER"
        header_surface = self.header_font.render(header_text, True, COLORS.TEXT_HIGHLIGHT)
        screen.blit(header_surface, (panel_x + 85, header_y))

        # System status section
        status_y = header_y + 50
        self._draw_system_status(screen, panel_x + 25, status_y)

        # Current phase section
        phase_y = status_y + 140
        self._draw_current_phase(screen, panel_x + 25, phase_y)

        # Statistics section
        stats_y = phase_y + 130
        self._draw_statistics(screen, panel_x + 25, stats_y)

    def _draw_system_status(self, screen, x, y):
        """Draw system status indicators."""
        # Status header
        status_header = "System Status"
        header_surface = self.subtitle_font.render(status_header, True, COLORS.BRAND_LIGHT)
        screen.blit(header_surface, (x, y))

        # AI Status
        ai_y = y + 35
        ai_status = "AI Mode"
        ai_value = "ACTIVE 🧠" if self.app.ai_mode else "TIMER ⏱️"
        ai_color = COLORS.TEXT_SUCCESS if self.app.ai_mode else COLORS.TEXT_WARNING
        self._draw_status_item(screen, x, ai_y, ai_status, ai_value, ai_color)

        # Emergency Status
        emergency_y = ai_y + 35
        if hasattr(self.app.system_manager, 'emergency_mode') and self.app.system_manager.emergency_mode:
            emergency_status = "Emergency Mode"
            emergency_value = "ACTIVE 🚨"
            self._draw_status_item(screen, x, emergency_y, emergency_status, emergency_value, COLORS.ACCENT_EMERGENCY)

            # Blinking effect for emergency
            current_time = time.time()
            if current_time - self.last_blink_time > 0.5:
                self.blink_state = not self.blink_state
                self.last_blink_time = current_time

            if self.blink_state:
                blink_rect = pygame.Rect(x - 5, emergency_y - 5, 280, 40)
                pygame.draw.rect(screen, (*COLORS.ACCENT_EMERGENCY[:3], 30),
                               blink_rect, border_radius=8)

        # Simulation State
        state_y = emergency_y + (35 if hasattr(self.app.system_manager, 'emergency_mode') and self.app.system_manager.emergency_mode else 0)
        state_status = "Simulation"
        state_value = self.app.state.value.upper()
        state_color = COLORS.TEXT_SUCCESS if self.app.state.name == "RUNNING" else COLORS.TEXT_WARNING
        self._draw_status_item(screen, x, state_y, state_status, state_value, state_color)

    def _draw_status_item(self, screen, x, y, label, value, color):
        """Draw a status label-value pair."""
        # Draw indicator
        screen.blit(self.indicator_on if "ACTIVE" in value or "RUNNING" in value else self.indicator_off,
                   (x, y + 5))

        # Draw label
        label_surface = self.body_font.render(label, True, COLORS.TEXT_DIM)
        screen.blit(label_surface, (x + 20, y))

        # Draw value
        value_surface = self.body_font.render(value, True, color)
        value_x = x + 180
        screen.blit(value_surface, (value_x, y))

        # Draw underline
        pygame.draw.line(screen, (*color[:3], 50), (x, y + 30), (x + 250, y + 30), 1)

    def _draw_current_phase(self, screen, x, y):
        """Draw current traffic phase information."""
        if not hasattr(self.app.system_manager, 'traffic_lights'):
            return

        lights = self.app.system_manager.traffic_lights
        phase = lights.current_phase
        timer = lights.phase_timer

        # Phase header
        phase_header = "Current Phase"
        header_surface = self.subtitle_font.render(phase_header, True, COLORS.BRAND_LIGHT)
        screen.blit(header_surface, (x, y))

        # Determine phase color and state
        if timer < 30:
            phase_color = COLORS.GREEN
            phase_state = "GREEN"
            time_left = 30 - timer
        elif timer < 33:
            phase_color = COLORS.YELLOW
            phase_state = "YELLOW"
            time_left = 33 - timer
        else:
            phase_color = COLORS.RED
            phase_state = "RED"
            time_left = 35 - timer

        # Phase visual indicator
        phase_y = y + 35
        self._draw_phase_visual(screen, x, phase_y, phase, phase_color, phase_state)

        # Time information
        time_y = phase_y + 80
        time_text = f"Time remaining: {time_left:.1f}s"
        time_surface = self.body_font.render(time_text, True, COLORS.TEXT_WHITE)
        screen.blit(time_surface, (x, time_y))

        next_text = f"Next change in: {self.app.system_manager.next_phase_change:.1f}s"
        next_surface = self.small_font.render(next_text, True, COLORS.TEXT_DIM)
        screen.blit(next_surface, (x, time_y + 25))

    def _draw_phase_visual(self, screen, x, y, phase, color, state):
        """Draw visual phase indicator."""
        indicator_size = 70
        indicator_rect = pygame.Rect(x, y, indicator_size, indicator_size)

        # Draw glowing background
        glow_surf = pygame.Surface((indicator_size + 20, indicator_size + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color[:3], 50),
                         (indicator_size//2 + 10, indicator_size//2 + 10),
                         indicator_size//2 + 8)
        screen.blit(glow_surf, (x - 10, y - 10))

        # Draw indicator background
        pygame.draw.rect(screen, (*color[:3], 30), indicator_rect, border_radius=15)
        pygame.draw.rect(screen, (*color[:3], 150), indicator_rect, 3, border_radius=15)

        # Draw direction arrows
        center_x = x + indicator_size // 2
        center_y = y + indicator_size // 2

        if phase == 'NS':
            # North arrow
            pygame.draw.polygon(screen, color,
                              [(center_x, center_y - 15),
                               (center_x - 10, center_y),
                               (center_x + 10, center_y)])
            # South arrow
            pygame.draw.polygon(screen, color,
                              [(center_x, center_y + 15),
                               (center_x - 10, center_y),
                               (center_x + 10, center_y)])
            # N/S labels
            n_surface = self.small_font.render("N", True, color)
            s_surface = self.small_font.render("S", True, color)
            screen.blit(n_surface, (center_x - 5, center_y - 25))
            screen.blit(s_surface, (center_x - 5, center_y + 10))
        else:  # EW
            # West arrow
            pygame.draw.polygon(screen, color,
                              [(center_x - 15, center_y),
                               (center_x, center_y - 10),
                               (center_x, center_y + 10)])
            # East arrow
            pygame.draw.polygon(screen, color,
                              [(center_x + 15, center_y),
                               (center_x, center_y - 10),
                               (center_x, center_y + 10)])
            # E/W labels
            w_surface = self.small_font.render("W", True, color)
            e_surface = self.small_font.render("E", True, color)
            screen.blit(w_surface, (center_x - 20, center_y - 7))
            screen.blit(e_surface, (center_x + 10, center_y - 7))

        # Draw state text
        state_x = x + indicator_size + 15
        state_y = y + 10
        state_surface = self.header_font.render(state, True, color)
        screen.blit(state_surface, (state_x, state_y))

        phase_text = f"{phase} Direction"
        phase_surface = self.body_font.render(phase_text, True, COLORS.TEXT_WHITE)
        screen.blit(phase_surface, (state_x, state_y + 35))

    def _draw_statistics(self, screen, x, y):
        """Draw traffic statistics."""
        if not hasattr(self.app.system_manager, 'vehicle_manager'):
            return

        stats = self.app.system_manager.vehicle_manager.get_statistics()

        # Statistics header
        stats_header = "Traffic Statistics"
        header_surface = self.subtitle_font.render(stats_header, True, COLORS.BRAND_LIGHT)
        screen.blit(header_surface, (x, y))

        # Statistics grid
        stats_y = y + 35
        stats_data = [
            ("Active Vehicles", f"{stats['current_count']}", COLORS.TEXT_WHITE),
            ("Vehicles Passed", f"{stats['total_passed']}", COLORS.TEXT_WHITE),
        ]

        if stats['total_passed'] > 0:
            stats_data.extend([
                ("Avg Wait Time", f"{stats['average_wait_time']:.1f}s", COLORS.TEXT_SUCCESS),
                ("Max Wait Time", f"{stats['max_wait_time']:.1f}s", COLORS.TEXT_WARNING),
            ])

        for i, (label, value, color) in enumerate(stats_data):
            row_y = stats_y + i * 30

            # Draw bullet point
            pygame.draw.circle(screen, color, (x + 8, row_y + 10), 4)

            # Draw label
            label_surface = self.small_font.render(label, True, COLORS.TEXT_DIM)
            screen.blit(label_surface, (x + 20, row_y))

            # Draw value
            value_surface = self.body_font.render(value, True, color)
            value_x = x + 200
            screen.blit(value_surface, (value_x, row_y))

    def _draw_ai_panel(self, screen):
        """Draw the AI decision panel."""
        if not self.app.ai_mode or not hasattr(self.app.system_manager, 'current_ai_decision'):
            return

        decision = self.app.system_manager.current_ai_decision

        panel_width = 350
        panel_height = 280
        panel_x = DISPLAY.WIDTH - panel_width - 25
        panel_y = 90

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self._draw_panel(screen, panel_rect)

        # Panel header with AI icon
        header_y = panel_y + 20
        # Draw AI brain icon
        brain_points = [
            (panel_x + 30, header_y + 10),
            (panel_x + 20, header_y + 25),
            (panel_x + 25, header_y + 40),
            (panel_x + 35, header_y + 30),
            (panel_x + 45, header_y + 40),
            (panel_x + 50, header_y + 25),
            (panel_x + 40, header_y + 10),
        ]
        pygame.draw.polygon(screen, COLORS.BRAND_ACCENT, brain_points)

        header_text = "AI DECISION MAKING"
        header_surface = self.header_font.render(header_text, True, COLORS.TEXT_HIGHLIGHT)
        screen.blit(header_surface, (panel_x + 70, header_y))

        # AI Recommendation
        rec_y = header_y + 50
        rec_color = COLORS.GREEN if decision['recommended_phase'] == 'NS' else COLORS.YELLOW
        rec_text = f"Recommendation: {decision['recommended_phase']}"
        rec_surface = self.subtitle_font.render(rec_text, True, rec_color)
        screen.blit(rec_surface, (panel_x + 25, rec_y))

        # Traffic Analysis
        analysis_y = rec_y + 40

        # Vehicle counts with visual bars
        ns_cars = decision.get('ns_cars', 0)
        ew_cars = decision.get('ew_cars', 0)
        max_cars = max(ns_cars, ew_cars, 1)

        # NS bar
        ns_bar_width = int(120 * (ns_cars / max_cars))
        ns_bar_rect = pygame.Rect(panel_x + 25, analysis_y, ns_bar_width, 15)
        pygame.draw.rect(screen, (*COLORS.GREEN[:3], 150), ns_bar_rect, border_radius=3)
        pygame.draw.rect(screen, COLORS.GREEN, ns_bar_rect, 1, border_radius=3)

        ns_text = f"NS: {ns_cars}"
        ns_surface = self.small_font.render(ns_text, True, COLORS.TEXT_WHITE)
        screen.blit(ns_surface, (panel_x + 25 + ns_bar_width + 10, analysis_y - 2))

        # EW bar
        ew_bar_y = analysis_y + 25
        ew_bar_width = int(120 * (ew_cars / max_cars))
        ew_bar_rect = pygame.Rect(panel_x + 25, ew_bar_y, ew_bar_width, 15)
        pygame.draw.rect(screen, (*COLORS.YELLOW[:3], 150), ew_bar_rect, border_radius=3)
        pygame.draw.rect(screen, COLORS.YELLOW, ew_bar_rect, 1, border_radius=3)

        ew_text = f"EW: {ew_cars}"
        ew_surface = self.small_font.render(ew_text, True, COLORS.TEXT_WHITE)
        screen.blit(ew_surface, (panel_x + 25 + ew_bar_width + 10, ew_bar_y - 2))

        # Priority scores
        score_y = ew_bar_y + 30
        ns_score = decision.get('ns_score', 0)
        ew_score = decision.get('ew_score', 0)

        score_text = f"Priority Scores:"
        score_header = self.small_font.render(score_text, True, COLORS.TEXT_DIM)
        screen.blit(score_header, (panel_x + 25, score_y))

        ns_score_text = f"NS: {ns_score:.1f}"
        ew_score_text = f"EW: {ew_score:.1f}"

        ns_score_surface = self.body_font.render(ns_score_text, True,
                                               COLORS.GREEN if ns_score > ew_score else COLORS.TEXT_DIM)
        ew_score_surface = self.body_font.render(ew_score_text, True,
                                               COLORS.YELLOW if ew_score > ns_score else COLORS.TEXT_DIM)

        screen.blit(ns_score_surface, (panel_x + 25, score_y + 20))
        screen.blit(ew_score_surface, (panel_x + 120, score_y + 20))

        # Decision reason
        reason_y = score_y + 50
        reason_header = "Analysis:"
        reason_header_surface = self.small_font.render(reason_header, True, COLORS.TEXT_DIM)
        screen.blit(reason_header_surface, (panel_x + 25, reason_y))

        reason = decision['reason']
        reason_color = COLORS.ACCENT_EMERGENCY if decision['has_emergency'] else COLORS.TEXT_WHITE

        # Split long reasons
        if len(reason) > 35:
            parts = []
            current = reason
            while len(current) > 35:
                split_pos = current[:35].rfind(' ')
                if split_pos == -1:
                    split_pos = 35
                parts.append(current[:split_pos])
                current = current[split_pos:].strip()
            parts.append(current)

            for i, part in enumerate(parts):
                reason_surface = self.small_font.render(part, True, reason_color)
                screen.blit(reason_surface, (panel_x + 25, reason_y + 20 + i * 18))
        else:
            reason_surface = self.body_font.render(reason, True, reason_color)
            screen.blit(reason_surface, (panel_x + 25, reason_y + 20))

        # Action indicator
        if decision['should_switch']:
            action_y = panel_rect.bottom - 45
            action_color = COLORS.ACCENT_EMERGENCY if decision['has_emergency'] else COLORS.TEXT_WARNING
            action_text = "⚠️ RECOMMENDS PHASE CHANGE" if not decision['has_emergency'] else "🚨 EMERGENCY OVERRIDE"
            action_surface = self.body_font.render(action_text, True, action_color)
            action_x = panel_x + (panel_width - action_surface.get_width()) // 2

            # Draw highlight background
            action_bg = pygame.Rect(action_x - 10, action_y - 5,
                                  action_surface.get_width() + 20, 30)
            pygame.draw.rect(screen, (*action_color[:3], 20), action_bg, border_radius=6)
            pygame.draw.rect(screen, (*action_color[:3], 100), action_bg, 2, border_radius=6)

            screen.blit(action_surface, (action_x, action_y))

    def _draw_controls_panel(self, screen):
        """Draw the controls information panel."""
        panel_width = 350
        panel_height = 200
        panel_x = DISPLAY.WIDTH - panel_width - 25
        panel_y = DISPLAY.HEIGHT - panel_height - 25

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self._draw_panel(screen, panel_rect)

        # Panel header
        header_y = panel_y + 20
        pygame.draw.line(screen, COLORS.BRAND_ACCENT,
                        (panel_x + 20, header_y + 15),
                        (panel_x + 50, header_y + 15), 3)

        header_text = "CONTROLS"
        header_surface = self.header_font.render(header_text, True, COLORS.TEXT_HIGHLIGHT)
        screen.blit(header_surface, (panel_x + 65, header_y))

        # Controls in two columns
        controls_left = [
            ("SPACE", "Pause/Resume"),
            ("R", "Reset Simulation"),
            ("E", "Emergency Mode"),
            ("A", "Toggle AI Mode"),
            ("1 / 2", "Force NS/EW"),
        ]

        controls_right = [
            ("3", "Cycle Phase"),
            ("4-7", "Spawn Rate"),
            ("F2", "Screenshot"),
            ("ESC", "Quit"),
        ]

        # Draw left column
        start_y = header_y + 40
        for i, (key, desc) in enumerate(controls_left):
            self._draw_control_item(screen, panel_x + 25, start_y + i * 28, key, desc)

        # Draw right column
        for i, (key, desc) in enumerate(controls_right):
            self._draw_control_item(screen, panel_x + 185, start_y + i * 28, key, desc)

    def _draw_control_item(self, screen, x, y, key, description):
        """Draw a control key-description pair."""
        # Draw key background
        key_width = 50
        key_rect = pygame.Rect(x, y, key_width, 24)
        pygame.draw.rect(screen, (*COLORS.BRAND_PRIMARY[:3], 40), key_rect, border_radius=4)
        pygame.draw.rect(screen, (*COLORS.BRAND_PRIMARY[:3], 120), key_rect, 1, border_radius=4)

        # Draw key text
        key_surface = self.small_font.render(key, True, COLORS.BRAND_LIGHT)
        key_text_x = x + (key_width - key_surface.get_width()) // 2
        screen.blit(key_surface, (key_text_x, y + 4))

        # Draw description
        desc_surface = self.body_font.render(description, True, COLORS.TEXT_WHITE)
        screen.blit(desc_surface, (x + key_width + 10, y + 2))

    def _draw_footer(self, screen):
        """Draw the footer with performance info."""
        footer_height = 35
        footer_rect = pygame.Rect(0, DISPLAY.HEIGHT - footer_height, DISPLAY.WIDTH, footer_height)

        # Draw footer gradient
        footer_surf = pygame.Surface((DISPLAY.WIDTH, footer_height), pygame.SRCALPHA)
        for i in range(footer_height):
            alpha = int(180 * (1 - i / footer_height))
            color = (*COLORS.UI_BACKGROUND[:3], alpha)
            pygame.draw.line(footer_surf, color, (0, i), (DISPLAY.WIDTH, i))
        screen.blit(footer_surf, footer_rect)

        # Performance info on left
        fps = self.app.clock.get_fps()
        fps_color = COLORS.TEXT_SUCCESS if fps > 50 else COLORS.TEXT_WARNING if fps > 30 else COLORS.ACCENT_EMERGENCY

        fps_text = f"FPS: {fps:.0f}"
        fps_surface = self.small_font.render(fps_text, True, fps_color)
        screen.blit(fps_surface, (25, DISPLAY.HEIGHT - 25))

        frame_text = f"Frame: {self.app.performance.frame_count}"
        frame_surface = self.small_font.render(frame_text, True, COLORS.TEXT_DIM)
        screen.blit(frame_surface, (120, DISPLAY.HEIGHT - 25))

        # Time info on right
        time_text = f"Simulation Time: {self.app.elapsed_time:.1f}s"
        time_surface = self.small_font.render(time_text, True, COLORS.TEXT_DIM)
        screen.blit(time_surface, (DISPLAY.WIDTH - time_surface.get_width() - 25, DISPLAY.HEIGHT - 25))

        # Draw separator line
        sep_y = DISPLAY.HEIGHT - footer_height
        pygame.draw.line(screen, (*COLORS.BRAND_PRIMARY[:3], 100),
                        (0, sep_y), (DISPLAY.WIDTH, sep_y), 1)

    def _draw_pause_overlay(self, screen):
        """Draw pause overlay when simulation is paused."""
        if self.app.state.name == "PAUSED":
            # Create semi-transparent overlay
            overlay = pygame.Surface((DISPLAY.WIDTH, DISPLAY.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            # Draw pause panel
            pause_width = 400
            pause_height = 180
            pause_x = DISPLAY.WIDTH // 2 - pause_width // 2
            pause_y = DISPLAY.HEIGHT // 2 - pause_height // 2

            pause_rect = pygame.Rect(pause_x, pause_y, pause_width, pause_height)
            self._draw_panel(screen, pause_rect, (*COLORS.UI_PANEL_DARK[:3], 250), shadow=True)

            # Draw pause icon
            icon_center_x = pause_x + pause_width // 2
            icon_y = pause_y + 50

            # Draw two vertical bars for pause icon
            pygame.draw.rect(screen, COLORS.BRAND_ACCENT,
                           (icon_center_x - 30, icon_y - 25, 15, 50), border_radius=4)
            pygame.draw.rect(screen, COLORS.BRAND_ACCENT,
                           (icon_center_x + 15, icon_y - 25, 15, 50), border_radius=4)

            # Draw pause text
            pause_text = "SIMULATION PAUSED"
            pause_surface = self.header_font.render(pause_text, True, COLORS.TEXT_HIGHLIGHT)
            screen.blit(pause_surface, (icon_center_x - pause_surface.get_width()//2, icon_y + 40))

            # Draw continue instruction
            continue_text = "Press SPACE to continue"
            continue_surface = self.body_font.render(continue_text, True, COLORS.TEXT_DIM)
            screen.blit(continue_surface, (icon_center_x - continue_surface.get_width()//2, icon_y + 80))

    def render(self, screen: pygame.Surface) -> None:
        """Render all UI elements with polished design."""
        # Draw background pattern
        screen.blit(self.bg_pattern, (0, 0))

        # Draw all UI components
        self._draw_header(screen)
        self._draw_traffic_control_panel(screen)
        self._draw_ai_panel(screen)
        self._draw_controls_panel(screen)
        self._draw_footer(screen)

        # Draw pause overlay if needed
        self._draw_pause_overlay(screen)
