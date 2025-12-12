class User:
    def __init__(self, id: int, name: str):
        self._id = None
        self._name = None
        
        self.id = id
        self.name = name
        self.subscribed_currencies = []
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID должен быть целым числом")
        if value <= 0:
            raise ValueError("ID должен быть положительным числом")
        self._id = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Имя пользователя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self._name = value.strip()
    
    def subscribe_to_currency(self, currency):
        if currency not in self.subscribed_currencies:
            self.subscribed_currencies.append(currency)