class SelectionItem(object):
    def __init__(self, title: str, description: str):
        self._title = title
        self._description = description

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description
