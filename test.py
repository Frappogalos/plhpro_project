from PIL import Image
import pygame

# Resize image
# img = Image.open("images/traffic_lights/car_red.png")
# print(img.size)
# resized_img = img.resize((int(img.width/2), int(img.height/2)))
# resized_img.save("images/traffic_lights/car_red2.png", "PNG")

# Rotate Image
# img = Image.open("images/traffic_lights/pedestrian_green.png")
# img = img.rotate(270, expand=True)
# img.save("images/traffic_lights/pedestrian_lights_green1.png")


directions = [1, 2, 3, 4]
images_dict = {"off": "images/traffic_lights/pedestrian_off.png",
			   "red": "images/traffic_lights/pedestrian_red.png",
			   "green": "images/traffic_lights/pedestrian_green.png"}
images = {}


def preload_images():
	temp = {}
	for x in directions:
		for i in images_dict.keys():
			temp[i] = pygame.transform.rotate(pygame.image.load(images_dict[i]), 90 * x)
		images[x] = temp

	print(images)


preload_images()
