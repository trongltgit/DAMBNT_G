import os
from flask_bcrypt import generate_password_hash

# Đọc mật khẩu mặc định và tên người dùng mặc định từ Environment Variables
# Lưu ý: Các biến này phải được thiết lập trên Render
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD', 'Vcb@1234')
DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin01')

# Mật khẩu được mã hóa (hashed) sẽ được tạo khi ứng dụng khởi động lần đầu
# Hàm này mô phỏng việc hash mật khẩu khi người dùng đăng ký lần đầu
DEFAULT_PASSWORD_HASH = generate_password_hash(DEFAULT_PASSWORD).decode('utf-8')

# Dữ liệu người dùng (Mô phỏng cơ sở dữ liệu)
USERS_DB = {
    DEFAULT_ADMIN_USERNAME: {
        'username': DEFAULT_ADMIN_USERNAME,
        # Lưu trữ mật khẩu đã được hash
        'password_hash': DEFAULT_PASSWORD_HASH,
        'role': 'admin'
    }
}

def get_user_by_username(username):
    """
    Hàm tìm kiếm người dùng trong cơ sở dữ liệu mô phỏng.
    
    Args:
        username (str): Tên đăng nhập cần tìm.
        
    Returns:
        dict: Thông tin người dùng nếu tìm thấy, ngược lại là None.
    """
    # Trả về thông tin người dùng từ USERS_DB nếu có
    return USERS_DB.get(username)

# In thông tin khởi tạo để dễ dàng gỡ lỗi
print(f"--- DATABASE STATUS ---")
print(f"Admin User: {DEFAULT_ADMIN_USERNAME}")
print(f"Default Password Hash: {DEFAULT_PASSWORD_HASH}")
print(f"-----------------------")
