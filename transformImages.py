import cv2
import numpy as np
import glob
import os
import shutil
import sys

# Author: jtrebicki
# Written: June of 2023



# Here you can set the output path of the images
folder_path = './done/'  

# We get a list of all files in the output folder; we search the one with the highest number
# Images are output as "output1.png","output2.png" etc.
# We do this so we dont delete old images!
files = os.listdir(folder_path)
filtered_files = [file for file in files if file.startswith('output') and file.endswith('.png')]
numbers = [int(file.split('output')[1].split('.png')[0]) for file in filtered_files]

# if there are no output files yet, numbers will be empty!
if numbers:
    # We get the maximum number
    highest_number = max(numbers)
    print(f"The highest number is: {highest_number}")
    # the new numbers will start one after the max number
    i = highest_number+1
else:
    i = 0




# Preparing data structures to save results
images = []
points = []
scaled_image = 0


# This code handles showing the UI and registring clicks, so you can select the four points
def click_event(event, x, y, flags, param):
    global points, image, scaled_image, scale_ratio

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
           
            points.append([x, y])
            cv2.circle(scaled_image, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Scaled Image", scaled_image)
            if len(points) >= 4:
                cv2.putText(
                    scaled_image,
                    "Four points selected!",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
                cv2.imshow("Scaled Image", scaled_image)
                cv2.waitKey(100)
                perspective_transform(scale_ratio)
        else:
            cv2.putText(
                scaled_image,
                "Four points selected!",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.imshow("Scaled Image", scaled_image)
            cv2.waitKey(100)
            perspective_transform(scale_ratio)


# handle the perspective transform
def perspective_transform(scale_ratio):
    print("Perspective Transform")
    global points, image

    width, height = image.shape[1], image.shape[0]

    src_pts = np.array(points, dtype=np.float32) / scale_ratio
    dst_pts = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32,
    )

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    result = cv2.warpPerspective(image, matrix, (width, height))
    # save the result of the transform after putting finishing touches on
    finishing_touches(result)


# finishing touches and saving the image
def finishing_touches(image):
    print("Finishing touches")
    global images, i
    
    # Append image to array
    images.append(image)
    # export as output<Number>.png
    cv2.imwrite("./done/output"+str(i)+".png",images[-1])
    print("Saved ./done/output"+str(i)+".png")
    i=i+1


    # Do the next image
    next_image()


def next_image():
    print("Next Image")
    global points, image, scaled_image, scale_ratio, images

    folder_path = "./"
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif"]
    image_files = []

    # Get all image files from the current folder
    for extension in image_extensions:
        pattern = os.path.join(folder_path, extension)
        image_files.extend(glob.glob(pattern))


    # if there are image files left
    if image_files:
        
        print("There are images left.");
        image_path = image_files[0]
        points = []
        # read in the image
        image = cv2.imread(image_path)
        
        # move the image to the used folder
        used_folder = "./used"
        os.makedirs(used_folder, exist_ok=True)
        shutil.move(image_path, os.path.join(used_folder, os.path.basename(image_path)))
        
        # if the image doesnt fit on the screen, scale it down
        max_width = 400
        if image.shape[1] > max_width:
            scale_ratio = max_width / image.shape[1]
            scaled_image = cv2.resize(
                image, (max_width, int(image.shape[0] * scale_ratio)))
        else:
            scale_ratio = 1.0
            scaled_image = image.copy

        cv2.namedWindow("Scaled Image")
        cv2.setMouseCallback("Scaled Image", click_event)
        cv2.imshow("Scaled Image", scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # quit the program
    else:
        # destroy all windows and quit!
        print("no images left, quitting!")
        cv2.destroyAllWindows()
        sys.exit()





# This gets called when the program gets started
print("First start:")
next_image()