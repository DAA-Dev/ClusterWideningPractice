import logging
from PIL import Image

logging.getLogger('PIL').setLevel(logging.WARNING)

# These two store directions as well as their relevant offsets from the current position
move_directions = {'R':(1,0), 'L':(-1,0), 'B':(0,1), 'T':(0,-1)}
check_order = {'R': ('B', 'L', 'T'), 'L': ('T', 'R', 'B'), 'B': ('L', 'R', 'T'), 'T': ('R', 'L', 'B')}

def cluster_widen(save_path):
    # Load the image into memory
    image = Image.open(save_path)
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()

    # Method to check if a pixel is black
    def black(pix):
        if (pix[0] == 0 and pix[1] == 0 and pix[2] == 0):
            return True
        return False 

    # Method to check if a pixel is red
    def red(pix):
        if not(pix[0] == 255 and pix[1] == 0 and pix[2] == 0):
            return False
        return True
   
    # Method to paint a pixel red, blue, or green
    def paint_pixel(location, color):
        x, y = location
        pixels[x, y] = (255 if color == 'red' else 0, 
                        255 if color == 'green' else 0,
                        255 if color == 'blue' else 0,
                        255)
        
    # Recursive method in order to paint out the edge of a pixel cluster
    def paint_border(initial_location, is_first):
        if is_first:
            initial_location = (initial_location[0]-1, initial_location[1])
            paint_pixel(initial_location, 'red')
        
        obstructed = 0
        first_blk_key = None
        for i, look in enumerate(move_directions.values()):
            look_dir = (initial_location[0]+look[0], initial_location[1]+look[1])

            if not black(pixels[look_dir[0], look_dir[1]]):
                obstructed += 1
                if first_blk_key is None:
                    first_blk_key = list(move_directions.keys())[i]
        
        trapped = False
        if obstructed != 4:
            scan_dirs = check_order[first_blk_key]
            for direction in scan_dirs:
                hot_pixel = (initial_location[0]+move_directions[direction][0], initial_location[1]+move_directions[direction][1])
                if black(pixels[hot_pixel[0], hot_pixel[1]]):
                    paint_pixel(hot_pixel, 'blue')
                    trapped = paint_border(hot_pixel, False)
                    if not trapped:
                        return False
                if direction == 'B' and red(pixels[hot_pixel[0], hot_pixel[1]]):
                    return trapped
            return trapped
        else:
            return True

    # Scan from left to right
    # Modify this code in order to work with multiple clusters 
    current_location = [0, 0]
    found_start = False
    for y in range(0, height):
        if not found_start:
            for x in range (0, width):
                pixel = pixels[x, y]
                if not black(pixel) and not found_start:
                    paint_border((x, y), True)
                    found_start = True
                    break
            

    # Save the modified image
    image.save('res{}'.format(save_path), 'PNG')
    image.show()

test_num = 3
cluster_widen('Test{}.png'.format(test_num))