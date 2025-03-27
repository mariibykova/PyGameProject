import pygame


def start_final_window(given_score):
    given_score = str(given_score)

    pygame.init()


    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Игра")

    # Выгрузка картинки завершения
    new_game_button_img = pygame.image.load("data/picture/new_game_button.png")

    # Выгрузка рекорда
    with open("data/info/record.txt", "r") as file:
        record_value = int(file.read())

    font = pygame.font.Font(None, 36)
    text = font.render("Рекорд: " + str(record_value), True, (0, 0, 0))
    your_score_text = font.render("Ваш счёт: " + given_score, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width / 2, 50))
    your_score_text_rect = your_score_text.get_rect(center=(screen_width / 2, 100))

    class Button(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    buttons = pygame.sprite.Group()
    new_game_button = Button(
        new_game_button_img, screen_width / 2 - new_game_button_img.get_width() / 2, 300
    )
    buttons.add(new_game_button)

    
    run = True
    while run:
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                run = False
            if el.type == pygame.KEYDOWN:
                if el.key == pygame.K_ESCAPE:
                    pygame.quit()
            if el.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.rect.collidepoint(el.pos):
                    return True

        screen.fill(pygame.Color(186, 229, 240))
        screen.blit(text, text_rect)
        screen.blit(your_score_text, your_score_text_rect)
        buttons.draw(screen)

        pygame.display.flip()

    pygame.quit()
