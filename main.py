from selenium import webdriver
from numpy import save
import urllib.request
import matplotlib.pyplot as plt
from selenium.webdriver.common.keys import Keys
import requests
import os
import re
from bs4 import BeautifulSoup as bs
import time
from PIL import Image
import numpy as np
from numpy import asarray




# image download runtime ~ 3 hours

# the following lists will hold a rocks, name, location (lat & lat coordinates) and the its image number
# there are a total of 8,3999 rocks that will be downloaded
image_name = []
image_id = []
image_location = []
image_link = []
image_number = 1



# main function that operates our web_crawler
# web_crawler will click through every single page on the
# website until we have downloaded every image available (8,399 images)
def page_navigator(web_crawler):
    # accessing the website we want to navigate through
    web_crawler.get("http://www.myfirstascent.com/app/routes")
    i = 0

    # there are 88 clickable location on our main page
    # while loop will run until each page has been clicked through
    # we access the clickable locations on the web page by calling
    # find_elements_by_class_name()
    # each clickable location (element) is accessible through
    # their class identifier. In this particular webpage,
    # each clickable location is part of an array with the same
    # class name
    # by calling find_elements_by_class_name we are able to access
    # each clickable element on the webpage.
    while i < 88:
        web_crawler.find_elements_by_class_name("jss135")[i].click()
        time.sleep(1)
        web_crawler.refresh()
        page_source = web_crawler.page_source

        # has_more_locations parses the source code of the web page
        # to determine if there are more clickable locations
        if has_more_locations(page_source):
            # getting the number of sub locations
            # each sub location is a JSON object with
            # with a key "name"
            num_of_sublocs = page_source.count(',"name"')

            web_crawler.find_element_by_id('integration-downshift').send_keys(Keys.TAB)
            page_source = web_crawler.page_source

            # helper function will navigate through sub locations
            navigate_sub_locations(web_crawler, num_of_sublocs)
            web_crawler.execute_script("window.history.go(-1)")
            web_crawler.refresh()
            i += 1

        else:
            # if there are no sub locations then the web page is displaying only images
            # dowload_images will download every image present on the webpage
            download_images(web_crawler)
            time.sleep(1)
            web_crawler.execute_script("window.history.go(-1)")
            web_crawler.refresh()
            i += 1


# function will navigate through each sub location
def navigate_sub_locations(web_crawler, num_of_sublocs):
    i = 0
    while num_of_sublocs > i:
        time.sleep(1)
        web_crawler.find_elements_by_class_name('jss135')[i].click()

        web_crawler.refresh()
        page_source = web_crawler.page_source

        # check if the sub location has a sub location of its own
        if has_more_locations(page_source):
            num_of_sublocs2 = page_source.count(',"name"')

            j = 0
            while num_of_sublocs2 > j:
                time.sleep(1)
                web_crawler.find_elements_by_class_name('jss135')[j].click()
                web_crawler.refresh()
                page_source = web_crawler.page_source
                time.sleep(1)

                # checking for sub locations
                if has_more_locations(page_source):
                    web_crawler.refresh()
                    page_source = web_crawler.page_source
                    num_of_sublocs3 = page_source.count(',"name"')

                    k = 0
                    while num_of_sublocs3 > k:
                        web_crawler.refresh()
                        web_crawler.find_elements_by_class_name('jss135')[k].click()
                        time.sleep(1)
                        web_crawler.refresh()
                        page_source4 = web_crawler.page_source

                        if has_more_locations(page_source4):
                            num_of_sublocs4 = page_source4.count(',"name"')

                            l = 0
                            while num_of_sublocs4 > l:
                                web_crawler.refresh()
                                time.sleep(1)
                                web_crawler.find_elements_by_class_name('jss135')[l].click()
                                time.sleep(1)
                                web_crawler.refresh()
                                page_source5 = web_crawler.page_source

                                if has_more_locations(page_source5):
                                    n = 0
                                    num_of_sublocs5 = page_source5.count(',"name"')
                                    while num_of_sublocs5 > n:
                                        web_crawler.find_elements_by_class_name('jss135')[n].click()
                                        time.sleep(1)
                                        web_crawler.execute_script("window.history.go(-1)")
                                        n += 1
                                    l += 1
                                    web_crawler.execute_script("window.history.go(-1)")

                                else:
                                    # no more clickable locations
                                    # call download_images to download
                                    # every image on the web page
                                    download_images(web_crawler)
                                    web_crawler.execute_script("window.history.go(-1)")
                                    l += 1
                            k += 1
                            web_crawler.execute_script("window.history.go(-1)")

                        else:
                            download_images(web_crawler)
                            web_crawler.execute_script("window.history.go(-1)")
                            k += 1
                    j += 1
                    web_crawler.execute_script("window.history.go(-1)")
                    web_crawler.refresh()

                else:
                    download_images(web_crawler)
                    web_crawler.execute_script("window.history.go(-1)")
                    web_crawler.refresh()
                    j += 1
            i += 1
            time.sleep(1)
            web_crawler.execute_script("window.history.go(-1)")
            time.sleep(1)
            web_crawler.refresh()

        else:
            # page contains images we need to download
            # call scroll to the bottom function
            # download each image in the page
            download_images(web_crawler)
            web_crawler.execute_script("window.history.go(-1)")
            time.sleep(1)
            web_crawler.refresh()
            i += 1


# method will interact with the load more button in page
# will keep pressing button until every image is displayed on page
# we return the number of clicks as this will help us in another function
# call later
def scroll_to_bottom(web_crawler):
    num_of_clicks = 0
    web_crawler.refresh()
    time.sleep(1)

    while len(web_crawler.find_elements_by_class_name('jss254')) > 1:
        web_crawler.find_element_by_class_name('jss254').click()
        time.sleep(1)
        num_of_clicks += 1

    return num_of_clicks


# boolean function will analyze the page source and determine if there are sub locations in the web page
def has_more_locations(page_source):
    if page_source.find('{"allRoutes":[]') > -1:
        # has more locations within web page
        return True
    else:
        # page has no more locations, instead page is filled with images
        return False


# function will download an image
def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpeg'
    urllib.request.urlretrieve(url, full_path)


# function will populate your street_view and satellite_view folders
# with the downloaded images from the website
def fill_folders(rock_link, number_of_rocks, rock_location, image_id):
    # Each rock image will be named after their respective image_number, from 1 to 8,399
    global image_number
    i = 0

    # while loop will download every rock image
    while number_of_rocks > i:
        current_directory = os.getcwd()
        file_path = current_directory + '\street_view_rocks/'
        url = rock_link[i]
        file_name = image_id[i]
        download_image(url, file_path, file_name)

        file = open(r'./street_view_rocks/coordinates.txt', 'a')
        rock_id_and_loc = 'rock id: ' + image_id[i] + ' coordinates: ' + rock_location[i] + '\n'
        file.write(rock_id_and_loc)
        file.close()
        # uncomment code to begin downloading satellite view for rocks

        # file_path = current_directory + '\satellite_view/'
        #
        # # call helper function to get the url for the satellite image
        # # of the rock we downloaded above
        # satellite_url = get_satellite_url(rock_location[i])
        # download_image(satellite_url, file_path, file_name)
        #
        image_number = int(image_number)
        image_number += 1
        i += 1


# Function will download every image displayed on the web page
def download_images(spider):
    # scoll_to_bottom function interacts with the "load more" button present on the webpage, each click
    # is associated with displaying up to 50 more images (pagination) so we count the number
    # of clicks to know how many images we need to download
    num_of_clicks = scroll_to_bottom(spider)
    url = spider.current_url
    soup = bs(requests.get(url).content, "html.parser")






    # the webpage is set up so we have limiations to the amount of JSON objects we can access through the
    # web page's source code. we can only access 50 json image objects through the source code present on the webpage
    # here we count each "name" key to know how images are present on the page.
    page_source = spider.page_source
    number_of_images = re.findall(r'"name":', page_source)
    number_of_images = len(number_of_images)
    i = 0

    # while loop will parse through the web page source and extract the name, coordinates, and image link associated
    # with each rock
    while number_of_images > i:
        index = page_source.find('"id":')
        page_source = page_source[index + 5:]
        index = page_source.find(',')
        rock_id = page_source[:index]
        index = page_source.find('"name":"')
        page_source = page_source[index + 8:]
        index = page_source.find(',')
        name = page_source[:index - 1]
        name = re.sub(r'\W+', '', name)
        index = page_source.find('"lat":')
        page_source = page_source[index + 6:]
        index = page_source.find(',')
        lat = page_source[:index]
        index = page_source.find('"lon":')
        page_source = page_source[index + 6:]
        index = page_source.find(',')
        lon = page_source[:index]
        location = lat + ',' + lon
        index = page_source.find('"image_url":"')
        page_source = page_source[index + 13:]
        index = page_source.find('"')
        image_url = page_source[:index]

        image_id.append(rock_id)
        image_name.append(name)
        image_location.append(location)
        image_link.append(image_url)
        i += 1

    # call function to populate our street_view and satellite_view image
    fill_folders(image_link, len(image_name), image_location, image_id)

    # empty the list after each download
    image_name[:] = []
    image_link[:] = []
    image_location[:] = []
    image_id[:] = []



    # if num_of_clicks is greater than 0 it means we have more than 50 images to download
    # which means the web pages source code only displays the JSON information for 50 images
    # in order to get the remaining images JSON information we must make a GET request
    # the number of requests is equal to the number of times we clicked load more
    # each click returns a JSON array of up to 50 elements. This pagination feature
    # on the web page requires us to make GET requests
    if num_of_clicks > 0:
        # more images to download
        # num_of_clicks = number of GET requests to make

        i = 0
        offset = 50
        while i < num_of_clicks:
            url = get_url(spider, offset)
            time_param = str(int(round(time.time() * 1000)))
            url = url + time_param

            r = requests.get(url)
            json_info = r.text

            # the number of occurrences of "name": is the number of loops we do
            # each loop will create a folder for each image

            num_of_images = json_info.count('"name":')

            j = 0

            while j < num_of_images:
                index = json_info.find('"id":')
                json_info = json_info[index + 5:]
                index = json_info.find(',')
                rock_id = json_info[:index]
                index = json_info.find('"name":"')
                json_info = json_info[index + 8:]
                index = json_info.find(',')
                name = json_info[:index - 1]
                name = re.sub(r'\W+', '', name)
                index = json_info.find('"lat":')
                json_info = json_info[index + 6:]
                index = json_info.find(',')
                lat = json_info[:index]
                index = json_info.find('"lon":')
                json_info = json_info[index + 6:]
                index = json_info.find(',')
                lon = json_info[:index]
                location = lat + ',' + lon
                index = json_info.find('"image_url":"')
                json_info = json_info[index + 13:]
                index = json_info.find('"')
                image_url = json_info[:index]

                image_id.append(rock_id)
                image_name.append(name)
                image_location.append(location)
                image_link.append(image_url)

                j += 1


            # populate our folders with the remaining images on the page
            fill_folders(image_link, len(image_name), image_location, image_id)

            # recycle the list
            image_name[:] = []
            image_link[:] = []
            image_location[:] = []
            image_id[:] = []

            offset += 50
            i += 1



    else:
        print('No more images to download')


# function uses the static maps api to download a satellite image view of a rock
# a valid static maps api key is required to use this function
# function returns a url which will display a satellite image of the coordinates inputted
# create your own maps static api key to use this function
# you are billed (very very very small amount) per api call
def get_satellite_url(coordinates):
    url_one = 'https://maps.googleapis.com/maps/api/staticmap?'
    url_two = 'center='
    url_three = '&zoom=20&size=400x400&scale=2&maptype=satellite&key='

    file = open('config.txt', 'r')

    # enter your own api key here
    api_key = file.readline()

    url_two = url_two + coordinates
    url_three = url_three + api_key

    final_url = url_one + url_two + url_three
    return final_url

# helper function returns the url parameters on a given webpage, we need these parameters
# for when we are making GET requests to access the JSON object of images in a webpage
# where more than 50 images are present
def get_url_params(web_crawler):
    params = []

    page_source = web_crawler.page_source
    index = page_source.find('"userLat":')
    page_source = page_source[index + 10:]
    index2 = page_source.find(',')
    userLat = page_source[:index2]
    params.append(userLat)

    index = page_source.find('"userLon":')
    page_source = page_source[index + 10:]
    index2 = page_source.find(',')
    userLon = page_source[:index2]
    params.append(userLon)

    index = web_crawler.current_url.find('=')
    areaId = web_crawler.current_url[index + 1:]
    params.append(areaId)

    return params

# function will return a url that will be used to make a GET request to acess the JSON information
# for web pages displaying more than 50 images
def get_url(web_crawler, offset):
    url_params = get_url_params(web_crawler)
    url_param_offset = str(offset)

    url_one = 'http://www.myfirstascent.com/routes?offset='
    param_divider = '&'
    url_two = 'lat='
    url_three = 'lon='
    url_four = 'areaId='
    url_five = 'maxCreatedAt='

    # stitching together the url with its parameters to make a GET request and receive json information about
    # the images on the web page
    final_url = url_one + url_param_offset + param_divider + url_two + url_params[0] + param_divider
    final_url = final_url + url_three + url_params[1] + param_divider + url_four + url_params[2] + param_divider
    final_url = final_url + url_five

    return final_url


# each list will contain 8,399 images
street_data = []
satellite_data = []


# we create the street_dataset by taking every image in the street_view folder
# and encoding them to pixel dimension of 104x104 then converting them
# to numpy arrays
# arrays will later be saved as .npy files to make data portability easier
def create_street_dataset(num_of_images):
    i = 1


    while i <= num_of_images:

        # These two select images have an image channel of 4, so we ignore them
        if i == 3702:
            i += 1
        elif i == 3704:
            i += 1
        else:
            path = os.getcwd()
            path = path + '/street/'
            file_name = str(i) + '.jpeg'
            path = path + file_name

            print(path)


            image = Image.open(path)
            image = image.resize((600, 600))
            image = asarray(image)

            street_data.append(image)
            i += 1


# we create the street_dataset by taking every image in the satellite_view folder
# and encoding them to pixel dimension of 104x104 then converting them
# to numpy arrays
# arrays will later be saved as .npy files to make data portability easier
def create_satellite_dataset(num_of_images):
    i = 1


    while i <= num_of_images:

        # These two select images have an image channel of 4, so we ignore them
        if i == 3702:
            i += 1
        elif i == 3704:
            i += 1
        else:
            path = os.getcwd()
            path = path + '/sat/'
            file_name = str(i) + '.jpeg'
            path = path + file_name

            print(path)
            image = Image.open(path).convert("RGB")
            image = image.resize((600, 600))
            image = asarray(image)


            satellite_data.append(image)
            i += 1









# begin the image download process
# total runtime ~ 3 hours
# 10 total gb of data
# 8,399 images of rocks and 8,399 satellite images
# 16,798 images

# creating our webcrawler
crawler = webdriver.Chrome("C:/Users/willi/Desktop/CSUSM/Spring '20/CS 497/Final/chromedriver.exe")
page_navigator(crawler)

# converting our images to a numpy dataset
# shape of each dataset is (8,379, 104, 104, 3)
# 8,379 images, 104x104 pixels, RGB so 3 color channels
# create_street_dataset(image_number)
# create_satellite_dataset(8399)
#
# street_data = asarray(street_data)
# satellite_data = asarray(satellite_data)
#
# np.save('street_dataset_600p.npy', street_data)
# np.save('satellite_dataset_600p.npy', satellite_data)
