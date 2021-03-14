class RepositoryException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Repository:
    def __init__(self, pk):
        self._items = []
        self._pk = pk

    def get(self, key):
        """
        Returns the item from the list with the primary_key=key
        :param key: The pk value of the needed item
        :return: The found item
        :raises:
            RepositoryException - if there is no item with that pk
        """
        found_item = [i for i in self.items if getattr(i, self.pk) == key]
        if not found_item:
            raise RepositoryException(f"Item(pk={key}) not found.")
        return found_item[0]

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self):
        return len(self.items)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def pk(self):
        return self._pk

    def add_item(self, item):
        """
        Adds a new item to the listX
        :param item: The item to be added
        :return: None
        """
        self.items.append(item)

    def update_strength(self, item_id: str, strength):
        item = self.get(item_id)
        item._strength = strength

    def delete_item(self, item_id: str):
        """
        Deletes an item from the list
        :param item_id: The primary_key value of the item to delete
        :return: None
        """
        deleted_item = self.get(item_id)
        new_item_list = [item for item in self.items if getattr(item, self.pk) != item_id]
        self.items = new_item_list
        return deleted_item
