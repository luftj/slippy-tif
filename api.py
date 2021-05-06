from flask import Flask,render_template

import processing

app = Flask(__name__)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def root():
    vector_maps = processing.get_vector_maps()
    print(vector_maps)
    map_dirs = processing.get_map_dirs()
    print(map_dirs)
    map_groups=processing.get_map_groups()
    print(*map_groups.items(),sep="\n")
    return render_template('map_browser.html', vector_maps=vector_maps, single_maps=map_dirs, map_groups=map_groups )

if __name__ == '__main__':
    app.run(debug = True)