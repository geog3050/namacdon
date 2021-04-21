import arcpy
from arcpy import env
import sys,os
from os import listdir
from os.path import isfile, join

env.overwriteOutput = True
directory = "C:/Users/Neal/OneDrive - University of Iowa/Derecho Damage Project/EO Data/EVWHS/marion"
env.workspace = directory
dataloc = "C:/Users/Neal/OneDrive - University of Iowa/Derecho Damage Project/EO Data/EVWHS/marion"

get_folders = [os.path.join(directory, f) for f in listdir(directory) if os.path.isdir(join(directory, f))]
sr = arcpy.SpatialReference(32638)

for t in get_folders:
    tif_files = [os.path.join(path,name)
        for path, subdirs, files in os.walk(t)
        for name in files
        if name.endswith(".jpg")]
    for z in tif_files:
        arcpy.DefineProjection_management(z, sr)
    desc = arcpy.Describe(tif_files[0])
    bands = desc.bandCount
    print("working",tif_files[0], bands)
    name = os.path.basename(tif_files[0])
    arcpy.MosaicToNewRaster_management(tif_files,dataloc,name+".tif",sr,"", "", bands, "","")
    print("Mosaic complete:",name)
