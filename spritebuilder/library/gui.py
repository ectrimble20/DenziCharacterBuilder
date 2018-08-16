from pygame.sprite import Sprite


class Button(Sprite):

    def __init__(self, action, surface, center):
        super().__init__()
        self.action = action
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = center
