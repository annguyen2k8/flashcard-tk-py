from pathlib import Path


class AppData:
    def __init__(self, app_name: str):
        self.base_dir = Path.home() / f".{app_name}"
        self.config = self.base_dir / "config.json"
        self.session = self.base_dir / "session.json"
        
        self.__init()

    def __init(self):
        self.base_dir.mkdir(exist_ok=True)
        self.saves.mkdir(exist_ok=True)

        if not self.config.exists():
            self.save_config({})

    def save_config(self, data: dict):
        self.config.write_text(json.dumps(data))

    def load_config(self) -> dict:
        return json.loads(self.config.read_text())
