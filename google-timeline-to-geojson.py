import ijson
from datetime import datetime
import json

filename = "{Your filename}"
filename_output = "{Your output filename}.geojson"

# Function to parse the latitude, longitude, and timestamp
def parse_lat_lng_time(lat_lng_str, time_str):
    lat, lng = lat_lng_str.replace('°', '').split(',')
    # Convert the time string to a datetime object
    time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return float(lat), float(lng), time

# Initialize the GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Open the JSON file and parse it iteratively
with open(filename, 'rb') as file:
    # Parse the JSON file for the 'semanticSegments' array
    semantic_segments = ijson.items(file, 'semanticSegments.item')
    for segment in semantic_segments:
        # Check if 'timelinePath' is in the segment
        if 'timelinePath' in segment:
            for point in segment['timelinePath']:
                # Parse the latitude, longitude, and timestamp from the 'point' string
                lat, lng, time = parse_lat_lng_time(point['point'], point['time'])
                # Create a GeoJSON feature
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lng, lat]
                    },
                    "properties": {
                        "timestamp": time.isoformat() + 'Z'
                    }
                }
                # Add the feature to the GeoJSON structure
                geojson['features'].append(feature)

# Save the GeoJSON to a file
with open(filename_output, 'w') as outfile:
    json.dump(geojson, outfile)

print("GeoJSON file created successfully!")
