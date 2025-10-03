import os

# 1. SECRET_KEY: Khóa bảo mật cho Flask Session
# Đọc từ biến môi trường Render
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_fallback_secret_key_for_local_dev')

# 2. DEFAULT_PASSWORD: Mật khẩu mặc định cho người dùng admin
# Đọc từ biến môi trường Render (Vcb@1234)
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD', 'Vcb@1234')

# 3. DEFAULT_ADMIN_USERNAME: Tên người dùng mặc định
# Đọc từ biến môi trường Render (admin01)
DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin01')
