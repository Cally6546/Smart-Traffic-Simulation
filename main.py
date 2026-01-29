"""
Entry point for the Smart Traffic Simulation.
"""

from core.application import get_app

if __name__ == "__main__":
    app = get_app()
    app.run()
