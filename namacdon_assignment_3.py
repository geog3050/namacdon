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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    
    '''
    This function takes a workspace as an input then prints the name and type
    type of each feature class in the format: 'states is a point feature class'.
    '''
    
    if arcpy.Exists(workspace): # checks if this is a valid workspace
        arcpy.env.workspace = workspace
        fclist = arcpy.ListFeatureClasses() # gets list of all FCs in the workspace
        for fc in fclist: # iterates through each fc
            desc = arcpy.da.Describe(fc) # creates a description variable of the fc
            print("{} is a {} feature class".format(desc["baseName"],desc["shapeType"]))
    else:
        print("Invalid workspace")

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):

    '''
    This function takes a feature class as an input, then prints all of the attribute
    names and its data type, but only if it is a numerical data type.
    '''
    
    if arcpy.Exists(workspace): # checks if this is a valid workspace
        arcpy.env.workspace = workspace
        try:
            fieldlist = arcpy.ListFields(inputFc) # attempts to list fields
            for field in fieldlist: # iterates through fields
                if field.type in ["Integer","Double","Float","SmallInteger","Single"]:
                    print("{} is a {} feature class".format(field.name,field.type))
        except Exception as e: # catches exceptions for things like the input not existing
            print("Error: ",e)
    else:
        print("Invalid worspace")

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

######################################################################
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):

    '''
    This function takes an input database and a shape type, then moves only feature classes
    of the set type to an output_geodatabase, creating one if necessary.
    This function would benefit from being designed with a "workspace" parameter.
    It is otherwise ambiguous as to if each GDB parameter is a full path or name only,
    as well as creating issues based on if the script is run in the same folder as the inputs
    or if imported as a module. I've added code to defensively check this, but a workspace
    parameter would solve the ambiguity as to param types.
    '''
     
    # Check if there is already a database at output_geodatabase path location,
    # then allows the user to authorize an overwrite if needed
    if arcpy.Exists(output_geodatabase) or \
        arcpy.Exists(os.path.dirname(output_geodatabase)) or \
        arcpy.Exists(os.path.dirname(input_geodatabase)):
        print("Database {} already exists".format(output_geodatabase))
        question = input("Overwrite {}? (y/n)".format(output_geodatabase)).lower()
        if question == "y":
            arcpy.Delete_management(output_geodatabase)
            print("Overwriting database and executing copy function")
        else: 
            sys.exit("Database not overwritten")
  
    # Determine if the input GDBs are full paths or just basenames,
    # then assign workspace and dbnames as needed
    if output_geodatabase.count(':') > 0:
        workspace = os.path.dirname(output_geodatabase) # use output_geodatabase path from param
    elif input_geodatabase.count(':') > 0:
        workspace = os.path.dirname(input_geodatabase) # get path from input_geodatabase
    else: 
        workspace = os.getcwd() # use the current project/python working directory as path

    # Create new GDB in location as specified from last if...else loop
    outGDB = arcpy.management.CreateFileGDB(workspace,os.path.basename(output_geodatabase))
    
    arcpy.env.workspace = input_geodatabase
    # Get features from input_geodatabase and add to output_geodatabase
    fclist = arcpy.ListFeatureClasses(feature_type = shapeType)
    for fc in fclist:
        arcpy.FeatureClassToFeatureClass_conversion(fc,outGDB,fc+".shp")
        print("Added {} to new GDB, a {} feature class".format(fc,shapeType))
###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

######################################################################
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    
    '''
    This function takes a feature class and a table, joins them based on field selection params,
    then prints how many attributes were merged and how many remained unchanged.
    '''
    
    arcpy.env.workspace = workspace

    # Create join, copy to new fc, and remove join from inputFc
    joined_fc_table = arcpy.management.AddJoin(inputFc, idFieldInputFc, inputTable, idFieldTable,"KEEP_COMMON")
    arcpy.CopyFeatures_management(joined_fc_table,"new_fc")
    arcpy.RemoveJoin_management(inputFc)

    # get number of records in original and new FC, then print matched/unmatched
    old_len = arcpy.GetCount_management(inputFc)
    new_len = arcpy.GetCount_management("new_fc")
    print("{} records matched".format(new_len))
    print("{} records unmatched".format(int(old_len[0])-int(new_len[0])))    

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
