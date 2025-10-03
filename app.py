from flask import Flask, request, redirect, url_for, session, render_template, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS 
import time
from datetime import timedelta
from flask import after_this_request

# Import cấu hình và mô hình 
from config import SECRET_KEY, SESSION_TIMEOUT_SECONDS
from models import USERS_DB, User 

# --- APPLICATION INITIALIZATION ---
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# Đặt thời gian hết hạn session thành vĩnh viễn (cho đến khi logout hoặc hết thời gian timeout)
app.permanent_session_lifetime = timedelta(seconds=SESSION_TIMEOUT_SECONDS)
bcrypt = Bcrypt(app) 
CORS(app) 

# In thông tin mặc định khi khởi động server
print(f"Server đã khởi động thành công.")
print(f"User test: {', '.join(USERS_DB.keys())}")


# --- API LOGIN (AJAX HANDLER) ---
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Xử lý đăng nhập qua API (Fetch/AJAX)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Yêu cầu phải là JSON."}), 400

        user_id = data.get('username')
        password = data.get('password')

        user = USERS_DB.get(user_id)

        # 1. Xác thực mật khẩu 
        if user and user.check_password(password):
            
            # 2. Tạo Session
            session.permanent = True
            session['user_id'] = user.user_id
            session['role'] = user.role
            session['last_activity'] = time.time() 

            # 3. Xác định trang chuyển hướng 
            if user.needs_reset:
                next_url = url_for('change_password', _external=True)
            elif user.role == 'admin':
                next_url = url_for('admin_dashboard', _external=True)
            elif user.role == 'dau_moi':
                next_url = url_for('trader_dashboard', _external=True)
            elif user.role == 'phong':
                next_url = url_for('client_dashboard', _external=True)
            else:
                next_url = url_for('login', _external=True)

            return jsonify({
                "success": True, 
                "message": "Đăng nhập thành công!",
                "user_id": user.user_id,
                "role": user.role, 
                "needs_reset": user.needs_reset,
                "redirect_url": next_url
            })
        else:
            return jsonify({"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu."}), 401

    except Exception as e:
        print(f"Lỗi đăng nhập API: {e}")
        return jsonify({"success": False, "message": "Lỗi hệ thống không xác định. Vui lòng kiểm tra terminal."}), 500

# --- ROUTE GET /LOGIN (Hiển thị HTML) ---
@app.route('/')
@app.route('/login', methods=['GET'])
def login():
    """Hiển thị trang đăng nhập và xử lý chuyển hướng nếu đã đăng nhập"""
    @after_this_request
    def add_header(response):
        # Đảm bảo trình duyệt không cache trang đăng nhập
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response

    if 'user_id' in session and session.get('user_id') in USERS_DB:
        user = USERS_DB[session['user_id']]
        if user.role == 'admin': return redirect(url_for('admin_dashboard'))
        if user.role == 'dau_moi': return redirect(url_for('trader_dashboard'))
        if user.role == 'phong': return redirect(url_for('client_dashboard'))
    
    return render_template('login.html')

# --- HÀM HỖ TRỢ ĐĂNG XUẤT và DASHBOARD GIẢ LẬP ---
@app.route('/logout', methods=['GET'])
def logout():
    # Xóa hoàn toàn session
    session.clear() 
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return f"<h1>Admin Dashboard</h1><p>Chào mừng Admin {session.get('user_id')}.</p><a href='{url_for('logout')}'>Đăng xuất</a>"

@app.route('/trader/dashboard')
def trader_dashboard():
    if session.get('role') != 'dau_moi': return redirect(url_for('login'))
    return f"<h1>Trader Dashboard</h1><p>Chào mừng Trader {session.get('user_id')}.</p><a href='{url_for('logout')}'>Đăng xuất</a>"

@app.route('/client/dashboard')
def client_dashboard():
    if session.get('role') != 'phong': return redirect(url_for('login'))
    return f"<h1>Client Dashboard</h1><p>Chào mừng Client {session.get('user_id')}.</p><a href='{url_for('logout')}'>Đăng xuất</a>"

@app.route('/change-password')
def change_password():
    if 'user_id' not in session: return redirect(url_for('login'))
    return f"<h1>Đổi Mật khẩu Lần đầu</h1><p>Chào mừng {session.get('user_id')}. Vui lòng đổi mật khẩu.</p><a href='{url_for('logout')}'>Đăng xuất</a>"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
