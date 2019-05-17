import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

OldMax = 280
OldMin = 40
NewMax = 100
NewMin = 0
OldRange = (OldMax - OldMin)
min_y = 120
max_y = 240
left_red = 40
left_yellow = 90
right_yellow = 230
right_red = 280

height = 240
width = 320

def region_of_interest(img, vertices):
    # Define a blank matrix that matches the image height/width.
    mask = np.zeros_like(img)
    # Create a match color with the same color channel counts.
    match_mask_color = (255,) #* channel_count
      
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

    
def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    # If there are no lines to draw, exit.
    if lines is None:
        return
    # Make a copy of the original image.
    img = np.copy(img)
    # Create a blank image that matches the original in size.
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8,
    )
    # Loop over all lines and draw them on the blank image.
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    # Merge the image with the lines onto the original.
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    # Return the modified image.
    return img    
    

def scale_value(OldValue):
	if (OldRange == 0):
		NewValue = NewMin
	else:
		NewRange = (NewMax-NewMin)
		NewValue = (((OldValue-OldMin) * NewRange) / OldRange) + NewMin
	return NewValue
	
region_of_interest_vertices = [
    (0, height),
    (0, height / 2),
    (width, height /2),
    (width, height),
]
 

def Houghdat(img):
	grey_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	
	cannyed_image = cv2.Canny(grey_image, 100, 200)
	
	cropped_image = region_of_interest(
        cannyed_image,
        np.array([region_of_interest_vertices], np.int32),
        )
    
	lines = cv2.HoughLinesP(cannyed_image, 
	    rho=10, #originally 6 
	    theta=np.pi / 60, #originally 60
	    threshold=100,
	    lines=np.array([]),
	    minLineLength=10, 
	    maxLineGap=25 #distance between matching angular lines
	)		

	left_line_x =[]
	left_line_y =[]
	right_line_x =[]
	right_line_y =[]

        if lines is None:
            return 50
	for line in lines:
		for x1, y1, x2, y2 in line:
     	                
			slope = (y2 - y1)*1.0/(x2 - x1)*1.0 # <-- Calculating the slope.
        
			if math.fabs(slope) < 0.5: # <-- Only extreme slope
				continue
			if slope <= 0: # <-- If the slope is negative, left group.
				left_line_x.extend([x1, x2])
				left_line_y.extend([y1, y2])
        	        else: # <-- Otherwise, right group.
				right_line_x.extend([x1, x2])
            	                right_line_y.extend([y1, y2])
        
        if ((right_line_x == []) & (right_line_y == [])):
            return 50
        if ((left_line_x == []) & (right_line_x != [])):
            return 100
        if ((right_line_x == []) & (left_line_x != [])):
            return 0

	poly_left = np.poly1d(np.polyfit( left_line_y, left_line_x, deg=1 ))
 
	left_x_start = int(poly_left(max_y))
	left_x_end = int(poly_left(min_y)) 
 
	poly_right = np.poly1d(np.polyfit( right_line_y, right_line_x, deg=1 ))
 
	right_x_start = int(poly_right(max_y))
	right_x_end = int(poly_right(min_y))

	left_yellow_line = [left_yellow, max_y, left_yellow , min_y]
	left_red_line = [left_red, max_y, left_red, min_y]
	right_yellow_line = [right_yellow, max_y, right_yellow, min_y]
	right_red_line = [right_red, max_y, right_red, min_y]
	middle_of_lane = (right_x_start - left_x_start)/2
        if left_x_start <= 0:
            left_x_start = 0
        if right_x_start >= 320:
            right_x_start = 320
	current_location = scale_value(middle_of_lane)
        if current_location < 0:
            return 0
	if current_location >100:
	    return 100
	return current_location
