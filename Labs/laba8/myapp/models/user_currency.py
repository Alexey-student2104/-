class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: str):
        self._id = None
        self._user_id = None
        self._currency_id = None
        
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id
    
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
    def user_id(self) -> int:
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID пользователя должен быть целым числом")
        if value <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")
        self._user_id = value
    
    @property
    def currency_id(self) -> str:
        return self._currency_id
    
    @currency_id.setter
    def currency_id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ID валюты должен быть строкой")
        if not value.strip():
            raise ValueError("ID валюты не может быть пустым")
        self._currency_id = value.strip()