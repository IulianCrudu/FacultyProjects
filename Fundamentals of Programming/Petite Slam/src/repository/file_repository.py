from .repository import Repository
from src.domain import Player


class FileRepository(Repository):
    def __init__(self, file_name, pk="id"):
        super().__init__(pk)
        self._file_name = file_name
        self._load()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            if not line:
                continue
            line = [l_part.strip() for l_part in line.split(',')]
            super().add_item(Player(line[0], line[1], int(line[2])))

    def add_item(self, item):
        result = super().add_item(item)
        # self._save()
        return result

    def delete_item(self, id_):
        result = super().delete_item(id_)
        # self._save()
        return result

    def update_strength(self, item_id, strength):
        result = super().update_strength(item_id, strength)
        # self._save()
        return result

    def _save(self):
        f = open(self._file_name, 'wt')
        for player in self._items:
            line = player.id + ';' + player.name + ';' + player.strength
            f.write(line)
            f.write('\n')
        f.close()
