import json

config_path = "config.json"

config = {}

def load_config():
    with open(config_path) as fr:
        global config
        config = json.load(fr)

config = load_config()

if __name__ == "__main__":
    from time import sleep
    while True:
        sleep(5)
        load_config()