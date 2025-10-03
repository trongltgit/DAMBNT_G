// static/js/main.js

const QUOTE_TIMEOUT = 120; // 120 giây (từ config.py)

function startCountdown(elementId, quoteTimeISO) {
    const quoteTime = new Date(quoteTimeISO);
    const countdownElement = document.getElementById(elementId);
    
    // Nếu element không tồn tại hoặc đã có timer, không làm gì
    if (!countdownElement || countdownElement.timer) {
        return;
    }

    // Định nghĩa timer cho element
    countdownElement.timer = setInterval(() => {
        const now = new Date();
        // Tính thời gian đã trôi qua (giây)
        const elapsed = (now.getTime() - quoteTime.getTime()) / 1000; 
        const remaining = QUOTE_TIMEOUT - elapsed;
        
        const minutes = Math.floor(remaining / 60);
        const seconds = Math.floor(remaining % 60);

        if (remaining <= 0) {
            clearInterval(countdownElement.timer);
            countdownElement.textContent = "HẾT HẠN";
            countdownElement.classList.add('expired'); 
            // Cần vô hiệu hóa nút CHẤP NHẬN tại đây
        } else {
            const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            countdownElement.textContent = timeString;

            // Chớp nháy khi còn dưới 30 giây
            if (remaining <= 30) {
                countdownElement.classList.add('flash-red');
            } else {
                countdownElement.classList.remove('flash-red');
            }
        }
    }, 1000);
}

// **QUAN TRỌNG:** Cần gọi hàm startCountdown này từ template client/dashboard.html
// khi có một yêu cầu ở trạng thái "Đã báo giá".
