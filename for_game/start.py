import pygame
from for_game.game import start_the_game


def start_starting_window():

    pygame.init()


    w = 800
    h = 600
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Игра")

    # Выгрузка картинки старта
    start_button_img = pygame.image.load("data/picture/start_button.png")

    # Выгрузка рекорда
    with open("data/info/record.txt", "r") as file:
        record_value = int(file.read())

    # Текст
    font = pygame.font.Font(None, 36)
    text = font.render("Рекорд: " + str(record_value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(w / 2, 50))

    class Button(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    buttons = pygame.sprite.Group()
    start_button = Button(
        start_button_img, w / 2 - start_button_img.get_width() / 2, 300
    )
    buttons.add(start_button)

    run = True
    while run:
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                run = False
            if el.type == pygame.KEYDOWN:
                if el.key == pygame.K_ESCAPE:
                    return False
            if el.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(el.pos):
                    return start_the_game()
        screen.fill(pygame.Color(240, 128, 128))
        screen.blit(text, text_rect)
        buttons.draw(screen)
        pygame.display.flip()
    pygame.quit()
