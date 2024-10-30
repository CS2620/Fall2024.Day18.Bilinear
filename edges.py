from PIL import Image
import math

image = Image.open("abstract.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width*2, image.height*2))
new_data = new_image.load()

algorithm = "SOLID"
# algorithm = "BLEED"
# algorithm = "MIRROR"
# algorithm = "TILE"

for y in range(new_image.height):
    for x in range(new_image.width):
        
        new_x = x - image.width/2
        new_y = y - image.height/2
        new_x //=1
        new_y //=1
        
        if new_x < 0 or new_x >= image.width or new_y < 0 or new_y >= image.height:
            if algorithm == "SOLID":
                new_data[x,y] = (255,255,255)
            elif algorithm == "BLEED":
                if new_x < 0:
                    new_x = 0
                if new_y < 0:
                    new_y = 0
                if new_x >=image.width:
                    new_x = image.width-1
                if new_y >= image.height:
                    new_y = image.height-1
                new_data[x,y] = data[new_x, new_y]
            elif algorithm == "MIRROR":
                if new_x < 0:
                    new_x = abs(new_x)
                if new_y < 0:
                    new_y = abs(new_y)
                if new_x >= image.width:
                    new_x = image.width-new_x-1
                if new_y >= image.height:
                    new_y = image.height-new_y-1
                new_data[x,y] = data[new_x, new_y]
            elif algorithm == "TILE":
                if new_x < 0:
                    new_x = image.width-1+new_x
                if new_y < 0:
                    new_y = image.height-1+new_y
                if new_x >= image.width:
                    new_x = new_x-image.width
                if new_y >= image.height:
                    new_y = new_y - image.height
                new_data[x,y] = data[new_x, new_y]
            else:
                new_data[x,y] = (255, 0, 255)
        else:
            new_data[x,y] = data[new_x, new_y]
        

new_image.save("out_edges_" + algorithm + ".png")
