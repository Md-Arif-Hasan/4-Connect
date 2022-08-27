import pygame
import button
import GAME

#create display window
SCREEN_HEIGHT = 420
SCREEN_WIDTH = 420

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen1 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Connect-4')

#load button images
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

#create button instances
menu_button = button.Button(100, 150, start_img, 0.8)
#exit_button = button.Button(100, 150, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if menu_button.draw(screen):
		GAME.main()
		menu_button = button.Button(100, 150, exit_img, 0.8)
	if menu_button.draw(screen):
		pygame.quit()
		print('EXIT')

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

#pygame.quit()