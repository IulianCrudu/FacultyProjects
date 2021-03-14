class Settings:
    def __init__(self, settings_path: str = "settings.properties"):
        self._settings_data = {}
        self._read_file(settings_path)

    @property
    def settings_data(self):
        return self._settings_data

    @property
    def dim(self):
        return int(self.settings_data["DIM"])

    @property
    def apple_count(self):
        return int(self.settings_data["apple_count"])

    def _read_file(self, file_path: str):
        f = open(file_path, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            [s_property, s_value] = line.split("=", 1)
            s_property = s_property.strip()
            s_value = s_value.strip()
            self.settings_data[s_property] = s_value
