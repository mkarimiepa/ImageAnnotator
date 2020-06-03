"""
ImageAnnotator - created by Muhammad T Karimi - 6/1/2020
For the purpose of Annotating images in a streamlined and easy way. Designed so the user can annotate any number of
images contained in the images directory, and the choice of the user (from 5 or 6 answer choices) will be saved in
a csv file next to the image file name.
"""

import os
import datetime
import ctypes

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Global variables
todays_date = f"{datetime.datetime.today().month}-{datetime.datetime.today().day}-{datetime.datetime.today().year}"
csv_file = f"annotations-with-numbers{todays_date}.csv"  # name of the csv output file that uses numbers not names
csv_file2 = f"annotations-with-names{todays_date}.csv"  # name of the csv output file that uses material names
numbers_to_primary_materials_dict = {1: "Brick", 2: "Wood", 3: "Glass", 4: "Concrete", 5: "Steel"}
numbers_to_secondary_materials_dict = {1: "Brick", 2: "Wood", 3: "Glass", 4: "Concrete", 5: "Steel", 6: "None"}


"""
This function asks the user what the primary material of the building in the image is, and then asks the secondary 
material that makes up the building.
  - The user can select 'Delete' for the primary material, indicating that they believe that the image is not useful
  - The user can also select 'None' for the secondary material, meaning there is no or not enough of a 2nd material
    for it to be worth mentioning
    
@return tuple that has the primary material and the secondary material
"""


def ask_material():
    secondary_material = 0  # if user says 'Delete' for 1st material, this is needed so 2nd material has a value
    while True:
        print("What is the majority construction material of the building in this image?"
              "\n1. Brick\t\t2. Wood\t\t3. Glass"
              "\n4. Concrete\t\t5. Steel\t6. Delete")
        primary_material = input("Enter number: ")
        if primary_material != '1' and primary_material != '2' and primary_material != '3' and primary_material != '4' \
                and primary_material != '5' and primary_material != '6':
            print("Invalid choice\n")
        else:
            break

    while primary_material != '6':  # if user said 'Delete', then this block is skipped as 2nd material is not needed
        print("\nWhat is the 2nd majority construction material of the building in this image, if any?"
              "\n1. Brick\t\t2. Wood\t\t3. Glass"
              "\n4. Concrete\t\t5. Steel\t6. None")
        secondary_material = input("Enter number: ")
        if secondary_material != '1' and secondary_material != '2' and secondary_material != '3' and \
                secondary_material != '4' and secondary_material != '5' and secondary_material != '6':
            print("Invalid choice")
        else:
            break
    return primary_material, secondary_material


"""
This function enables VT100 emulation, a Windows 10 setting that allows the color codes used above to actually
work and show the different colors. Otherwise, the colors would not work on the majority of terminals.
"""


def colors():
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)


# Call colors() to enable colors in text
colors()

# Start up and main menu
print(f"\n{bcolors.HEADER}WELCOME TO THE IMAGEANNOTATOR{bcolors.ENDC}")
print("The purpose of this software is to categorize images of buildings displayed to the user, the results of which"
      " will be written to 2 CSV files.\nIn order for the software to work properly, there are some rules and"
      " guidelines that must be followed.")
print("\nOnce you start, you will be shown images of buildings one-by-one, and for each image you must:")
print("1. Determine the majority construction material in that building and then enter that option into the system.")
print("2. Determine the 2nd majority construction material in the building, if any. If none, enter 0 in the system.")

print(f"\n{bcolors.WARNING}Note:{bcolors.ENDC}")
print("  -You have the option of deleting an image if the building is difficult to see, covered by other objects,"
      " not a good representation of that material,\n  too far away, if there are too many other objects/people in the"
      " image, or for other reasons you deem significant enough. If you are unsure, don't delete it.")
print("  -When you start a session, please finish the session completely, do not end halfway.")
print("  -If you restart a session, you will have to do the whole set again.")
print("  -The program will inform you when you have started and ended a session.")
print("  -For our purposes, there will be about 110 images in every set/session, so be sure to set enough time.")

while True:
    answer = input("\nDo you acknowledge the above, and are ready to begin?\n"
          "a. Yes\n"
          "b. No\n\n"
          "Enter your choice: ")
    if answer.lower() == 'b':
        quit(0)
    elif answer.lower() != 'a':
        print("Invalid choice")
    else:
        break

print(f"{bcolors.OKBLUE}Session start{bcolors.ENDC}")

images = os.listdir("images")  # files will be added in descending order, starting from 0-9, then a-z (case ignored)
open(csv_file, "w")
open(csv_file2, "w")  # these lines clear the files, if they already exist

n = 1
num_images = len(images)
for image in images:
    print(f"\n{bcolors.UNDERLINE}Image {n}/{num_images}{bcolors.ENDC}")
    os.system(f"start images/{image}")  # start the image
    primary_material, secondary_material = ask_material()  # ask user which 2 main materials make up the building
    os.system("taskkill /f /im WLXPhotoGallery.exe /t >nul 2>&1")  # close the image

    if primary_material == '6':  # if user said 'Delete' for primary material, delete image and move to next image
        os.remove(f"images/{image}")
        n += 1
        continue

    with open(csv_file, "a") as output:  # write results to first csv file, using the numbers entered
        output.write(f"{image},{primary_material},{secondary_material}\n")

    with open(csv_file2, "a") as output:  # write results to second csv file, converting the numbers to material names
        output.write(f"{image},{numbers_to_primary_materials_dict[int(primary_material)]},"
                     f"{numbers_to_secondary_materials_dict[int(secondary_material)]}\n")

    n += 1
