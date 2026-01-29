"""
Performance metrics tracking for optimization.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class PerformanceMetrics:
    """Track performance metrics for optimization."""
    frame_count: int = 0
    avg_fps: float = 0.0
    frame_times: List[float] = field(default_factory=list)
    max_frame_time: float = 0.0

    def update(self, frame_time: float) -> None:
        """Update metrics with new frame time."""
        self.frame_count += 1
        self.frame_times.append(frame_time)

        # Keep only last 60 frames (1 second at 60 FPS)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)

        self.avg_fps = 1000.0 / (sum(self.frame_times) / len(self.frame_times)) if self.frame_times else 0
        self.max_frame_time = max(self.max_frame_time, frame_time)
