from shapely.geometry import Point
from requests import get
from json import loads
from time import sleep
from keys import *

ratio = 112000 

# API : https://www.jawg.io/en/elevation/
def elevation_jawg(points, locs, api_limit=100):
    len_p = len(points)
    print(len_p)
    if len_p > api_limit:
        mod = len_p % api_limit
        coef = (len_p - mod) / api_limit
        # I using recursive because api limits
        for i in range(int(coef)):
            elevation_jawg(points[i*api_limit:(i*api_limit)+api_limit], locs)
            sleep(1) # for api limits
        elevation_jawg(points[(i*api_limit)+api_limit:(i*api_limit)+api_limit+mod], locs)

    else:
        locations=""
        for point in points:
            locations+=str(point.x) + "," + str(point.y) + "%7C"
                                                         # %7C = |
                                                         # [:-3] is for delete last %7C
        url = f"https://api.jawg.io/elevations?locations={locations[:-3]}&access-token={api_jawg}"
        locs.extend(loads(get(url).text))


# API : https://developers.google.com/maps/documentation/elevation/start
def elevation_google( points, locs, api_limit=512):
    len_p = len(points)
    if len_p > api_limit:
        mod = len_p % api_limit
        coef = (len_p - mod) / api_limit
        # I using recursive because api limits
        for i in range(int(coef)):
            elevation_google(points[i*api_limit:(i*api_limit)+api_limit], locs)
        elevation_google(points[(i*api_limit)+api_limit:(i*api_limit)+api_limit+mod], locs)

    else:
        locations=""
        for point in points:
            locations+=str(point.x) + "," + str(point.y) + "%7C"
                                                         # %7C = |
                                                         # [:-3] is for delete last %7C
        url=f"https://maps.googleapis.com/maps/api/elevation/json?locations={locations[:-3]}&key={api_google}"
        locs.extend(loads(get(url).text)['results'])


def elevation(points, locs, api_limit, api):
    if api == 'google':
        elevation_google(points, locs, api_limit)
    elif api == 'jawg':
        elevation_jawg(points, locs, api_limit)


def parser(lat, lng, extent, gap):
    gap_m = gap/ratio
    extent_m = extent/ratio
    count = extent/gap
    points = list()
    
    center = Point(lat,lng)
    corners_x, corners_y = center.buffer(extent_m, cap_style=3).exterior.coords.xy
    lat_, lng_ = corners_x[0], corners_y[0]


    points.append(center)

    for j in range((int(count)*2)):        
        for i in range((int(count)*2)):
            points.append(Point(lat_, lng_))
            lng_ -= gap_m
        lat_ -= gap_m
        lng_ += (int(count)*gap_m*2)

    
    return points