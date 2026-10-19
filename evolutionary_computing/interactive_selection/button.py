import pygame


class Button:
    def __init__(self, text, x, y, width, height, color=(200, 200, 200)):
        self.text = text
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.color = pygame.Color(color)

    def draw(self, screen):
        my_font = pygame.font.SysFont("Arial", 20)
        if self.check_clicked():
            pygame.draw.rect(screen,pygame.Color(100,100,100) , self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen,self.color, self.rect, border_radius=8)
        text_surf = my_font.render(self.text, True, "black")
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos) and clicked:
            return True
        return False