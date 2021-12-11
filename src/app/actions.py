from collections import deque

from config import CMD_PROMPTS, OUTPUTS, YES, NO
from app.command_factory import ENTITY_DICT

class Action:
    '''Superclass for menu actions'''
    def __init__(self, io, item_service, action=None):
        self._io = io
        self._item_service = item_service

        if action is None:
            self._cmds = []
        else:
            self._cmds = CMD_PROMPTS[action]

    def perform(self):
        self._io.write(OUTPUTS['unknown command'])
        return True

    def _get_info(self, prompt, error_msg):
        """Internal method to read and write info from/to the console."""
        adding = True
        while adding:
            info = self._io.read(prompt)
            if not info:
                self._io.write(error_msg)
            else:
                adding = False
        return info

    def _list(self):
        headers = ['type', 'id', 'creator', 'title']
        items = deque(self._item_service.list_by_type_alphabetically())
        if items:
            ids = [item[1] for item in items]
            items.appendleft(headers)
            self._io.write(items, True)
        else:
            ids = []
            self._io.write(OUTPUTS["empty list"])

        return ids

    # def _list(self, str_len='long'):
    #     items = self._item_service.find_all_items()
    #     titles = []
    #     if items:
    #         for item in items:
    #             item_str = self._is_valid(item)
    #             if item_str is not None:
    #                 if str_len == 'long':
    #                     output = f"id: {item[0]}, tyyppi: {item[1].capitalize()}, tiedot: {item_str}"
    #                 else:
    #                     output = item_str.short_str
    #                 self._io.write(output)
    #                 titles.append(item_str.title)
    #     else:
    #         self._io.write(OUTPUTS["empty list"])

    #     return titles

    # def _is_valid(self, item):
    #     try:
    #         return ENTITY_DICT[item[1]](*item[2])
    #     except TypeError:
    #         return None
    #     except KeyError:
    #         return None

class Add(Action):
    '''Superclass for add actions'''
    def __init__(self, io, item_service, action):
        super().__init__(io, item_service, action)
        self._action = action

    def perform(self):
        item = []
        for cmd in self._cmds:
            item.append(self._get_info(*cmd))

        added = self._item_service.create_item(self._action, item)
        # if added == "duplicate":
        if not added:
            self._io.write(OUTPUTS["already in list"])
        else:
            self._io.write(OUTPUTS["added"])
        return True

class AddBook(Add):
    def __init__(self, io, item_service):
        super().__init__(io, item_service, 'book')

class AddBlog(Add):
    def __init__(self, io, item_service):
        super().__init__(io, item_service, 'blog')

class AddVideo(Add):
    def __init__(self, io, item_service):
        super().__init__(io, item_service, 'video')

class List(Action):
    def __init__(self, io, item_service):
        super().__init__(io, item_service)

    def perform(self):
        self._io.write(OUTPUTS['list'])
        self._list()
        return True

class Delete(Action):
    """Menu subclass for deleting an item."""
    def __init__(self, io, item_service):
        super().__init__(io, item_service, 'delete')

    def perform(self):
        self._io.write(OUTPUTS['list'])
        # items = self._list('short')
        items = self._list()

        if items:
            prompt, error_msg = self._cmds[0]
            item = self._get_info(prompt, error_msg)
            if item not in items:
                self._io.write(OUTPUTS['item not found'])
            else:
                self._delete_item(item, items)

        return True

    def _delete_item(self, item, items):
        for i in range(len(items)):
            if items[i] == item:
                self._confirm(item)

    def _confirm(self, item):
        while True:
            choice = self._io.read(OUTPUTS['confirm'])
            if choice == YES:
                self._item_service.delete_item(item)
                self._io.write(OUTPUTS['deleting'])
                return
            elif choice == NO:
                self._io.write(OUTPUTS['not deleted'])
                return

class Quit(Action):
    def __init__(self, io, item_service):
        super().__init__(io, item_service)

    def perform(self):
        self._io.write(OUTPUTS['quit'])
        return False
