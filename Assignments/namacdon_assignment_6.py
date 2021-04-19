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
import sys
arcpy.env.overwriteOutput = True

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
        
    if arcpy.Exists(geodatabase): # Check if input workspace is valid
        arcpy.env.workspace = geodatabase # Set workspace to input_geodatabase
        try:
            # Get description of csv to retrieve name of file
            desc = arcpy.Describe(csvFile)
                      
            # Read file to table, naming it based on the description value
            arcpy.management.CopyRows(csvFile,f"table_{desc.baseName}")
            print(f"Created table_{desc.baseName} in GDB.")
            
        except AttributeError:
            print("CSV File does not exist")
        
        # Catch other errors
        except Exception as e:
            print(e)
    
    else: # Print statement if input workspace is invalid
        print("Workspace does not exist, correct input_geodatabase")
        sys.exit(1) 

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    
    # Check if input workspace is valid
    if arcpy.Exists(workspace): 
        arcpy.env.workspace = workspace # Set workspace to workspace
       
    else: # Print statement if input workspace is invalid
        print(f"Workspace {workspace} does not exist.")
        sys.exit(1) 
    
    # Check if the clipping feature exists, and set the coordinate system to its SR
    if arcpy.Exists(inClipFc):
        desc_clip = arcpy.Describe(inClipFc)
        arcpy.env.outputCoordinateSystem = desc_clip.spatialReference
        print("Spatial Reference set to",desc_clip.spatialReference.name)
    else:
        print(f"Error, {inClipFc} does not exist or is not supported.")
        sys.exit(1)
        
    # Check if the table file exists, and confirm it is a table
    if arcpy.Exists(inTable) and arcpy.Describe(inTable).dataType in ['Table','TableView']:
        
        # Create a feature layer using the Lat/Lon values from the inTable
        try:
            table_name = arcpy.Describe(inTable).baseName
            print(f'Creating feature layer for {table_name}')
            arcpy.management.XYTableToPoint(inTable,f'layer_{table_name}',xField, yField)
        except Exception as e:
            print(e)
    else:
        print(f"Error, {inTable} does not exist or is not supported.")
        sys.exit(1)
    
    # Verify the Spatial Analyst license is available
    if arcpy.CheckExtension('Spatial') == 'Available':
        try:
            # Set the parameters for the Ordinary Kriging Model
            print('Executing Kriging')
            kriging_model = arcpy.sa.KrigingModelOrdinary("CIRCULAR", 0.08,0.62,15,0)

            # Perform kriging using the parameters
            # By saving it to a variable, there is no file that has to be deleted later
            krig = arcpy.sa.Kriging(f'layer_{table_name}',valueField,kriging_model)
            print('Kriging complete, now clipping...')
            # Determine the output extent of the clipping feature
            extent = str(arcpy.Describe(inClipFc).extent)

            # Clip the kriging to the shape of Iowa
            out_name = f"krig_clipped_{table_name}"
            arcpy.management.Clip(krig, extent,out_name,
                                  inClipFc, "3.4e+38", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
            print(f'Operation complete, file saved as {out_name}')
        except Exception as e:
            print(e)
    else:
        print('Error with Spatial Analyst license.')

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
