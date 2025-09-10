import secrets
from abc import ABC, abstractmethod
import hashlib
# Abstract base class for users
class User(ABC):
    def __init__(self,name : str , email : str , id : str, role : str):
        self.name = name
        self.email = email
        self.id = id
        self._role = role
        self.__salt = secrets.token_hex(16)
        self.__password_hash = None
    def set_password(self, password: str):
        """Sets the user's password by hashing it with a salt."""
        pass_data = (password + self.__salt).encode("utf-8")
        self.__password_hash = hashlib.sha256(pass_data).hexdigest()
    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored password hash."""
        if not self.__password_hash:
            return False
        pass_data = (password + self.__salt).encode("utf-8")
        return hashlib.sha256(pass_data).hexdigest() == self.__password_hash
    @property                              # Read-only property for role (attribute)
    def get_role(self) -> str:
        return self._role
    @abstractmethod
    def borrow_limit(self) -> int:
        return NotImplementedError

# subclass for a specific user type

# Student subclass
class Student(User):
    def __init__(self, name: str, email: str, id: str):
        super().__init__(name, email, id, role="Student")
    def borrow_limit(self) -> int:
        return 3  # Students can borrow up to 3 items

# Teacher subclass
class Teacher(User):
    def __init__(self, name: str, email: str, id: str):
        super().__init__(name, email, id, role="Teacher")
    def borrow_limit(self) -> int:
        return 5  # Teachers can borrow up to 5 items
    
# Admin subclass
class Admin(User):
    def __init__(self, name: str, email: str, id: str):
        super().__init__(name, email, id, role="Admin")
    def borrow_limit(self) -> int:
        return float("inf")  # Admins can borrow unlimited items