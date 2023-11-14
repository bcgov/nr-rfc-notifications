import osgeo.ogr as ogr
import pprint
import json
import os
""" simple script to extract hierarchical basin / sub-basin information from a 
shapefile and write it to a json file.  Used to inject this information into a 
chefs / forms.io form.

# useful gdal doc:
https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
"""
layer = None
ds = None

def getLayer(shape_file_path):
    """Gets the ogr layer object for the given shapefile

    :param shapeFile: the path to the shapefile to open
    :type shapeFile: str
    :return: the ogr layer object that wraps the provided shapefile path
    :rtype: _type_
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # weakness with ogr implementation, https://trac.osgeo.org/gdal/ticket/7175
    global layer, ds
    ds = driver.Open(shape_file_path, 0)
    layer = ds.GetLayer()
    return layer

def print_column_names(layer):
    """prints to stdout the column names for the given ogr layer

    :param layer: ogr layer
    :type layer: ogr.layer
    """
    print("getting column names")
    layerDefinition = layer.GetLayerDefn()
    print("here")
    cnt = layerDefinition.GetFieldCount()
    print(f"getting column name: {cnt}")

    for n in range(layerDefinition.GetFieldCount()):
        print("herer")
        fdefn = layerDefinition.GetFieldDefn(n)
        print(f"column name: {fdefn.name}")

def create_json_struct(layer, json_file_path):
    """Creates the json structure from the given ogr layer

    :param layer: input ogr layer object
    :type layer: ogr.layer
    :param json_file_path: the path to the json file to write
    :type json_file_path: str
    """
    outStruct = {}
    for feature in layer:
        basin = feature.GetField("Major_Basi")
        subbasin = feature.GetField("Sub_Basin")

        if basin not in outStruct:
            outStruct[basin] = []
        if subbasin and subbasin not in outStruct[basin]:
            outStruct[basin].append(subbasin)
    with open("json_file_path", "w") as fh:
        json.dump(outStruct, fh, indent=4)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(outStruct)





if __name__ == "__main__":
    shape_file_path = "./data/basins/Flood_Advisory_and_Warning_Notifications.shp"
    json_file_path = './data/basins.json'
    if os.path.exists(shape_file_path):
        print("file exists")

    layer = getLayer(shape_file_path)
    print(f"layer: {layer}")
    print_column_names(layer)
    create_json_struct(layer, json_file_path)



