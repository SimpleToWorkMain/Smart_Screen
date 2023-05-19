import time
import cv2
import mss
import numpy
import pytesseract
from win32api import GetSystemMetrics
import os
import time
import subprocess

pytesseract.pytesseract.tesseract_cmd = f'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def get_keywords():
    folder_name = "\\".join(os.path.dirname(__file__).split("\\")[:-1])
    # print(folder_name)
    keyword_folder = f'{folder_name}\\Keywords'

    list_files = os.listdir(keyword_folder)
    keywords = []
    all_keywords = []
    for file in list_files:
        # opening the file in read mode
        my_file = open(f'{keyword_folder}\\{file}', "r")

        # reading the file
        data = my_file.read()
        data_list = data.split("\n")
        # print(data_list)
        keywords.extend(data_list)
        # replacing end of line('/n') with ' ' and
        # # splitting the text it further when '.' is seen.
        # data_into_list = data.replace('\n', ' ').split(".")
        #
        # # printing the data
        # print(data_into_list)
    # print(keywords)
    #
    switch_order = [" ".join([x.split(" ")[1], x.split(" ")[0]]) for x in keywords if  len(x.split(" "))== 2]
    keywords.extend(switch_order)
    all_keywords.extend(keywords)
    add_plus = [x.replace(" ", "+") for x in keywords if " " in x]
    all_keywords.extend(add_plus)
    add_minus = [x.replace(" ", "-") for x in keywords if " " in x]
    all_keywords.extend(add_minus)

    if " " in all_keywords:
        all_keywords.remove(" ")
    return all_keywords

def check_screen_for_text():
    end_loop = False

    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    mon = {'top': 0, 'left': 0, 'width':5000, 'height': 5000}

    while end_loop is False:
        keywords = get_keywords()
        counter = 0
        im = numpy.asarray(mss.mss().grab(mon))
        text = pytesseract.image_to_string(im).lower()

        for keyword in keywords:
            if keyword.lower() in text:
                start_position = text.find(keyword)
                length_of_keyword = len(keyword)
                end_position = start_position + length_of_keyword

                full_text = text[start_position-1:end_position+1]
                if keyword.lower() == full_text.strip() and keyword.lower() != "":
                    # print(f"ALERT BAD WORD DETECTED {keyword} {start_position}")
                    counter +=1
                    # break

                # break
        print(f'{counter} Risky Words Detected')
        if counter >0:
            subprocess.call("TASKKILL /f /IM CHROME.EXE")

        # time.sleep(1)
    # print("Don't F With Me")


            # cv2.imshow('Image', im)
            #
            # # Press "q" to quit
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break
            #
            # # One screenshot per second
            # time.sleep(1)


check_screen_for_text()