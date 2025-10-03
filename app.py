import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from models import get_user_by_username
from config import SECRET_KEY, DEFAULT_PASSWORD, DEFAULT_ADMIN_USERNAME
from flask_bcrypt import Bcrypt

# Cấu hình ứng dụng
app = Flask(__name__)

# Đặt khóa bí mật từ biến môi trường (BẮT BUỘC cho session)
app.secret_key = SECRET_KEY 

# Khởi tạo Bcrypt
bcrypt = Bcrypt(app)

# Cấu hình CORS để cho phép các yêu cầu từ mọi nguồn gốc (chế độ phát triển/API)
# Trong môi trường sản xuất, nên giới hạn nguồn gốc cụ thể
CORS(app)

# ====================================================================
# ROUTE GIAO DIỆN (UI)
# ====================================================================

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login_page():
    # Đảm bảo trình duyệt luôn tải lại trang mới, rất quan trọng cho các thay đổi UI
    response = app.make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/dashboard')
def dashboard():
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'logged_in' in session and session['logged_in']:
        username = session.get('username', 'Admin')
        return f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f9; }}
                .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }}
                h1 {{ color: #0d9488; }}
                p {{ color: #333; }}
                .logout-btn {{ background-color: #ef4444; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; margin-top: 20px; display: inline-block; }}
                .logout-btn:hover {{ background-color: #dc2626; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Chào mừng, {username}!</h1>
                <p>Bạn đã đăng nhập vào Hệ thống MBNT thành công trên Render.</p>
                <a href="{url_for('logout')}" class="logout-btn">Đăng xuất</a>
            </div>
        </body>
        </html>
        """
    return redirect(url_for('login_page'))

# ====================================================================
# ROUTE API ĐĂNG NHẬP
# ====================================================================

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 1. Lấy thông tin người dùng
    user = get_user_by_username(username)
    
    if user:
        # 2. Kiểm tra mật khẩu bằng Bcrypt
        # So sánh password người dùng nhập (chuỗi) với password đã hash trong DB (user['password_hash'])
        if bcrypt.check_password_hash(user['password_hash'], password):
            session['logged_in'] = True
            session['username'] = username
            # 3. Trả về thành công
            return jsonify({'success': True, 'redirect': url_for('dashboard')}), 200
        else:
            # 4. Sai mật khẩu
            return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'}), 401
    else:
        # 5. Sai tên đăng nhập
        return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    # Trong Render, Gunicorn sẽ chạy ứng dụng này, nên dòng này không cần thiết
    # Tuy nhiên, vẫn giữ lại để test local
    app.run(debug=True, host='0.0.0.0')
