class App:
    def __init__(self, name: str, version: str, author):
        self._name = None
        self._version = None
        self._author = None
        
        self.name = name
        self.version = version
        self.author = author
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название приложения должно быть строкой")
        if not value.strip():
            raise ValueError("Название приложения не может быть пустым")
        self._name = value.strip()
    
    @property
    def version(self) -> str:
        return self._version
    
    @version.setter
    def version(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Версия должна быть строкой")
        if not value.strip():
            raise ValueError("Версия не может быть пустой")
        self._version = value.strip()
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        from models.author import Author
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть экземпляром класса Author")
        self._author = value