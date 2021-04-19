import sys,os

folder_location = "C:/Users/Neal/OneDrive - University of Iowa/Derecho Damage Project/EO Data/EVWHS/New"

tif_files = [os.path.join(path,name)
    for path, subdirs, files in os.walk(folder_location)
    for name in files
    if name.endswith(".TIF")]
print(tif_files)

##        htmlfiles = [os.path.join(root, name)
##             for root, dirs, files in os.walk(path)
##             for name in files
##             if name.endswith((".html", ".htm"))]

