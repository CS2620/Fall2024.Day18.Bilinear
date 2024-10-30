from PIL import Image
import math

def nn_interpolation(data, x, y):
    return data[math.floor(x), math.floor(y)]

def interpolate(start, end, percent):
    return (end-start)*percent+start
    
def interpolateRGB(start, end, percent):
    r_start = start[0]
    g_start = start[1]
    b_start = start[2]
    
    r_end = end[0]
    g_end = end[1]
    b_end = end[2]
    
    r = interpolate(r_start, r_end, percent)
    g = interpolate(g_start, g_end, percent)
    b = interpolate(b_start, b_end, percent)
    
    return (r,g,b)

def bilinear_interpolation(data, x, y):
    # Gather my pixels
    x_start = math.floor(x)
    x_end = x_start + 1
    x_percent = x - x_start
    
    y_start = math.floor(y)
    y_end = y_start + 1
    y_percent = y - y_start
    
    
    top_left = data[int(x_start), int(y_start)]
    top_right = data[int(x_end), int(y_start)]
    bottom_left = data[int(x_start), int(y_end)]
    bottom_right = data[int(x_end), int(y_end)]
    
    
    #Interpolate across the top
    top = interpolateRGB(top_left, top_right, x_percent)
    
    #Interpolate across the bottom
    bottom = interpolateRGB(bottom_left, bottom_right, x_percent)
    
    #Interpolate vertically
    result = interpolateRGB(top, bottom, y_percent)
    
    #return the result
    return (math.floor(result[0]),math.floor(result[1]),math.floor(result[2]))


image = Image.open("abstract.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

rotation = .5
center = (image.width/2,image.height/2)

cosine_theta = math.cos(-rotation)
sine_theta = math.sin(-rotation)

dx = - cosine_theta * image.width/2 + sine_theta*image.height/2+image.width/2
dy = - sine_theta * image.width/2- cosine_theta * image.height/2+image.height/2

# dx = 0
# dy = 0

for y in range(image.height):
    for x in range(image.width):
        
        new_x = cosine_theta * x - sine_theta * y + dx
        new_y = sine_theta * x + cosine_theta * y + dy
        
        # new_x //= 1
        # new_y //= 1
        
        if new_x < 0 or new_x >= image.width-1 or new_y < 0 or new_y >= image.height-1:
            new_data[x,y] = (0,0,0)
        else:
            new_data[x,y] = bilinear_interpolation(data, new_x, new_y)
            #data_start[math.floor(new_x), math.floor(new_y)]
        

new_image.save("out_rotation_bilinear.png")
