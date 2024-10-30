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

image_start = Image.open("abstract.jpg")
data_start = image_start.load()

image_out = Image.new("RGB", (image_start.width, image_start.height))
data_out = image_out.load()

min_dimension = min(image_out.width, image_out.height)

for y in range(image_out.height):
    for x in range(image_out.width):
        pixel = data_start[x,y]
        
        xc = x - image_out.width/2
        yc = y - image_out.height/2
        
        radius = math.sqrt(xc**2+yc**2)
        theta = math.atan2(yc, xc)
        
        new_radius = (radius/(min_dimension/2))**3
        if(radius > min_dimension/2):
            new_radius = radius/(min_dimension/2)
        
        new_x = math.cos(theta)*new_radius*min_dimension/2
        new_y = math.sin(theta)*new_radius*min_dimension/2
        
        new_x += image_out.width/2
        new_y += image_out.height/2
        
        if new_x < 0 or new_x >= image_out.width-1 or new_y < 0 or new_y >= image_out.height-1:
            data_out[x,y] = (0,0,0)
        else:
            data_out[x,y] = bilinear_interpolation(data_start, new_x, new_y)
            #data_start[math.floor(new_x), math.floor(new_y)]
        
        
        
image_out.save("out_bulge.png")
