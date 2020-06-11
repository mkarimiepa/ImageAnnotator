"""
ImageAnnotator - created by Muhammad T Karimi - 6/1/2020
For the purpose of Annotating images in a streamlined and easy way. Designed so the user can annotate any number of
images contained in the images directory, and the choice of the user (from 5 or 6 answer choices) will be saved in
a csv file next to the image file name.
"""

import os
import datetime
import ctypes
import time


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
user = os.path.abspath("").split("\\")[2]  # current user, this value is used in the 4 variables below
path_to_imgs_to_annotate_dir = ""  # TODO
path_to_imgs_temp_dir = ""  # TODO
path_to_imgs_annotated_dir = ""  # TODO
path_to_output_csv = ""  # TODO
numbers_to_materials_dict = {1: "Brick", 2: "Wood", 3: "Glass", 4: "Concrete", 5: "Steel", 6: "None", 7: "Deleted"}
nums_to_use_dict = {1: "Agriculture", 2: "Banks", 3: "Church/Non-Profit", 4: "Colleges/Universities", 5: "Construction",
                    6: "Emergency Response", 7: "Entertainment & Recreation", 8: "Food/Drugs/Chemicals",
                    9: "General Services", 10: "Grade Schools", 11: "Heavy", 12: "High Technology", 13: "Hospital",
                    14: "Institutional Dormitory", 15: "Light", 16: "Medical Office/Clinic",
                    17: "Metals/Minerals Processing", 18: "Mobile Home", 19: "Multi Family Dwelling - Duplex",
                    20: "Multi Family Dwelling - 3-4 Units", 21: "Multi Family Dwelling - 5-9 Units",
                    22: "Multi Family Dwelling - 10-19 Units", 23: "Multi Family Dwelling - 20-49 Units",
                    24: "Multi Family Dwelling - 50+ Units", 25: "Nursing Home", 26: "Parking",
                    27: "Personal and Repair Services", 28: "Professional/Technical Services", 29: "Retail Trade",
                    30: "Single Family Dwelling", 31: "Temporary Lodging", 32: "Theaters", 33: "Wholesale Trade"}

"""
This function asks the user what the primary material of the building in the image is, and then asks the secondary 
material that makes up the building.
  - The user can select 'Delete' for the primary material, indicating that they believe that the image is not useful
  - The user can also select 'None' for the secondary material, meaning there is no or not enough of a 2nd material
    for it to be worth mentioning

@return tuple that has the primary material and the secondary material
"""


def ask_building_material():
    while True:
        print("\nWhat are the majority/primary and secondary construction materials of the building(s) in this image?"
              "\n1. Brick\t\t2. Wood\t\t3. Glass\t\t7. Delete"
              "\n4. Concrete\t\t5. Steel\t6. None")
        user_choices = input("Enter numbers with a space (Ex. '1 3', to delete: '7 7'): ")
        user_choices_list = user_choices.split(" ")  # get two users building material choices
        try:
            primary_choice = user_choices_list[0]
            secondary_choice = user_choices_list[1]
            if primary_choice.isalpha() or secondary_choice.isalpha() or int(primary_choice) < 1 or int(primary_choice) \
                    > 7 or int(secondary_choice) < 1 or int(secondary_choice) > 7:
                print("Invalid choice")  # if user entered <1 or >7 or not a number
                continue
        except (IndexError, ValueError):
            print("Invalid choice")
            continue
        break
    return int(primary_choice), int(secondary_choice)  # ignore errors, will never reach this point without values


"""
This function asks the user what the category of use of the building in the image is.

@return building_use the use of the building as selected by the user
"""


def ask_building_use():
    while True:
        print("\nWhat is the category of use of the building(s) in this image?"
              "\n 1. Agriculture\t\t\t\t 2. Banks\t\t\t\t 3. Church/Non-Profit"
              "\n 4. Colleges/Universities\t\t 5. Construction\t\t\t 6. Emergency Response"
              "\n 7. Entertainment & Recreation\t\t 8. Food/Drugs/Chemicals\t\t 9. General Services"
              "\n10. Grade Schools\t\t\t11. Heavy\t\t\t\t12. High Technology"
              "\n13. Hospital\t\t\t\t14. Institutional Dormitory\t\t15. Light"
              "\n16. Medical Office/Clinic\t\t17. Metals/Minerals Processing\t\t18. Mobile Home"
              "\n19. Multi Family Dwelling - Duplex\t20. Multi Family Dwelling - 3-4 Units"
                "\t21. Multi Family Dwelling - 5-9 Units"
              "\n22. Multi Family Dwelling - 10-19 Units\t23. Multi Family Dwelling - 20-49 Units"
                "\t24. Multi Family Dwelling - 50+ Units"
              "\n25. Nursing Home\t\t\t26. Parking\t\t\t\t27. Personal and Repair Services"
              "\n28. Professional/Technical Services\t29. Retail Trade\t\t\t30. Single Family Dwelling"
              "\n31. Temporary Lodging\t\t\t32. Theaters\t\t\t\t33. Wholesale Trade")
        user_choice = input("Enter number: ")
        try:
            if user_choice.isalpha() or int(user_choice) < 1 or int(user_choice) > 33:
                print("Invalid choice\n")  # if user entered < 1 or > 33 or not a number
                continue
        except ValueError:
            print("Invalid choice\n")
            continue
        break
    return int(user_choice)


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
      " will be\nwritten to a CSV file. In order for the software to work properly, there are some rules and"
      "guidelines that must be\nfollowed.")
print("\nOnce you start, you will be asked how many images you want to annotate for this session. "
      "Then you will be shown images\nof buildings one-by-one, and for each image you must:")
print("1. Determine the majority construction material in that building and then enter that option into the system.")
print("2. Determine the 2nd majority construction material in the building, if any. If none, enter 6 in the system.")
print("3. Determine the category of use of the building (Ex. Residential, Office, School, etc.).")

print(f"\n{bcolors.WARNING}Note:{bcolors.ENDC}")
print("  -You also have the option of deleting an image if the building is difficult to see, covered by other objects,"
      " not a\n\tgood representation of that material, too far away, if there are too many other objects/people in the"
      " image, or \t\tfor other reasons you deem significant enough. If you are unsure, don't delete it.")
print("  -When you start a session, please finish the session completely, do not end halfway.")
print("  -The program will inform you when you have started and finished a session.")
print("  -The program will let you know how many images are left to annotate, so you can enter any number <= that.")

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

while True:
    answer = input("\nHow many images do you want to annotate: ")
    # TODO: Get number of imgs in ToAnnotate directory currently
    if not answer.isdigit() or int(answer) < 1 or int(answer) > 9660:
        print("Invalid choice")
    else:
        num_images = int(answer)
        break

# Quality Test section - asking user same questions on two images who's values are already known
os.system(f"start quality_check_imgs/barn.jpg")  # show first test img
primary_material, secondary_material = ask_building_material()  # ask user 2 main materials make up the building
building_use = ask_building_use()
os.system("taskkill /f /im WLXPhotoGallery.exe /t >nul 2>&1")  # close the image

# if user got a question wrong, show them which one
if primary_material != 2 or secondary_material != 6 or building_use != 1:
    print(f"\n{bcolors.OKBLUE}This is a test question. Please review the correct answers.{bcolors.ENDC}")
    print(f"For primary material, you said: {bcolors.FAIL}{numbers_to_materials_dict[primary_material]}{bcolors.ENDC}"
          "\t\t\t\t\tCorrect answer: Wood" if primary_material != 2 else "For primary material, you said: "
                                                                         f"{numbers_to_materials_dict[primary_material]}\t\t\t\t\tCorrect answer: Wood")
    print(f"For secondary material, you said: {bcolors.FAIL}{numbers_to_materials_dict[secondary_material]}"
          f"{bcolors.ENDC}\t\t\t\t\tCorrect answer: None" if secondary_material != 6 else "For secondary material, you "
                                                                                          f"said: {numbers_to_materials_dict[secondary_material]}\t\t\t\t\tCorrect answer: None")
    print(f"For building use, you said: {bcolors.FAIL}{nums_to_use_dict[building_use]}{bcolors.ENDC}"
          f"\t\t\t\t\tCorrect answer: Agriculture" if building_use != 1 else
          f"For building use, you said: {nums_to_use_dict[building_use]}\t\t\t\t\tCorrect answer: Agriculture")
    time.sleep(5)  # pause system to give user time to read corrections before continuing

os.system(f"start quality_check_imgs/office.jpg")  # show 2nd test img
primary_material, secondary_material = ask_building_material()  # ask user 2 main materials make up the building
building_use = ask_building_use()
os.system("taskkill /f /im WLXPhotoGallery.exe /t >nul 2>&1")  # close the image

# if user got a question wrong, show them which one
if primary_material != 4 or secondary_material != 3 or building_use != 28:
    print(f"\n{bcolors.OKBLUE}This is a test question. Please review the correct answers.{bcolors.ENDC}")
    print(f"For primary material, you said: {bcolors.FAIL}{numbers_to_materials_dict[primary_material]}{bcolors.ENDC}"
          f"\t\tCorrect answer: Concrete" if primary_material != 4
          else f"For primary material, you said: {numbers_to_materials_dict[primary_material]}\t\t\t\t\tCorrect answer: Wood")
    print(f"For secondary material, you said: {bcolors.FAIL}{numbers_to_materials_dict[secondary_material]}"
          f"{bcolors.ENDC}\t\t\t\t\tCorrect answer: None" if secondary_material != 3 else
          f"For secondary material, you said: {numbers_to_materials_dict[secondary_material]}\t\t\t\t\tCorrect answer: Wood")
    print(f"For building use, you said: {bcolors.FAIL}{nums_to_use_dict[building_use]}{bcolors.ENDC}"
          f"\t\t\t\t\tCorrect answer: Agriculture" if building_use != 28 else
          f"For building use, you said: {nums_to_use_dict[building_use]}\t\t\t\t\tCorrect answer: Agriculture")
    time.sleep(5)  # pause system to give user time to read corrections before continuing

print(f"\n{bcolors.OKBLUE}Session start{bcolors.ENDC}")

# TODO: Move number of images chosen to the Temp directory from ToAnnotate directory here
images = os.listdir(path_to_imgs_temp_dir)  # files added in descending order, from 0-9, then a-z (case ignored)

n = 1
num_images = len(images)
for image in images:
    print(f"\n{bcolors.UNDERLINE}Image {n}/{num_images}{bcolors.ENDC}")
    os.system(f"start images/{image}")  # start the image
    primary_material, secondary_material = ask_building_material()  # ask user 2 main materials make up the building
    building_use = ask_building_use()
    os.system("taskkill /f /im WLXPhotoGallery.exe /t >nul 2>&1")  # close the image

    with open(path_to_output_csv, "a") as output:  # write results to first csv file, using the numbers entered
        output.write(f"{image},{primary_material},{secondary_material},{building_use},"
                     f"{numbers_to_materials_dict[primary_material]},{numbers_to_materials_dict[secondary_material]},"
                     f"{nums_to_use_dict[building_use]}\n")
    # TODO: move annotated image to the Annotated directory from Temp directory
    n += 1

if num_images > 0:
    print(f"\n{bcolors.OKGREEN}Session complete! Thank you!{bcolors.ENDC}")
