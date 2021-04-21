import sys, os
import re
import arcpy
import shutil

arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.addOutputsToMap = False
arcpy.env.overwriteOutput = True
arcpy.env.processorType = "GPU"
default_extent = "649947.8909 4410578.6392 714505.2748 4475136.0231"

def preprocess(in_folder,clip_selector=False,clipping_extent=default_extent,bands=[4,3,2]):
    '''Function to preprocess imagery from larger files into PNGs for use in deep learning models'''

    # Gather all rasters in input folder, and sort by name
    arcpy.env.workspace = in_folder
    rasters = arcpy.ListRasters()
    rasters.sort()

    holding_folder=os.path.join(in_folder,'delete')
    try: os.mkdir(holding_folder)
    except FileExistsError: print(f"{holding_folder} already exists.")
    output_folder=os.path.join(in_folder,'output')
    print(f"Output folder at {output_folder}")
    try: os.mkdir(output_folder)
    except FileExistsError: print(f"{output_folder} already exists.")
    
    for raster in rasters:
        desc = arcpy.Describe(raster)
        print(f"Working on {desc.baseName}")
        
        # Regular expression to identify year value
        year_search = re.search(r'\d\d\d\d',desc.baseName)
        year = year_search.group()

        # If no year value present, print error and continue for loop
        if year == None:
            print('No year value found in name, skipping.')
            continue

        # If year is present, execute following steps:
        else:
            
            # Create scratch folder to hold working files
            
            try: temp = arcpy.management.CreateFolder(holding_folder,f'delete_{desc.baseName}')
            except FileExistsError: print(f"{temp} already exists.")
            
            try:
                # Move raster into file geodatabase to enable GDB operations
                arcpy.RasterToGeodatabase_conversion(raster,temp)
                print(temp)
                print(f"Raster {desc.baseName} to Feature Layer")
                
                temp_folder = str(temp)
                arcpy.env.workspace = temp_folder
                raster_gdb = desc.baseName
                
                # Clip if necessary, and rename file to shorten length
                clipped_name = f"cr_{year}"
                if clip_selector == True:
                    arcpy.management.Clip(raster_gdb, clipping_extent, clipped_name)
                    print(f"Clipped {clipped_name}")
                else:
                    arcpy.management.Rename(raster_gdb, clipped_name)
                    print(f"Renamed {clipped_name}")

                # Create a three-band PNG composite for deep learning
                composite_name = f"cmp_{year}.png"
                arcpy.management.MakeRasterLayer(clipped_name, composite_name,
                                                 "", "", f"{bands[0]};{bands[1]};{bands[2]}")
                arcpy.management.CopyRaster(composite_name, os.path.join(output_folder, composite_name),
                    '',None, "3.4e+38", "NONE", "NONE", '16_BIT_UNSIGNED', "NONE",
                    "NONE", "PNG", "NONE", "CURRENT_SLICE", "NO_TRANSPOSE")
                print(f"Composite PNG for {composite_name} complete.")
        
            except Exception as e:
                print(e)
                
            finally:
                arcpy.env.workspace = in_folder
                # Delete scratch folder to save space 
                try: arcpy.management.Delete(temp)
                except Exception as e: pass
                try: shutil.rmtree(temp_folder)
                except Exception as e: pass               
