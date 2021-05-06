import os
import sys
import subprocess

import json

from osgeo import gdal

from config import config

config_path = "config.json"
slippy_maps_path = "static/slippy_maps/"
file_types = [".tif"]
vector_types = [".geojson"]

def get_vector_maps():
    path = "static/vector_maps/"
    vector_map_files = os.listdir(path)
    vector_map_files = [os.path.join(path,x) for x in vector_map_files]
    vector_map_files = [x for x in vector_map_files if os.path.isfile(x) and os.path.splitext(x)[-1] in vector_types]
    return vector_map_files

def get_raster_bbox(filepath):
    # from https://gis.stackexchange.com/questions/126467/determining-if-shapefile-and-raster-overlap-in-python-using-ogr-gdal#126472
    raster = gdal.Open(filepath)

    # Get raster geometry
    transform = raster.GetGeoTransform()
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    xLeft = transform[0]
    yBottom = transform[3]
    xRight = xLeft+cols*pixelWidth
    yTop = yBottom-rows*pixelHeight

    return xLeft, yBottom, xRight, yTop

def overlap_bbox(bbox_a, bbox_b):
    # return True if two boxes are overlapping. boxes in form [minx,miny,maxx,maxy]
    a_rightof_b = bbox_a[0] > bbox_b[2]
    b_rightof_a = bbox_b[0] > bbox_a[2]

    has_x_overlap = not(a_rightof_b or b_rightof_a)

    a_topof_b = bbox_a[1] > bbox_b[3]
    b_topof_a = bbox_b[1] > bbox_a[3]

    has_y_overlap = not(a_topof_b or b_topof_a)

    return has_x_overlap and has_y_overlap

def get_map_paths():
    return config["map_paths"]

def get_map_dirs():
    map_dirs = []
    for filename in os.listdir(slippy_maps_path):
        filepath = os.path.join(slippy_maps_path, filename)
        if os.path.isdir(filepath) and not filename.startswith("group"):
            print(filepath)
            map_dirs.append(filepath)
    return map_dirs

def get_map_groups():
    groups = {}
    for filename in os.listdir(slippy_maps_path):
        filepath = os.path.join(slippy_maps_path, filename)
        if os.path.isdir(filepath) and filename.startswith("group"):
            group_name = filename.replace("group_","")
            print(filepath)
            for map_dir in os.listdir(filepath):
                if os.path.isdir(filepath):
                    if not group_name in groups:
                        groups[group_name] = []
                    groups[group_name].append(filepath+"/"+map_dir)
    return groups

def convert(input_file,name,outpath):
    gdaltilespath = 'C:/Program Files/GDAL/gdal2tiles.py'
    outdir = outpath + os.path.splitext(name)[0]+"_tiles/"
    if os.path.isdir(outdir):
        print("map %s already converted" % input_file)
        # return # already exists
    command = [sys.executable, gdaltilespath,"-x","-n","-e","--processes=2","-z","4-12","--profile","geodetic",input_file, outdir]
    print(command)
    subprocess.run(command)

def get_overlapping_maps(list_of_files):
    overlap_matrix = [[False]*len(list_of_files) for x in range(len(list_of_files))]
    
    bboxes = []
    for file in list_of_files:
        bboxes.append(get_raster_bbox(file))

    for idx1,this in enumerate(bboxes):
        for idx2,other in enumerate(bboxes):
            overlap_matrix[idx1][idx2] = overlap_bbox(this, other)
            # print(*overlap_matrix,sep="\n")

    print(*overlap_matrix,sep="\n")
    # merge
    final_sets = []
    for line in overlap_matrix:
        s = [i for i,x in enumerate(line) if x]
        # check if we have seen any element of s before
        found = False
        for el in s:
            for os in final_sets:
                if el in os:
                    #append here
                    found = True
                    print("merge",s,el)
                    for e in s:
                        os.add(e)
                    break
            if found:
                break
        if not found:
            final_sets.append(set(s))
    

    print(*final_sets, sep="\n")

def make_tiles():
    for raw_maps_path in get_map_paths():
        for filename in os.listdir(raw_maps_path):
            filepath = os.path.join(raw_maps_path,filename)
            if os.path.isfile(filepath):
                if not os.path.splitext(filename)[-1] in file_types:
                    continue # not a map

                convert(filepath, filename, slippy_maps_path)
                # # gdaltilespath = os.path.dirname(os.path.abspath(gdal2tiles.__file__))+"/gdal2tiles"
                # gdaltilespath = 'C:/Program Files/GDAL/gdal2tiles.py'
                # outdir = slippy_maps_path + os.path.splitext(filename)[0]+"_tiles/"
                # if os.path.isdir(outdir):
                #     print("map %s already converted" % filepath)
                #     continue # already exists
                # command = [sys.executable, gdaltilespath,"-z","5-15","--profile","geodetic",filepath, outdir]
                # print(command)
                # subprocess.run(command)
                # # gdal2tiles.py --profile=geodetic -z 5-15 data/raw_maps/georef_sheet_329_warp.tif data/slippy_maps/georef_sheet_329_warp
            else:
                # is a folder. possibly a set of images -> merge them?
                #from osm wiki:
                #If you want to tile multiple images, you might merge them first. A nice space-saving way is to use the gdal_vrtmerge.py example script to make a GDAL virtual raster which can then be fed to the main gdal2tiles.py program.
                #gdal_vrtmerge.py -o mosaic.vrt -i *.tif
                print(filepath)
                # gdalmergepath = 'C:/Program Files/GDAL/gdal_vrtmerge.py'
                # vrt_file = "%s_marged.vrt" % filename
                infiles = [os.path.join(filepath,f) for f in os.listdir(filepath) if os.path.splitext(f)[-1] in file_types]
                # get_overlapping_maps(infiles)
                # exit()
                # command = ["gdalbuildvrt", vrt_file, *infiles]
                # print(command)
                # subprocess.run(command)
                
                for f in infiles:
                    convert(f, os.path.basename(f), slippy_maps_path+"group_"+os.path.splitext(filename)[0]+"/")
                # gdaltilespath = 'C:/Program Files/GDAL/gdal2tiles.py'
                # outdir = slippy_maps_path + os.path.splitext(filename)[0]+"_tiles/"
                # if os.path.isdir(outdir):
                #     print("map %s already converted" % filepath)
                #     continue # already exists
                # command = [sys.executable, gdaltilespath,"-z","5-15","--profile","geodetic",vrt_file, outdir]
                # print(command)
                # subprocess.run(command)
                

if __name__ == "__main__":
    make_tiles()