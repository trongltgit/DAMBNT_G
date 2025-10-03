# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import get_user_by_username
from config import SECRET_KEY, DEFAULT_PASSWORD, DEFAULT_ADMIN_USERNAME

# Khởi tạo Ứng dụng Flask
app = Flask(__name__)
# Đặt khóa bí mật từ biến môi trường (Bắt buộc cho Render)
app.config['SECRET_KEY'] = SECRET_KEY
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=SESSION_TIMEOUT_SECONDS) # Không cần thiết cho ứng dụng này
bcrypt = Bcrypt(app)
CORS(app)

# --- ROUTES ---

@app.route('/')
def home():
    """Route gốc: Chuyển hướng người dùng đến trang đăng nhập."""
    # Nếu người dùng đã đăng nhập, có thể chuyển hướng đến trang dashboard hoặc home thực tế
    if 'logged_in' in session and session['logged_in']:
        # Hiện tại chưa có trang dashboard, nên ta giữ họ ở trang login (hoặc redirect tùy ý)
        return "Chào mừng đến với trang MBNT (Đã đăng nhập)!"
    
    # Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    """Hiển thị trang đăng nhập."""
    # Dữ liệu truyền vào template để hiển thị thông tin debug (không bắt buộc)
    data = {
        'default_user': DEFAULT_ADMIN_USERNAME,
        'default_pass': 'Vcb@1234' # Chỉ hiển thị mật khẩu gốc trong môi trường này
    }
    return render_template('login.html', data=data)

@app.route('/api/auth/login', methods=['POST'])
def handle_login():
    """API Endpoint xử lý logic đăng nhập."""
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return {'status': 'error', 'message': 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.'}, 400

    user = get_user_by_username(username)

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        # Đăng nhập thành công
        session['logged_in'] = True
        session['username'] = username
        
        # In thông báo thành công ra log (debug trên Render)
        print(f"User {username} logged in successfully.")
        
        return {'status': 'success', 'message': f'Đăng nhập thành công! Chào mừng {username}.'}
    else:
        # Đăng nhập thất bại
        return {'status': 'error', 'message': 'Tên đăng nhập hoặc mật khẩu không đúng.'}, 401

# --- Khởi động Ứng dụng (chỉ dùng cho phát triển cục bộ) ---
# Trong môi trường Render, Gunicorn sẽ chạy ứng dụng, không phải khối này
if __name__ == '__main__':
    # Chỉ nên chạy Flask debug mode khi phát triển
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
