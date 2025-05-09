##HOUGH-LINE-DETECTION ALGORITHMUS

#%matplotlib inline
import cv2
import matplotlib.pyplot as plt
import numpy as np


import math
def find_hough_lines(image, edge_image, num_rhos, num_thetas, bin_threshold):
  #image size
  img_height, img_width = edge_image.shape[:2]
  img_height_half = img_height / 2
  img_width_half = img_width / 2
  
  # Rho and Theta ranges
  diag_len = np.sqrt(np.square(img_height) + np.square(img_width))
  dtheta = 180 / num_thetas
  drho = (2 * diag_len) / num_rhos
  
  ## Thetas is bins created from 0 to 180 degree with increment of the provided dtheta
  thetas = np.arange(0, 180, step=dtheta)
  
  ## Rho ranges from -diag_len to diag_len where diag_len is the diagonal length of the input image
  rhos = np.arange(-diag_len, diag_len, step=drho)
  
  # Calculate Cos(theta) and Sin(theta) it will be required later on while calculating rho
  cos_thetas = np.cos(np.deg2rad(thetas))
  sin_thetas = np.sin(np.deg2rad(thetas))
  
  # Hough accumulator array of theta vs rho, (rho,theta)
  accumulator = np.zeros((len(rhos), len(thetas)))
  
  # Hough Space plot for the image.
  #figure = plt.figure()
  #hough_plot = figure.add_subplot()
  #hough_plot.set_facecolor((0, 0, 0))
  #hough_plot.title.set_text("Hough Space")
  
  # Iterate through pixels and if non-zero pixel process it for hough space
  for y in range(img_height):
    for x in range(img_width):
      if edge_image[y][x] != 0: #white pixel
        edge_pt = [y - img_height_half, x - img_width_half]
        hough_rhos, hough_thetas = [], [] 
        
        # Iterate through theta ranges to calculate the rho values
        for theta_idx in range(len(thetas)):
          # Calculate rho value
          rho = (edge_pt[1] * cos_thetas[theta_idx]) + (edge_pt[0] * sin_thetas[theta_idx])
          theta = thetas[theta_idx]
          
          # Get index of nearest rho value
          rho_idx = np.argmin(np.abs(rhos - rho))
          
          #increment the vote for (rho_idx,theta_idx) pair
          accumulator[rho_idx][theta_idx] += 1
          
          # Append values of rho and theta in hough_rhos and hough_thetas respectively for Hough Space plotting.
          hough_rhos.append(rho)
          hough_thetas.append(theta)
        
        # Plot Hough Space from the values
        #hough_plot.plot(hough_thetas, hough_rhos, color="white", alpha=0.05)

  # accumulator, thetas, rhos are calculated for entire image, Now return only the ones which have higher votes. 
  # if required all can be returned here, the below code could be post processing done by the user.
  
  # Output image with detected lines drawn
  output_img = image.copy()
  # Output list of detected lines. A single line would be a tuple of (rho,theta,x1,y1,x2,y2) 
  out_lines = []
  
  for y in range(accumulator.shape[0]):
    for x in range(accumulator.shape[1]):
      #print(f"nombre de votes:( {accumulator[y][x]} ) ") # If number of votes is greater than bin_threshold provided shortlist it as a candidate line
      if accumulator[y][x] > bin_threshold:
        rho = rhos[y]
        theta = thetas[x]
        
        # a and b are intercepts in x and y direction
        a = np.cos(np.deg2rad(theta))
        b = np.sin(np.deg2rad(theta))
        
        x0 = (a * rho) + img_width_half
        y0 = (b * rho) + img_height_half
        
        # Get the extreme points to draw the line
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        
        
        
        # Draw line on the output image
        output_img = cv2.line(output_img, (x1,y1), (x2,y2), (0,255,0), 1)
        
        # Add the data for the line to output list
        out_lines.append((rho,theta,x1,y1,x2,y2))

 
  
  return output_img, out_lines


def proceed(img , box):
    num_rho = 180
    num_theta = 180
    bin_threshold = 20
    lines_are_white = True
    input_img = img
    #input_img = cv2.imread('./TestRoi.jpg')
    #Edge detection on the input image
    edge_image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    ret, edge_image = cv2.threshold(edge_image, 120, 255, cv2.THRESH_BINARY_INV)
    #edge_image = cv2.Canny(edge_image, 100, 200)
    
    if edge_image is not None:
            
        #print ("Detecting Hough Lines Started!")
        line_img, lines = find_hough_lines(input_img, edge_image, num_rho, num_theta, bin_threshold)
        
        #cv2.imshow('Detected Lines', line_img)
        #print(f"nombre de lignes detectes:( {len(lines)} ) ")
        if (len(lines) == 0):
            xmin, ymin, xmax, ymax = box
            return (xmin,ymin),(xmax, ymax)
        first_line = lines[(int)(len(lines) / 2)]
        rho, theta, x1, y1, x2, y2 = first_line
        xmin, ymin, xmax, ymax = box
        first_line_img = input_img.copy()

        if(((y2-y1)/(x2-x1)) > 0):
            
            return (xmin,ymin),(xmax, ymax)
        else:
            
            return (xmax,ymin),(xmin, ymax)
        
    
    else:
        print ("Error in input image!")

