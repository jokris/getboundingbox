import sys
import json
import urllib

# function that returns true if more than half of a box's area is within bounds
def halfWithin(box, bounds):
    boxArea = (abs(box[1][1]-box[0][1]) * abs(box[2][0]-box[0][0]))
    #box = #"type": "Polygon", "coordinates": [[[-79.76259, 40.477383], [-79.76259, 45.015851], [-71.777492, 45.015851], [-71.777492, 40.477383]]]
    #(45 - 40) * (-71 - -79)
    XA1 = box[0][1]
    XA2 = box[1][1]
    YA1 = box[0][0]
    YA2 = box[2][0]
    
    boundsArea = (abs(bounds[3]-bounds[1]) * abs(bounds[2]-bounds[0]))
    #bounds = #coords=[-78.5401367286,42.00027541,-76.18272114,43.3301514]
    #(43 - 42) * (-76 - -78)
    XB1 = bounds[1]
    XB2 = bounds[3]
    YB1 = bounds[0]
    YB2 = bounds[2]
    
    ratio = 0.0
    intersectionArea = max(0, min(XA2, XB2) - max(XA1, XB1)) * max(0, min(YA2, YB2) - max(YA1, YB1))
    ratio = intersectionArea/float(boxArea)
    #print "    bounds " + str(boundsArea)
    #print "box " + str(boxArea)
    #print "inter " + str(intersectionArea)
    #print "rat " + str(ratio)
    if ratio < 0.5:
        return False
    return True

# filter 1 and 2 (geotag and place field)
def hasBadLocation(json_data): 
    # geotag filter (BOUNDING BOX) (monroe)
    
    # coordinate from input (here is Greater Rochester)
    coords = [-78.50480611, 42.00012444, -76.07799052, 43.36077324]
    if json_data["coordinates"] is not None:
        coord=json_data["coordinates"]["coordinates"]
        # coords = coordinates": [-74.084772, 42.965323]
        #geotag is inside bounding box
        if not (coord[0]>coords[2] or coord[0]<coords[0] or coord[1]>coords[3] or coord[1]<coords[1]): 
            return False
    
    # place filter (POINT OR POLYGON)
    if not json_data["place"]== None:
        if json_data["place"]["bounding_box"]["type"].lower()=="point":
            coord=json_data["place"]["bounding_box"]["coordinates"]
            #coordinate (Mid point of place bounding box) is inside filter bounds
            if not (coord[0]>coords[2] or (coord[0]<coords[0] or (coord[1]>coords[3] or coord[1]<coords[1]))):
                return False
        elif json_data["place"]["bounding_box"]["type"].lower()=="polygon":
            #"type": "Polygon", "coordinates": [[[-79.76259, 40.477383], [-79.76259, 45.015851], [-71.777492, 45.015851], [-71.777492, 40.477383]]]}
            #"type": "Polygon", "coordinates": [[[-80.519851, 39.719801], [-80.519851, 42.516072], [-74.689517, 42.516072], [-74.689517, 39.719801]]]}
            
            '''Jack's approach
            save = 0
            for thing in json_data["place"]["bounding_box"]["coordinates"]:
                for coord in thing:
                    #point is not inside bounding box
                    if (coord[0]>coords[2] or (coord[0]<coords[0] or (coord[1]>coords[3] or coord[1]<coords[1]))):
                        save=save+1
            if save > 0:
                return False
            '''
            #extra [] here for some reason
            for noextra in json_data["place"]["bounding_box"]["coordinates"]:
                box = noextra
                #print box
                # if half of place is within our bounds
                if (halfWithin(box, coords)):
                    return False
    return True

input=sys.argv[1]
output = sys.argv[2]
locations = []

data = {}
good = 0
bad = 0
with open(input, 'r') as reader:
    for line in reader:
    
        json_line=json.loads(line)
        if (hasBadLocation(json_line)):
            profile = json_line['user']
            locations.append(profile['location'])
            bad = bad + 1
            #For Acessing the google Place API
            #credentials = []
                
            #location = profile['location']
            #locString = locations[-1] #+ " NY"
            #url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+locString+"&sensor=false&key=AIzaSyAmLISNSH9wHzdmWiCNMOP-tgY4O1Jie-M"
            #response = urllib.urlopen(url);
            #jsonResult = json.loads(response.read())
            #print jsonResult
            #for i in jsonResult['results']:
            #        data[locString] = i['geometry']['viewport']
        else:
            good = good + 1

#print good
#print bad

i = 0
for entry in locations:
    try:
        if entry != '':
            print str(i) + ":", entry
            i += 1
    except:
        pass


