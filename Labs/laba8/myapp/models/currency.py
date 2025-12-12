class Currency:
    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self._id = None
        self._num_code = None
        self._char_code = None
        self._name = None
        self._value = None
        self._nominal = None
        
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal
        self.history = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ID валюты должен быть строкой")
        if not value.strip():
            raise ValueError("ID валюты не может быть пустым")
        self._id = value.strip()
    
    @property
    def num_code(self) -> str:
        return self._num_code
    
    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Цифровой код должен быть строкой")
        if not value.strip():
            raise ValueError("Цифровой код не может быть пустым")
        self._num_code = value.strip()
    
    @property
    def char_code(self) -> str:
        return self._char_code
    
    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Символьный код должен быть строкой")
        if not value.strip():
            raise ValueError("Символьный код не может быть пустым")
        self._char_code = value.strip()
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название валюты должно быть строкой")
        if not value.strip():
            raise ValueError("Название валюты не может быть пустым")
        self._name = value.strip()
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Курс должен быть числом")
        if value <= 0:
            raise ValueError("Курс должен быть положительным числом")
        self._value = float(value)
    
    @property
    def nominal(self) -> int:
        return self._nominal
    
    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Номинал должен быть целым числом")
        if value <= 0:
            raise ValueError("Номинал должен быть положительным числом")
        self._nominal = value
    
    def add_to_history(self, value: float, timestamp: str):
        self.history.append({
            'value': value,
            'timestamp': timestamp
        })