from tkinter import *
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""tkinter program that uses web scrapping to get weather and temperature data for different cities.
    user can input their home city and add other locations that will be displayed on the home screen."""
# TODO: add a menu bar at the top that allows for the user to get different info (snowfall, wind, etc.)


def drawMainScreen():
    """draw the main screen"""
    title = ttk.Label(window, text="Weather Finder")
    title.grid(column=0, row=0, columnspan=3)
    title.configure(font="default, 50")
    locationFile = open("locations.txt", 'r')
    locations = locationFile.readlines()
    if not locations:
        addHome()
    else:
        displayHome(locations)


def displayHome(locations):
    """display the home screen with home and location weather"""
    # set the home weather info and build the main screen
    home.set(getLocationInfo(locations[0].strip()))
    homeWindow.grid(column=0, row=1, columnspan=3)
    homeWindow.columnconfigure(0, weight=1)
    homeWindow.rowconfigure(0, weight=1)
    homeTitle = ttk.Label(homeWindow, text="Home", width=40)
    homeTitle.grid(column=0, row=0)
    homeTitle.configure(font='default, 18', foreground='red')
    homeLabel = ttk.Label(homeWindow, textvariable=home, width=40, padding='0 10 0 10', font='default 14 bold')
    homeLabel.grid(column=0, row=1)
    locationsTitle = ttk.Label(homeWindow, text="Locations", width=40)
    locationsTitle.grid(column=0, row=2)
    locationsTitle.configure(font='default, 18', foreground='blue')
    # display all the locations the user has added so far
    locInfo = []
    rowCount = 3
    for i in range(1, len(locations)):
        loc = getLocationInfo(locations[i].strip())
        locInfo.append(ttk.Label(homeWindow, text=loc, width=45, padding='0 5 0 5'))
        locInfo[i-1].grid(column=0, row=2+i)
        rowCount += 1
    # draw the prompt that allows the user to enter a new location
    enterLocLbl = ttk.Label(homeWindow, text="Enter a new location:", padding='0 10 0 5')
    newLoc = ttk.Entry(homeWindow, textvariable=location, width=10)
    enterLocLbl.place(x=150, y=62)
    root.update()
    newLoc.place(x=300, y=68)
    # if the user presses 'Enter', take the input from the location entry box
    root.bind('<Return>', addNewLocation)


def addNewLocation(*args):
    """add a location to the locations text file."""
    # add the new location value to the text file
    locationFile = open('locations.txt', 'a')
    locationFile.write(location.get() + '\n')
    locationFile.flush()
    # update the main screen
    drawMainScreen()


def getLocationInfo(loc):
    """gets the weather information for the user's home city"""
    url = "https://www.google.com/search?q={}+weather".format(loc)
    # initiate a headless chrome browser
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome("drivers/chromedriver", options=chromeOptions)
    # go to the webpage
    browser.get(url)
    # get the temperature text
    temp = browser.find_element_by_class_name("wob_t").text
    weather = browser.find_element_by_id("wob_dc").text
    print("city: " + loc)
    print("temperature displayed: " + temp)
    print("weather displayed: " + weather)
    browser.quit()
    # return the string value displaying the city name, weather, and temperature
    return "{}: {}\u00B0C, {}".format(loc.capitalize(), temp, weather)


def addHome():
    """display the frame that allows the user to set their home city. Only runs if user has no locations"""
    print("no locations present, prompt user to input home location")
    # if the user has not initialized the program before, prompt them to enter their home city
    addHomeWindow.grid(column=0, row=1)
    ttk.Label(addHomeWindow, text="Welcome to Weather Finder! You currently don't have any locations."
                                  "\nPlease input your home location below:", padding='0 10 0 10') \
        .grid(column=0, row=1, columnspan=2)
    ttk.Label(addHomeWindow, text="My home city:").grid(column=0, row=2, sticky=E)
    homeEntry = ttk.Entry(addHomeWindow, width=15, textvariable=location)
    homeEntry.grid(column=1, row=2, sticky=W)
    homeEntry.focus()
    root.bind('<Return>', addHomeLocation)


def addHomeLocation(*args):
    """add a location to the locations text file."""
    # write the home location to the text file
    locationFile = open('locations.txt', 'a')
    locationFile.write(location.get() + '\n')
    locationFile.flush()
    locationFile.close()
    addHomeWindow.grid_forget()
    # re-draw the main screen
    drawMainScreen()


# create the main screen root
root = Tk()
root.title("Weather Finder")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# initialize string variables for location and home values
location = StringVar()
home = StringVar()
# create the main window and main home window
window = ttk.Frame(root, padding='3 3 12 12', width=1000)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
addHomeWindow = ttk.Frame(window, padding='3 3 12 12')
homeWindow = ttk.Frame(window)
window.grid()
drawMainScreen()
root.mainloop()
