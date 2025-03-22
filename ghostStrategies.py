from abc import ABC, abstractmethod

class ChaseStrategy(ABC):
    @abstractmethod
    def update_destination(self, ghost):
        """Оновлює ціль привида залежно від його стратегії переслідування."""
        pass

class BlinkyChaseStrategy(ChaseStrategy):
    def update_destination(self, ghost):
        ghost.destination = ghost.pacman.position

class PinkyChaseStrategy(ChaseStrategy):
    def update_destination(self, ghost):
        pacman_dir = ghost.pacman.direction
        ghost.destination = (
            ghost.pacman.position[0] + pacman_dir[0] * 4,
            ghost.pacman.position[1] + pacman_dir[1] * 4
        )

class InkyChaseStrategy(ChaseStrategy):
    def update_destination(self, ghost):
        blinky = next(g for g in ghost.game.ghosts if g.name == "Blinky")
        pacman_dir = ghost.pacman.direction
        intermediate = (
            ghost.pacman.position[0] + pacman_dir[0] * 2,
            ghost.pacman.position[1] + pacman_dir[1] * 2
        )
        ghost.destination = (
            intermediate[0] + (intermediate[0] - blinky.position[0]),
            intermediate[1] + (intermediate[1] - blinky.position[1])
        )

class ClydeChaseStrategy(ChaseStrategy):
    def update_destination(self, ghost):
        distance = ((ghost.position[0] - ghost.pacman.position[0]) ** 2 + 
                    (ghost.position[1] - ghost.pacman.position[1]) ** 2) ** 0.5
        if distance > 8:
            ghost.destination = ghost.pacman.position
        else:
            ghost.destination = ghost.scatter_point