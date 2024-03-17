import pygame
from cars import Cars
from buttons import Button
from traffic_lights import PedestrianLights, TrafficLights


BG_IMAGE = "images/double_intersection.png"
PAUSE_IMAGE = "images/buttons/pause_btn.png"
ON_OFF_RED = "images/buttons/on_off_red.png"
ON_OFF_GRN = "images/buttons/on_off_grn.png"
PAUSE_TEXT = "Simulation Paused"
FONT = "Consolas"
CARS_STARTING_POSITIONS = {"1": (1200, 900), "2": (1750, 380), "3": (560, -40), "4": (-40, 460)}
CAR_LIGHTS_INFO = [[640, 410, 2], [470, 430, 4], [535, 310, 3, 11000, 3000, 34000]]
PEDESTRIAN_INFO = [[610, 300, 1], [620, 540, 3], [495, 300, 1], [495, 540, 3],
				   [640, 335, 4], [470, 340, 2], [640, 505, 4], [470, 505, 2]]


def create_traffic_lights(add_x=0):
	PedestrianLights.preload_images()
	TrafficLights.preload_images()
	tr_car = TrafficLights(CAR_LIGHTS_INFO[0][0]+add_x, CAR_LIGHTS_INFO[0][1], CAR_LIGHTS_INFO[0][2])
	tr_car.sync.append(TrafficLights(CAR_LIGHTS_INFO[1][0]+add_x, CAR_LIGHTS_INFO[1][1], CAR_LIGHTS_INFO[1][2]))
	if add_x:
		tr_car.secondary.append(TrafficLights(1240, 520, 1,
							 CAR_LIGHTS_INFO[2][3], CAR_LIGHTS_INFO[2][4], CAR_LIGHTS_INFO[2][5]))
	else:
		tr_car.secondary.append(
			TrafficLights(CAR_LIGHTS_INFO[2][0] + add_x, CAR_LIGHTS_INFO[2][1], CAR_LIGHTS_INFO[2][2],
						  CAR_LIGHTS_INFO[2][3], CAR_LIGHTS_INFO[2][4], CAR_LIGHTS_INFO[2][5]))
	for x in range(8):
		if x == 0 or x == 1:
			tr_car.ped.append(PedestrianLights(PEDESTRIAN_INFO[x][0]+add_x, PEDESTRIAN_INFO[x][1], PEDESTRIAN_INFO[x][2]))
		elif x == 2 or x == 3:
			tr_car.sync[0].ped.append(PedestrianLights(PEDESTRIAN_INFO[x][0]+add_x, PEDESTRIAN_INFO[x][1],
														PEDESTRIAN_INFO[x][2]))
		else:
			tr_car.secondary[0].ped.append(PedestrianLights(PEDESTRIAN_INFO[x][0]+add_x, PEDESTRIAN_INFO[x][1],
															 PEDESTRIAN_INFO[x][2]))
	return tr_car


Cars.starting_positions = CARS_STARTING_POSITIONS
Cars.groups_directions = {x: pygame.sprite.Group() for x in CARS_STARTING_POSITIONS.keys()}
pygame.init()
bg = pygame.image.load(BG_IMAGE)
screen_size = bg.get_size()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Traffic Simulation")
pause_text = pygame.font.SysFont(FONT, 32).render(PAUSE_TEXT, True, pygame.color.Color('White'))
pause_btn = Button(800, 50, PAUSE_IMAGE)
on_off_btn = Button(875, 50, ON_OFF_RED)
clock = pygame.time.Clock()
lights = create_traffic_lights()
lights.next = create_traffic_lights(650)

run_sim = True
paused = False
while run_sim:
	clock.tick(60)
	if not paused:
		screen.blit(bg, (0, 0))
		Cars.create_cars()
		Cars.cars_group.draw(screen)
		Cars.cars_group.update()
		pause_btn.draw(screen)
		on_off_btn.draw(screen)
		for i in TrafficLights.traffic_lights_list:
			i.draw(screen)
	else:
		screen.blit(pause_text, (int(screen_size[0]/2), int(screen_size[1]/2)))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pause_btn.is_over(event.pos):
			if paused:
				paused = False
			else:
				paused = True
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and on_off_btn.is_over(event.pos):
			if on_off_btn.image_name == ON_OFF_RED:
				lights.turn_on()
				on_off_btn.image = pygame.image.load(ON_OFF_GRN)
				on_off_btn.image_name = ON_OFF_GRN
				on_off_btn.draw(screen)
			else:
				lights.turn_off()
				on_off_btn.image = pygame.image.load(ON_OFF_RED)
				on_off_btn.image_name = ON_OFF_RED
				on_off_btn.draw(screen)
		if event.type == pygame.QUIT:
			run_sim = False


pygame.quit()
