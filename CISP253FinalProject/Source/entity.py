from sprites import sprite, animation
from pygame import Rect, Surface
from abc import abstractmethod
from math import sqrt

#This is an abstract class dedicated to making entities and having them function properly.
class entity:
    #This constructor requires the animation associated with the entity (even if there is only 1 sprite in it).
    #The x and y are optional to set, but can determine where you'd like the entity to appear on the screen.
    def __init__(self, animation: animation, x: float = 0.0, y: float = 0.0) -> None:
        self.animation = animation
        self.x = x
        self.y = y
        self.layer = 0
        self.bottom = animation.current.image.get_rect().bottom
        #Set the width and height of the entity to the width and height of the animation's current image.
        self.width = animation.current.get_width()
        self.height = animation.current.get_height()
        #Set for entities which need to move in a certain direction.
        self.direction = 90.0
        #Set for entities which need to rotate their image.
        self.image_direction = 90

    #An abstract method for any object inheriting entity.
    #This method is used and will always run 60 times per second.
    @abstractmethod
    def update(self) -> None:
        pass
    #An abstract method for any object inheriting entity.
    #This method is used and will run as many times as the computer will allow it to.
    @abstractmethod
    def render(self, screen: Surface) -> None:
        pass

    #Retrieves how far away in pixels the current entity is from the provided coordinates.
    #If "center" is true (default is True), the distance will be calculated by the entity's center rather than top-left.
    def distance_from(self, x: float, y: float, center: bool = True) -> float:
        return sqrt((x - self.x) ** 2 + (y - self.y) ** 2) if not center else sqrt((x - (self.x - self.width / 2)) ** 2 + (y - (self.y - self.width / 2)) ** 2)

    #Retrieves how far away in pixels the current entity is from the provided entity.
    #If "center" is true (default is True), the distance will be calculated by the entities' centers rather than top-left.
    def distance_from_entity(self, entity: 'entity', center: bool = True) -> float:
        return self.distance_from(entity.x, entity.y, center) if not center else self.distance_from(entity.x - entity.width / 2, entity.y - entity.height / 2)

    #Checks if the provided x, y, width, and height intersect with this entity's.
    def intersects_with(self, x: float, y: float, width: int, height: int) -> bool:
        return self.x > x - self.width and self.x < x + width and self.y > y - self.height and self.y < y + height

    #Checks if the entity provided intersects with this entity.
    def intersects_with_entity(self, entity: 'entity') -> bool:
        return self.intersects_with(entity.x, entity.y, entity.width, entity.height)

    #Get the current sprite's animation frame.
    def get_sprite(self) -> sprite:
        return self.animation.current

    #Get the Rect data of the entity for rendering.
    def get_data(self) -> Rect:
        #Retrieve the rect from the current animation's image.
        rect = self.animation.current.image.get_rect()
        rect.bottom = self.bottom

        #Parse the x and y of the entity into an integer to pass into the rect.
        rect.x += int(self.x)
        rect.y += int(self.y)

        return rect

#I'm not sure how collections are handled within Python, so I made my own.
class entity_collection:
    #Typical setup for a class.
    def __init__(self) -> None:
        self.entities = []

    #Adds an entity to the list.
    def add(self, entity: entity) -> None:
        self.entities.append(entity)
        self.sort()

    #Add a list of entities to the current list.
    def add_range(self, entities: list) -> None:
        for entity in entities:
            self.entities.append(entity)

        self.sort()

    #Checks if the list contains the entity.
    def contains(self, entity: entity) -> bool:
        return self.entities.__contains__(entity)

    #Removes an entity from the list and returns True if it was successful; otherwise, it returns False.
    def remove(self, entity: entity) -> bool:
        result = self.contains(entity)

        self.entities.remove(entity)

        return result

    #Removes an entity at the location found at the index.
    def remove_at(self, index: int) -> None:
        self.entities.remove(self.get(index))

    #Retrieves the entity found at the index provided.
    def get(self, index: int) -> entity:
        return self.entities[index]

    #Gets the index of the entity provided. Returns -1 if none was found.
    def index_of(self, entity: entity) -> int:
        for i in range(len(self.entities)):
            if self.entities[i] == entity:
                return i

        return -1

    #Retrieves the size of the entity list.
    def size(self) -> int:
        return len(self.entities)

    def sort(self) -> None:
        self.entities.sort(key = lambda x: x.layer, reverse = False)

    #Updates all the entities.
    def update(self) -> None:
        for entity in self.entities:
            entity.update()

    #Renders all the entities.
    def render(self, screen: Surface) -> None:
        for entity in self.entities:
            entity.render(screen)