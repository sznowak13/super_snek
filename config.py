import json


class Config:
    DIRS = {
        'UP': 0,
        'RIGHT': 1,
        'DOWN': 2,
        'LEFT': 3,
    }

    COLORS = {
        'BLK': 0,
        'VLT': 201,
        'CYN': 46,
        'L_GRN': 119,
        'D_GRN': 65,
        'YLW': 227,
        'RED': 161,
        'TEAL': 73
    }

    VALID_KEYS = (
        'name',
        'level_size',
        'snake_size',
        'game_speed',
        'speed_delta',
        'points',
        'color_map'
    )

    def __init__(self, **cfg):
        assert len(cfg) == len(self.VALID_KEYS), ('Your Config has different number of attributes then it should. '
                                                  'Check your JSON file if used, or try again programmatically.')
        for k, v in cfg.items():
            if k not in self.VALID_KEYS:
                raise KeyError(
                    "Your config has invalid attribute, please remove that from your JSON file (invalid={})".format(k)
                )
            setattr(self, k, v)
        self.snake_pos = self.level_size // 2, self.level_size // 2

    @classmethod
    def from_json(cls, name: str):
        with open('./configs/{}.json'.format(name), 'r') as f:
            cfg = json.load(f)
        return Config(**cfg)

    def get_color(self, code):
        return self.COLORS[self.color_map[code]]
