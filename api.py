from flask import Flask, send_from_directory, render_template, url_for
import os

import map_handling

app = Flask(__name__)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def root():
    vector_maps = map_handling.get_vector_maps()
    print(vector_maps)
    map_dirs = map_handling.get_map_dirs()
    print(map_dirs)
    map_groups = map_handling.get_map_groups()
    print(*map_groups.items(), sep="\n")
    return render_template('map_browser.html', vector_maps=vector_maps, single_maps=map_dirs, map_groups=map_groups )

@app.route("/xyzmap/<mapname>/<z>/<x>/<y>.png")
def xyzmap(mapname, z, x, y):
    if not os.path.isdir("static/slippy_maps/%s_tiles" % mapname):
        return "map %s not found!" % mapname, 404
    if not os.path.isfile("static/slippy_maps/%s_tiles/%s/%s/%s.png" % (mapname, z, x, y)):
        return "no tile at position %s,%s,%s (z,y,x)!" % (z,y,x), 404
    return send_from_directory('static', 'slippy_maps/%s_tiles/%s/%s/%s.png' % (mapname, z, x, y))

@app.route("/xyzmap/<groupname>/<mapname>/<z>/<x>/<y>.png")
def xyzmapgroup(groupname, mapname, z, x, y):
    if not os.path.isdir("static/slippy_maps/group_%s" % groupname):
        return "map group %s not found!" % groupname, 404
    if not os.path.isdir("static/slippy_maps/group_%s/%s_tiles" % (groupname, mapname)):
        return "map %s not found in group %s!" % (mapname, groupname), 404
    if not os.path.isfile("static/slippy_maps/%s_tiles/%s/%s/%s.png" % (mapname, z, x, y)):
        return "no tile at position %s,%s,%s (z,y,x)!" % (z,y,x), 404
    return send_from_directory('static', 'slippy_maps/group_%s/%s_tiles/%s/%s/%s.png' % (groupname, mapname, z, x, y))

if __name__ == '__main__':
    app.run(debug = True)