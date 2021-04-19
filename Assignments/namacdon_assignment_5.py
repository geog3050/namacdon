###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Neal MacDonald", "namacdon"])

import arcpy
import sys, os

###################################################################### 
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute,geodatabase = "assignment2.gdb"):    
    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = geodatabase # Set workspace to input_geodatabase
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1)
    
    try:

        desc = arcpy.Describe(fcpolygon) # Describe the fcpolygon for multiple uses
        if desc.spatialReference.type == "Projected": # Check CRS type

            if desc.shapeType == 'Polygon': 

                fields = [field.name for field in arcpy.ListFields(fcpolygon)]
                if attribute in fields:
                    # Add a field for area in square miles
                    arcpy.management.AddGeometryAttributes(fcpolygon,'AREA',"",'SQUARE_MILES_US')

                    # Add an empty field for density by sqm
                    new_field = arcpy.ValidateFieldName("density_sqm",os.path.dirname(fcpolygon))
                    arcpy.management.AddField(fcpolygon,new_field,"DOUBLE")
                    print('Added field ', new_field)

                    # Divide the attribute by the area to get density
                    arcpy.management.CalculateField(fcpolygon,new_field,f"!{attribute}!/!POLY_AREA!")
                    print('Density calculated')

                else: # Raise error if not projected CRS
                    print('Invalid attribute name')
                    sys.exit(1)
            else:
                print(f"Incorrect shape type, {fcpolygon} is a {desc.shapeType}")
        else:
            print(f"{desc.baseName} is not in a projected CRS")
            sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase):
 
    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = geodatabase # Set workspace to input_geodatabase
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1)
        
    try:
        desc_line = arcpy.Describe(fcLine)
        desc_poly = arcpy.Describe(fcClipPolygon)

        if desc_line.shapeType in ['Line','Polyline'] and desc_poly.shapeType == 'Polygon':
            pass
        else:
            print("Input feature classes are not correct types")
            sys.exit(1)

        fields = [field.name for field in arcpy.ListFields(fcClipPolygon)]
        if polygonIDFieldName in fields:
            features = []
            with arcpy.da.SearchCursor(fcClipPolygon,[polygonIDFieldName]) as cursor:
                for row in cursor:
                    features.append(row[0])
            if clipPolygonID not in features:
                print(f"{clipPolygonID} does not exist in {polygonIDFieldName}")
                sys.exit(1)
            else:
                print('Field is valid, processing...')
        else:
            print(f"{polygonIDFieldName} is not in {fcClipPolygon}")
            sys.exit(1)

        try:
            if desc_line.spatialReference.name != desc_poly.spatialReference.name:
                arcpy.Project_management(fcClipPolygon,"clip_proj",desc_line.SpatialReference)
                fcClipPolygon = "clip_proj"
        except Exception as e:
            print(e)
        finally:
            arcpy.analysis.Select(fcClipPolygon, "selection", f"{polygonIDFieldName} = '{clipPolygonID}'")
            arcpy.analysis.Clip(fcLine,"selection","clipped_lines")
            arcpy.management.AddGeometryAttributes("clipped_lines",'LENGTH_GEODESIC','MILES_US')
            arcpy.management.Delete("selection")
            print('Calculated clipped lengths.')
    except Exception as e:
        print(e)
######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):
     
    arcpy.env.overwriteOutput = True
    
    if arcpy.Exists(geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = geodatabase # Set workspace to input_geodatabase
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1)
        
    # Add field to fcPoint
    try:
        new_field = arcpy.ValidateFieldName("count",os.path.dirname(fcPoint))
        arcpy.management.AddField(fcPoint,new_field,"DOUBLE")
        print('Adding field ',new_field)
    except Exception as e:
        print(e, "Error adding field to fcPoint")
        sys.exit(1)
        
    # Update cursor
    try:
        desc = arcpy.Describe(fcPoint)
        if desc.spatialReference.type == 'Geographic':
            distance_type = "WITHIN_A_DISTANCE_GEODESIC"
            print('Calculating Geometric Distance...')
        else: 
            distance_type = "WITHIN_A_DISTANCE"
            print("Calculating Euclidian distance...")
        with arcpy.da.UpdateCursor(fcPoint,["OBJECTID",new_field]) as cursor:
            for row in cursor:
                arcpy.management.SelectLayerByAttribute(fcPoint,"NEW_SELECTION",f"OBJECTID = {row[0]}")
                arcpy.management.SelectLayerByLocation(fcPoint, distance_type, 
                                        fcPoint, f"{distance} {distanceUnit}", "NEW_SELECTION")
                count = arcpy.management.GetCount(fcPoint)
                row[1] = count[0]
                cursor.updateRow(row)
        print('Processing Complete')
    except Exception as e:
        print(e, "Error with selection operation.")
        sys.exit(1)

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
