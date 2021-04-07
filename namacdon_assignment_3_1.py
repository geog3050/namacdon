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

###################################################################### 
# Problem 1 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the number of feature classes by each shape type. For example,
# polygon: 3, polyline: 2, point: 4

###################################################################### 
import arcpy
import sys
arcpy.env.overwriteOutput = True


def printNumberOfFeatureClassesByShapeType(workspace):
    '''This function gathers all of the Feature Classes in a workspace,
       then returns the number of objects grouped by feature type.'''
    
    arcpy.env.workspace = workspace #Set workspace from input

    # Create list of feature classes in the workspace
    fc_list = arcpy.ListFeatureClasses()

    # If the list is empty, return error message and exit
    if fc_list == None: 
        print("No feature classes in in workspace")
        sys.exit(1)

    # Iterate through the fc list and gather shape types       
    output = [] # Empty list for holding
    try:
        
        for feature in fc_list:
            desc = arcpy.Describe(feature)
            output.append(desc.shapeType)
            
        for type in set(output): #Creates set of unique types
            print("{}:".format(type), output.count(type))

    except Exception as e:
        print("Error found", e)

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the feature classes in a workspace, and
# prints the coordinate systems for each file

###################################################################### 
def printCoordinateSystems(workspace):
    '''This function gathers all of the Feature Classes in a workspace,
    then prints information about the coordinate system for each.'''

    arcpy.env.workspace = workspace  #Set workspace from input

    # If the list is empty, return error message and exit
    fc_list = arcpy.ListFeatureClasses()
    if fc_list == None: 
        print("No feature classes in in workspace")
        sys.exit(1)
        
    # Iterate through fc_list and print CRS name and type
    try:
        for feature in fc_list:
            desc = arcpy.Describe(feature)
            print(desc.basename,"is in the",
                  desc.spatialReference.name,"CRS, which is a",
                  desc.spatialReference.type, "system.")
            
    except Exception as e:
        print("Error found", e)

###################################################################### 
# Problem 3 (60 Points)
#
# Given two feature classes in a workspace:
# check whether their coordinate systems are
# the same, and if not convert the projection of one of them to the other.
# If one of them has a geographic coordinate system (GCS) and the other has
# a projected coordinate system (PCS), then convert the GCS to PCS. 

###################################################################### 
def autoConvertProjections(fc1, fc2, workspace):
    '''This function compares the CRS for two feature classes,
       then reprojects if one is a GCS and the other a PCS.
       If reprojection is needed, returns new file in workspace.'''
    
    try:
        arcpy.env.workspace = workspace #Set workspace from input
        if arcpy.ListFeatureClasses() == None:
            raise ValueError
    except ValueError:
        print("Workspace does not exist or has no Feature Classes.")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
        
    try:
        fc1_ref = arcpy.Describe(fc1)
        fc2_ref = arcpy.Describe(fc2)
    except Exception as e:
        print("Error, please enter two valid Feature Classes\n Error:",e)
        sys.exit(1)
        
    try:
        # If both systems are already projected, print statement and finish
        if fc1_ref.spatialReference.type == 'Projected' and fc2_ref.spatialReference.type == 'Projected':
            print("Both feature classes are already in a projected CRS, no reprojection needed.")

        # If one is a GCS and the other a PCS, repoject the GCS to the PCS
        elif fc1_ref.spatialReference.type == 'Geographic' and fc2_ref.spatialReference.type == 'Projected':
            print("Converting {} to {}".format(fc1_ref.name,fc2_ref.spatialReference.name))
            arcpy.management.Project(fc1, "{}_reprojected".format(fc1_ref.name), fc2_ref.spatialReference)
            print("New feature class {}_reprojected created.".format(fc1_ref.name))
        elif fc1_ref.spatialReference.type == 'Projected' and fc2_ref.spatialReference.type == 'Geographic':
            print("Converting {} to {}".format(fc2_ref.name,fc1_ref.spatialReference.name))
            arcpy.management.Project(fc2, "{}_reprojected".format(fc2_ref.name), fc1_ref.spatialReference)
            print("New feature class {}_reprojected created.".format(fc2_ref.name))
            
        # If both are in GCS, print message and finish
        else:
            print("Both feature classes are in a Geographic CRS.")
    except Exception as e:
        print(e)


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
