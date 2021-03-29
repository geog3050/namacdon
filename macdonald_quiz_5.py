def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2):
    '''Function to calculate the percentage of the area of the first polygon features 
    (fcPolygonA ) in the second polygon features (fcPolygonB), and append the percentage 
    of park area into a new field in the block groups feature class'''
    
    import arcpy
    import sys, os
    arcpy.env.overwriteOutput = True
    
    
    # Check if workspace exists, and if so, set as current workspace
    if arcpy.Exists(input_geodatabase):
        arcpy.env.workspace = input_geodatabase
    else:
        print("Invalid Workspace")
        sys.exit(1)

    # Check if feature classes exist
    if arcpy.Exists(fcPolygon1) and arcpy.Exists(fcPolygon2):
        try:
            # Create new field to hold percentage of areas
            newfield = arcpy.ValidateFieldName("Area_Pct",os.path.dirname(fcPolygon2))
            arcpy.management.AddField(fcPolygon2, newfield, "DOUBLE")
            
            # Create temporary table to hold intersection values and Tabulate Intsersection
            newtable = arcpy.ValidateTableName("out_table",os.path.dirname(fcPolygon2))
            descfc2 = arcpy.Describe(fcPolygon2) # Describe fcPolygon2 for field names
            arcpy.analysis.TabulateIntersection(fcPolygon2, descfc2.OIDFieldName, fcPolygon1, 
                                                newtable, sum_fields = descfc2.areaFieldName)
            
            # Run UpdateCursor through each field in fcPolygon2, checking for value in intsersection table
            print("Calculating percentages")
            with arcpy.da.UpdateCursor(fcPolygon2, ["OID@", "Area_Pct"]) as cursor:
                for row in cursor:
                    row[1] = 0 # Set initial percentage to zero for each row
                    for entry in arcpy.da.SearchCursor("out_table",["OBJECTID_1","PERCENTAGE"]):
                        if row[0] == entry[0]: # If the OIDs match between tables
                                row[1] += entry[1] # Add the percentage to the Area_Pct field
                    cursor.updateRow(row)
                    
            # Delete temporary table
            arcpy.management.Delete(newtable)
            print("Script complete, percentages added to {}".format(descfc2.baseName))
            
        except Exception as e:
            print(e)
    else:
        print("Invalid feature classes")
        sys.exit(1)    
