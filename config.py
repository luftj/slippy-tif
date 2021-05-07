import json

config_path = "config.json"

class Config:
    def __init__(self):
        self.load_config()

    def load_config(self):
        print("loading config at",config_path)
        with open(config_path) as fr:
            self.data = json.load(fr)

    def get(self, val):
        self.load_config()
        return self.data[val]

config = Config()

def load_config():
    print("loading config at",config_path)
    with open(config_path) as fr:
        return json.load(fr)

if __name__ == "__main__":
    from time import sleep
    while True:
        sleep(5)
        print("update tiles...")
        config.load_config()