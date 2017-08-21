import time
import datetime

import numpy as np
import matplotlib.pylab as plt

def transform_coordinate_geo2earthcentered(long, lat, altitude):
    radius = altitude + 6371000.0
    x = radius * np.cos(lat * np.pi/180) * np.sin(long * np.pi/180)
    y = radius * np.cos(lat * np.pi/180) * np.cos(long * np.pi/180)
    z = radius * np.sin(lat * np.pi/180)

    return x,y,z

def markers(f, number, lon, lat):
    content = "jsMaps.api.marker(map,{position: {lat: "+str(lat)+",lng: "+str(lon)+"}, title: 'Marker No "+str(number)+"',draggable: false})\n"
    f.write(content)

def mapcenter(f, lon, lat):

    content = "        var map = jsMaps.api.init(\n" \
    "                '#map',\n"\
    "                'native',\n"\
    "                {\n"\
    "                    center: {\n"\
    "                        latitude: "+ str(np.mean(lat)) +",\n"\
    "                        longitude: "+ str(np.mean(lon)) +"\n"\
    "                    },\n"\
    "                    zoom: 18,\n"\
    "                    mouse_scroll: true,\n"\
    "                    zoom_control: true,\n"\
    "                    map_type: true\n"\
    "                },tiles\n"\
    "        );\n"

    f.write(content)

def locations(f, number, colour, lon, lat):

    content = "        var polyLine"+str(number)+" = [\n"
    f.write(content)
    for i in range(len(lon)):
        #print(i, lat[i], lon[i])
        if i < len(lon) - 1:
            content = "            {lat: " + str(lat[i]) + ",lng:  " + str(lon[i]) + "},\n"
            f.write(content)
        if i == len(lon) - 1:
            content = "            {lat: " + str(lat[i]) + ",lng:  " + str(lon[i]) + "}\n"
            f.write(content)

    content = "        ];\n"\
    "        \n"\
    "        jsMaps.api.polyLine(map,{\n"\
    "            path: polyLine"+str(number)+",\n"\
    "            strokeColor: '"+colour+"',\n"\
    "            strokeOpacity: 0.2,\n"\
    "            strokeWeight: 0.6,\n"\
    "            draggable: true,\n"\
    "            editable: false\n"\
    "        });\n\n"

    content = content + "		jsMaps.api.circle(map,{\n"\
    "            center:  {lat: " + str(np.mean(lat)) + ", lng: " + str(np.mean(lon)) + "},\n"\
    "            radius: 2,\n"\
    "            strokeColor: '"+colour+"',\n"\
    "            strokeOpacity: 0.8,\n"\
    "            strokeWeight: 2,\n"\
    "            fillColor: '#000000',\n"\
    "            fillOpacity: 0.35,\n"\
    "            editable: false,\n"\
    "            draggable: false\n"\
    "        });\n"


    f.write(content)

def map(file):
    timestamp = []
    latitude = []
    longitude = []
    altitude = []
    satellites = []

    #with open(file) as f:
    import os
    import zipfile

    with zipfile.ZipFile(file) as z:
        for filename in z.namelist():
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    tmp1 = ""
                    tmp2 = ""

                    for line in f:
                        if str(line).find("$GPGGA") > -1:
                            tmp1 = str(line).split(",")

                        if str(line).find("$GPRMC") > -1:
                            tmp2 = str(line).split(",")

                        if len(tmp1) > 0 and len(tmp2) > 0 and str(line).find("$GPRMC") > -1:
                            if tmp1[1] == tmp2[1] and len(tmp1[2]) > 0:

                                lat = 1.0
                                if tmp1[3] == "S":
                                    lat = -1.0

                                lon = 1.0
                                if tmp1[5] == "W":
                                    lon = -1.0

                                s = tmp1[1][0:2]+":"+tmp1[1][2:4]+":"+tmp1[1][4:]+" "+tmp2[9][0:2]+"-"+tmp2[9][2:4]+"-"+tmp2[9][4:6]
                                unixtime = time.mktime(datetime.datetime.strptime(s, "%H:%M:%S.%f %d-%m-%y").timetuple())

                                timestamp.append(unixtime)
                                latitude.append(lat * float(tmp1[2][0:2]) + float(tmp1[2][2:])/60.0)
                                longitude.append(lon * float(tmp1[4][0:3]) + float(tmp1[4][3:])/60.0)
                                altitude.append(float(tmp1[9]))
                                satellites.append(float(tmp1[7]))

                    '''
                    print(unixtime,
                          lat * float(tmp1[2][0:2]) + float(tmp1[2][2:])/60.0,
                          lon * float(tmp1[4][0:3]) + float(tmp1[4][3:])/60.0,
                          tmp1[9],
                          "fix", tmp1[6],
                          "sats", tmp1[7],
                          "hdop", tmp1[8])
                    '''
    return timestamp, longitude, latitude, altitude, satellites


import os

folders = ['input/2/different/',
          'input/1/different/',
          'input/2/same/',
          'input/1/same/']

colour = ["#FF0000",
          "#FFFF00",
          "#00FF00",
          "#FF00FF"]

name = ["1: shack window",
        "1: roof1 free sky",
        "2: roof2 window",
        "2: roof2 free sky"]

origin = [[48.77701, 9.23558, 236.0],
          [48.777042, 9.23548, 242.0],
          [48.7770, 9.2356, 242.0],
          [48.7770, 9.2356, 241.0]]

sats_count = []
distance_count = []
longitude = []
latitude = []
unixtime = []
satellites = []
altitude = []
distance = []
distance_to_origin = []

for i in range(len(folders)):
    tmp1 = []
    tmp2 = []

    for j in range(20):
        tmp1.append(0)
        tmp2.append(0)

    sats_count.append(tmp1)
    distance_count.append(tmp2)


for folder in range(len(folders)):

    lon = []
    lat = []
    tim = []
    alt = []
    sats = []

    for path, dirs, files in os.walk(folders[folder]):

        # sort dirs and files
        dirs.sort()
        files.sort()

        for file in files:
            print(file)
            out = map(path+file)
            for position in range(len(out[0])):
                lon.append(out[1][position])
                lat.append(out[2][position])
                tim.append(out[0][position])
                alt.append(out[3][position])
                sats.append(out[4][position])
            print("test", len(out[0]), len(out[1]), len(out[2]))


    longitude.append(lon)
    latitude.append(lat)
    unixtime.append(tim)
    altitude.append(alt)
    satellites.append(sats)

    dist = []

    xm,ym,zm = transform_coordinate_geo2earthcentered(np.mean(lon), np.mean(lat), np.mean(alt))
    for i in range(len(lat)):
        x,y,z = transform_coordinate_geo2earthcentered(lon[i], lat[i], alt[i])
        dist.append(((x-xm)**2 + (y-ym)**2 + (z-zm)**2)**0.5)

    distance.append(dist)


    dist_origin = []

    xm,ym,zm = transform_coordinate_geo2earthcentered(origin[folder][1], origin[folder][0], origin[folder][2])
    for i in range(len(lat)):
        x,y,z = transform_coordinate_geo2earthcentered(lon[i], lat[i], alt[i])
        dist_origin.append(((x-xm)**2 + (y-ym)**2 + (z-zm)**2)**0.5)

    distance_to_origin.append(dist_origin)


    for sat in range(len(sats)):
        sats_count[folder][int(sats[sat])] = sats_count[folder][int(sats[sat])] + 1
        distance_count[folder][int(sats[sat])] = distance_count[folder][int(sats[sat])] + dist[sat]

for folder in range(len(folders)):
    satellite_distribution = np.divide(sats_count[folder], np.sum(sats_count[folder]))
    print("for", folder,
          "lat, long, alt", np.mean(latitude[folder]), np.mean(longitude[folder]), np.mean(altitude[folder]),
          "average distance to center", np.mean(distance[folder]),
          "average distance to origin", np.mean(distance_to_origin[folder]),
          "average number of visible GPS satellites for", np.mean(satellites[folder]),
          "average satellite distribtion", np.mean(satellite_distribution), np.argmax(satellite_distribution))

for folder in range(len(folders)):
    plt.plot(unixtime[folder], distance_to_origin[folder], "-", label=name[folder])
plt.title("distance to origin over time")
plt.xlabel("unixtime [s]")
plt.ylabel("distance [m]")
plt.legend()
plt.savefig('result_distance_to_origin.png')
#plt.show()
plt.clf()

for folder in range(len(folders)):
    plt.plot(unixtime[folder], distance[folder], "-", label=name[folder])
plt.title("distance to center over time")
plt.xlabel("unixtime [s]")
plt.ylabel("distance [m]")
plt.legend()
plt.savefig("result_distance_to_center.png")
#plt.show()
plt.clf()

for folder in range(len(folders)):
    satellite_distribution = np.divide(sats_count[folder], np.sum(sats_count[folder]))
    plt.plot(satellite_distribution*100.0, "o-", label=name[folder])
plt.title("distribution of visible GPS Satellites")
plt.xlabel("visible GPS satellites [-]")
plt.ylabel("distribution of GPS Satellites [%]")
plt.legend()
plt.savefig("result_distribution_of_visible_gps_satellites.png")
#plt.show()
plt.clf()

for folder in range(len(folders)):
    print(folder, sats_count[folder])
    print(folder, distance_count[folder])
    plt.plot(np.divide(distance_count[folder], sats_count[folder]), "o-", label=name[folder])
plt.title("distance to center per visible GPS satellites")
plt.xlabel("visible GPS satellites [-]")
plt.ylabel("distance/satellites [m]")
plt.legend()
plt.savefig("result_distance_to_center_per_visible_gps_satellites.png")
#plt.show()
plt.clf()


f = open("result_locotation.html", "w")

with open('template_markers.html') as fp:
    for line in fp:
        if line.find("XXXmapcenter") > -1:
            mapcenter(f, longitude[0], latitude[0])
        elif line.find("XXXlocations") > -1:
            for folder in range(len(folders)):
                markers(f, folder, origin[folder][1], origin[folder][0])
        else:
            f.write(line)

f.close()



f = open("result_gps_log.html", "w")

with open('template_markers.html') as fp:
    for line in fp:
        if line.find("XXXmapcenter") > -1:
            mapcenter(f, longitude[0], latitude[0])
        elif line.find("XXXlocations") > -1:
            for folder in range(len(folders)):
                locations(f, folder, colour[folder], longitude[folder][::2], latitude[folder][::2])
                markers(f, folder, origin[folder][1], origin[folder][0])
        else:
            f.write(line)

f.close()