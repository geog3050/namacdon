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
import re
arcpy.env.overwriteOutput = True

###################################################################### 
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    '''Function to deterimine distance from point to nearest polyline location.
        Name of nearest polyline is in NEAR_FID field and distance in NEAR_DIST'''
    
    if arcpy.Exists(input_geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = input_geodatabase # Set workspace to input_geodatabase
        if arcpy.Exists(fcPoint) and arcpy.Exists(fcPolyline):
            try: # Find nearest polyline (returns new columns of name and distance to nearest FC)
                arcpy.analysis.Near(fcPoint,fcPolyline)
                desc_fcPoint = arcpy.Describe(fcPoint)
                desc_fcPolyline = arcpy.Describe(fcPolyline)
                print("Calculated distance of {} to nearest location on {} in units: {}"\
                      .format(desc_fcPoint.baseName,
                              desc_fcPolyline.baseName,
                              desc_fcPoint.SpatialReference.linearUnitName))
            except Exception as e: # Catch errors in the Near calculation
                print("Error ", e)
                sys.exit(1)
        else: # Print statement if input features are invalid
            print("Feature classses do not exist, check input feature classes")
            sys.exit(1)
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1)
######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    '''This function counts the number of point features of a given type within a polygon 
        and returns the count of features in a new field in the polygon'''

    if arcpy.Exists(input_geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = input_geodatabase # Set workspace to input_geodatabase
        if arcpy.Exists(fcPoint) and arcpy.Exists(fcPolygon):
            try:
                # Create new field to hold count of features
                count_field = arcpy.ValidateFieldName("Pnt_count",os.path.dirname(fcPolygon))
                arcpy.management.AddField(fcPolygon, count_field, "SHORT")
                
                # Filter and spatially join only the features that meet the pointFieldName criteria
                where_clause = f"{pointFieldName} LIKE '%{pointFieldValue}%'"
                selection = arcpy.management.SelectLayerByAttribute(fcPoint, "NEW_SELECTION", where_clause)
                arcpy.analysis.SpatialJoin(fcPolygon, selection, "outfc","","","","CONTAINS")
                                
                # Update the pnt_count field with the count of elements that joined in the spatial join
                with arcpy.da.UpdateCursor(fcPolygon, ["FIPS",count_field]) as up_curs:
                    for urow in up_curs:
                        with arcpy.da.SearchCursor("outfc", ["FIPS","Join_Count"]) as search_curs:
                            for srow in search_curs:
                                if urow[0] == srow[0]:
                                    urow[1] = srow[1]
                        up_curs.updateRow(urow)
                print("Added field counting {} numbers in {}".format(pointFieldValue,arcpy.Describe(fcPolygon).baseName))

                # Delete the holding outfc
                arcpy.management.Delete("outfc")
                    
            except Exception as e: # Catch errors in the field manipulation calculations
                print("Error in code execution", e)
                sys.exit(1)
        else: # Print statement if input features are invalid
            print("Feature classses do not exist, check input feature classes")
            sys.exit(1)
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1)
######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    '''Function to count the unique attributes in a point feature class field and append
        them as new fields in the polygon feature class, with the values set to the count
        of features, by type, in each particular polygon feature'''
    
    if arcpy.Exists(workspace): # Check if input workspace is valid
        arcpy.env.workspace = workspace # Set workspace to workspace
        if arcpy.Exists(fcPoint) and arcpy.Exists(fcPolygon):
            try:
                
                # Gather unique names for features in the point FC
                features_set = set([row[0] for row in arcpy.da.SearchCursor(fcPoint,[pointFieldName])])
                
                # Iterate through each unique attribute
                for feature in features_set:
                    
                    # Add field to fcPolygon for attribute
                    new_field = arcpy.ValidateFieldName("{}"\
                                    .format(re.sub(r'\W+',"",feature[:13])),os.path.dirname(fcPolygon))
                    arcpy.management.AddField(fcPolygon, new_field, "SHORT")
                
                    # Filter and spatially join only the features that meet the pointFieldName criteria
                    where_clause = f"{pointFieldName} LIKE '%{feature}%'"
                    selection = arcpy.management.SelectLayerByAttribute(fcPoint, "NEW_SELECTION", where_clause)
                    arcpy.analysis.SpatialJoin(fcPolygon, selection, "outfc","","","","CONTAINS")
                    
                    # Update the pnt_count field with the count of elements that joined in the spatial join
                    with arcpy.da.UpdateCursor(fcPolygon, ["FIPS",new_field]) as up_curs:
                        for urow in up_curs:
                            with arcpy.da.SearchCursor("outfc", ["FIPS","Join_Count"]) as search_curs:
                                for srow in search_curs:
                                    if urow[0] == srow[0]:
                                        urow[1] = srow[1]
                            up_curs.updateRow(urow)

                    # Delete the holding outfc
                    arcpy.management.Delete("outfc")
                    print("Added field counting {} in {}".format(feature,arcpy.Describe(fcPolygon).baseName))
                    
            except Exception as e: # Catch errors in the field manipulation calculations
                print("Error in code execution", e)
                sys.exit(1)
        else: # Print statement if input features are invalid
            print("Feature classses do not exist, check input feature classes")
            sys.exit(1)
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct workspace input")
        sys.exit(1)
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
