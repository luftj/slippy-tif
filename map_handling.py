import os

slippy_maps_path = "static/slippy_maps/"
file_types = [".tif"]
vector_types = [".geojson"]

def get_vector_maps():
    path = "static/vector_maps/"
    vector_map_files = os.listdir(path)
    vector_map_files = [os.path.join(path,x) for x in vector_map_files]
    vector_map_files = [x for x in vector_map_files if os.path.isfile(x) and os.path.splitext(x)[-1] in vector_types]
    return vector_map_files

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