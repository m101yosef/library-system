from user import User, Student, Teacher, Admin
# Factory class to create user instances
class UserFactory:
    @staticmethod
    def create_user(name: str, email: str, user_id: str, role: str , password : str) -> User:
        role = role.lower()
        if role == "student":
            u =  Student(name, email, user_id)
        elif role == "teacher":
            u = Teacher(name, email, user_id)
        elif role == "admin":
            u = Admin(name, email, user_id)
        else:
            raise ValueError(f"Unknown role: {role}")
        u.set_password(password)
        return u