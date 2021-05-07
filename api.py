from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug = True)