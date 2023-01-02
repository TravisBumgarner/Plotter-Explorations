from PIL import Image, ImageDraw
import colorsys
import numpy as np
import time

################
### Settings ###
################
#max_photo_width = 100 #These settings resize the image to a max of whatever the values are here
#max_photo_height = 100 # This makes it easier to convert

spacing_per_dot = 10 #How many pixels space between each dot

#How many pixels should a dot take up
xtra_large_dot = 6
large_dot      = 3
medium_dot     = 1.5
small_dot      = 0.75
xtra_small_dot = 0

#What are the cutoffs for the brightness of a dot.
black_luminosity = 50
shadow_luminosity = 90
medium_luminosity = 130
highlight_luminosity = 170
white_luminosity = 220

def convert_photo(imported_photo):
    start = time.time()

    #raw_photo = Image.open(input("Specify photo path: "))
    #raw_photo = Image.open("C:\\Users\\travis.bumgarner\\Downloads\\cat.jpg")
    raw_photo = Image.open("test_img\\" + imported_photo)   
    raw_photo_width, raw_photo_height = raw_photo.size
    #resize image if too large
    ##if raw_photo_width > max_photo_width or raw_photo_height > max_photo_height:
    ##    scale_width = raw_photo_width / max_photo_width  
    ##    scale_height = raw_photo_height / max_photo_height
    ##    scale = max(scale_width,scale_height)
    ##    print(scale)
    ##    raw_photo_width = int(raw_photo_width / scale)
    ##    raw_photo_height = int(raw_photo_height / scale)

    #_arduino is the photo in matrix form that gets sent through serial to the arduino
    processed_photo_arduino = np.zeros(raw_photo.size)

    #_computer is the preview file that gets saved to the computer
    processed_photo_computer = Image.new("HSV",(raw_photo_width,raw_photo_height))

    #_print_preview is the preview of what the final printout might look like with dots
    processed_photo_print_preview = Image.new("RGB",(raw_photo_width * spacing_per_dot , raw_photo_height * spacing_per_dot),"white")
    print_preview_draw = ImageDraw.Draw(processed_photo_print_preview)

    #For each pixel in the image, go through and get the R,G,B values. Convert that to HLS, crop the luminosity, save it
    for x in range(raw_photo_width):
        for y in range(raw_photo_height):
            current_px = raw_photo.getpixel((x,y))

            r_px = current_px[0]
            g_px = current_px[1]
            b_px = current_px[2]
            #print(str(r_px) + "," + str(g_px) + "," + str(b_px))
            try:
                hls = colorsys.rgb_to_hls(r_px,g_px,b_px)
                #luminosity ranges from 255 black to 0 white
            except ZeroDivisionError:
                hls = (0,0,0)
            luminosity_px = lum_modifier(hls[1])
            

            processed_photo_arduino[x][y] = int(luminosity_px)
            processed_photo_computer.putpixel((x,y),(0,0,int(luminosity_px)))
            #Draw an elipse (left,top,right,bottom)
            pixel_size = pixel_size_print_preview(int(luminosity_px))
            if pixel_size > 0:
                print_preview_draw.ellipse((x * spacing_per_dot - pixel_size,
                                            y * spacing_per_dot - pixel_size,
                                            x * spacing_per_dot + pixel_size,
                                            y * spacing_per_dot + pixel_size),"black")

    #Save image
    dots_and_lums = (imported_photo + "Spacing-" + str(spacing_per_dot)
                     + "  Dots-" + str(xtra_large_dot) + " "
                                              + str(large_dot) + " "
                                              + str(medium_dot) + " "
                                              + str(small_dot) + " "
                                              + str(xtra_small_dot)
                                       +"   Lum-"
                                               + str(black_luminosity) + " "
                                               + str(shadow_luminosity) + " "
                                               + str(medium_luminosity) + " "
                                               + str(highlight_luminosity) + " "
                                               + str(white_luminosity)+".jpg")
   #processed_photo_computer.convert('RGB').save("pc" + dots_and_lums)
    #processed_photo_print_preview.save("cat3.jpg")
    processed_photo_print_preview.save("pp" + dots_and_lums)
    #Processing run time
    done = time.time()
    elapsed = done - start
    print(str(elapsed) + " seconds to process image.")

#Below are a list of functions to convert an image to different formats for printing
def lum_modifier(luminosity_px):
    if luminosity_px > 200:
        return 255
    elif luminosity_px > 150:
        return 170
    elif luminosity_px > 100:
        return 110
    elif luminosity_px > 50:
        return 60
    else:
        return 0

def pixel_size_print_preview(luminosity_px):
    if luminosity_px > white_luminosity:
        return xtra_small_dot
    elif luminosity_px > highlight_luminosity:
        return small_dot
    elif luminosity_px > medium_luminosity:
        return medium_dot
    elif luminosity_px > shadow_luminosity :
        return large_dot
    else:
        return xtra_large_dot
    
#testing
for i in range(4):
    convert_photo(str(i)+".jpg")
