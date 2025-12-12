class Author:
    def __init__(self, name: str, group: str):
        self._name = None
        self._group = None
        self.name = name
        self.group = group
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()
    
    @property
    def group(self) -> str:
        return self._group
    
    @group.setter
    def group(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой")
        if not value.strip():
            raise ValueError("Группа не может быть пустой")
        self._group = value.strip()