# models.py
# Cài đặt: pip install Flask-Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import re
from config import DEFAULT_PASSWORD # Cần thiết để khởi tạo user mặc định

# Giả lập Database (Thay thế bằng SQLAlchemy/DB thực tế)
USERS_DB = {} # {user_id: User object}
REQUESTS_DB = {} # {request_id: dict/object}
BLOTTER_DB = {} # {deal_id: dict/object}

class User:
    def __init__(self, user_id, role, password_hash, needs_reset=True, dept='N/A'):
        self.user_id = user_id
        self.role = role # 'admin', 'dau_moi', 'phong'
        self.password_hash = password_hash
        self.needs_reset = needs_reset
        self.dept = dept

    @staticmethod
    def hash_password(password):
        # Trả về chuỗi hash đã được mã hóa UTF-8
        return generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def check_password_complexity(password):
    """
    Quy tắc: >= 8 ký tự, có hoa, thường, ký tự đặc biệt.
    """
    if len(password) < 8:
        return False, "Mật khẩu phải có tối thiểu 8 ký tự."
    if not re.search(r"[A-Z]", password):
        return False, "Mật khẩu phải có ít nhất một chữ hoa."
    if not re.search(r"[a-z]", password):
        return False, "Mật khẩu phải có ít nhất một chữ thường."
    if not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]", password):
        return False, "Mật khẩu phải có ít nhất một ký tự đặc biệt (!@#$...). "
    return True, "Mật khẩu hợp lệ."
    
# Khởi tạo user mặc định (Admin dùng để tạo các user khác)
default_hash = User.hash_password(DEFAULT_PASSWORD)
USERS_DB['admin01'] = User('admin01', 'admin', default_hash, needs_reset=False, dept='Admin')
USERS_DB['trader01'] = User('trader01', 'dau_moi', default_hash, needs_reset=True, dept='Trading')
USERS_DB['client01'] = User('client01', 'phong', default_hash, needs_reset=True, dept='Kế toán')