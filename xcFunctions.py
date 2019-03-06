import urllib
import urllib.request
import json
import os

xc_API = "http://www.xeno-canto.org/api/2/recordings?query="
link = None
temp = None

# Checks if the users input is a country


def xc_if_country(usr_input):
    with open("countries.txt", "r") as countries:
        for line in countries:
            if usr_input.casefold() in line.casefold():
                global link
                country = usr_input.replace(" ", "&")
                link = xc_API + "cnt:" + country
                break
        else:
            xc_if_species(usr_input)

    return(link)


def xc_if_species(usr_input):
    global link
    genus, species = usr_input.split(" ")
    link = xc_API + genus + "%20" + species
    return(link)


def xc_get_data(link):
    global temp
    temp = urllib.request.urlopen(link)
    status = temp.getcode()
    if status == 200:
        temp = json.load(temp)
        if temp["numRecordings"] == "0":
            print("There seems to have been an error with your request. No recordings found")
        else:
            xc_save_data(usr_input, temp)
    else:
        print("Code: " + status +
              "There seems to have been an error with your request.")


def xc_save_data(usr_input, temp):
    file_name = usr_input.replace(" ", "")
    current_directory = os.getcwd()
    path = current_directory + "/recordings/" + usr_input
    os.makedirs(path)
    with open(os.path.join(path, file_name + ".json"), "w") as outfile:
        json.dump(temp, outfile)
    for p in temp["recordings"]:
        recording_url = "https:" + p["file"]
        download_file = "XC" + p["id"] + " - " + p["en"] + " - " + p["gen"] + " " + p["sp"] + ".mp3"
        full_filename = os.path.join(path, download_file)
        urllib.request.urlretrieve(recording_url, full_filename)



usr_input = input("Please enter the species latin name or country: ")
xc_if_country(usr_input)
xc_get_data(link)