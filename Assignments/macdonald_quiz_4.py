# Take a feature class and return a buffered fc based on feature type.
# There's a possible typo in the quiz question - you say 'seaplane' when
# the actual name in the FEATURES list is 'Seaplane Base'...
# I assume this isn't a trick question, even though 'other values do not create buffers'.

import arcpy

# Set the workspace and identify input/output .shp names.
arcpy.env.workspace = r"C:\Users\Neal\OneDrive - University of Iowa\Spring 2021\GEOG 5055\Quiz 4"
in_fc = "airports.shp"
out_fc = "buffer_airports.shp"

# Attempt to add a new field to hold the BUFFER distance.
# Error check and exit if it already exists.
try:
    arcpy.management.AddField(in_fc,"buffer","short")
except Exception as e:
    print(e)

# Run an Update Cursor that finds if the FEATURE is Airport or Seaplane Base,
# then adds the appropriate value to 'buffer' column.
with arcpy.da.UpdateCursor(in_fc,["FEATURE","buffer"]) as cursor:
    for row in cursor:
        if row[0] == 'Airport':
            row[1] = 15000
        elif row[0] == 'Seaplane Base': # I assume this is what you meant by 'seaplane'
            row[1] = 7500
        cursor.updateRow(row)

# Buffer each point in in_fc based on 'buffer' value, then create new fc at out_fc.
arcpy.Buffer_analysis(in_fc, out_fc, "buffer")
