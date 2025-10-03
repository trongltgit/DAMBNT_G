# config.py

# Khóa bí mật cho Flask Session (Cần thay đổi khi triển khai thực tế)
SECRET_KEY = 'super_secure_and_secret_key_12345'

# Mật khẩu mặc định cho các user mới được Admin tạo
DEFAULT_PASSWORD = "Vcb@1234"

# Thời gian hiệu lực của báo giá (tính bằng giây)
# Yêu cầu: 2 phút = 120 giây
QUOTE_TIMEOUT_SECONDS = 120