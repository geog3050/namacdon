import arcpy
from arcpy import env
import sys,os
from os import listdir
from os.path import isfile, join

env.overwriteOutput = True
directory = "C:/Users/Neal/OneDrive - University of Iowa/Derecho Damage Project/EO Data/EVWHS/new"
env.workspace = directory

dataloc = "C:/Users/Neal/Documents/ArcGIS/Projects/GEOG4580_6"
##arcpy.CreateFileGDB_management(dataloc,"testfolder.gdb")

##fclist = arcpy.List
##for fc in fclist:
##    fcdescribe = arcpy.Describe(fc)
##    if (fcdescribe.shapeType == 'Polygon'):
##        arcpy.CopyFeatures_management(fc, "C:/Users/Neal/OneDrive - University of Iowa/Fall 2020/GEOG 4580/Assignment 6/data/results/Q2.gdb/"+fcdescribe.basename)
##        print("Added",fcdescribe.basename,"to Q2.gdb")

get_folders = [os.path.join(directory, f) for f in listdir(directory) if os.path.isdir(join(directory, f))]
sr = arcpy.SpatialReference(32638)

for t in get_folders:
    tif_files = [os.path.join(path,name)
        for path, subdirs, files in os.walk(t)
        for name in files
        if name.endswith(".TIF")]
    for z in tif_files:
        arcpy.DefineProjection_management(z, sr)
##        dsc = arcpy.Describe(z)
##        coord_sys = dsc.spatialReference.name
##        print(z,coord_sys)
    desc = arcpy.Describe(tif_files[0])
    bands = desc.bandCount
    print(tif_files[0], bands)
    name = os.path.basename(tif_files[0])
    arcpy.MosaicToNewRaster_management(tif_files,dataloc,name+".tif",sr,"", "", bands, "","")
    print("Mosaiced",name)

##        htmlfiles = [os.path.join(root, name)
##             for root, dirs, files in os.walk(path)
##             for name in files
##             if name.endswith((".html", ".htm"))]

