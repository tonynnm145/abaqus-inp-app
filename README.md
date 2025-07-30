# 🔧 Abaqus INP File Processor

Ứng dụng Streamlit để xử lý file INP của Abaqus - Tính toán và tạo file INP mới với vật liệu phân lớp.

## 📋 Mô tả

Ứng dụng này cho phép:
- **Đọc file INP**: Upload và phân tích file INP của Abaqus
- **Trích xuất tọa độ**: Lấy tọa độ Z từ các node trong file
- **Tính toán module đàn hồi**: Áp dụng công thức phân lớp cho vật liệu
- **Tạo file mới**: Xuất file INP đã được xử lý với vật liệu phân lớp

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.7 trở lên
- pip (Python package installer)

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd abaqus-inp-processor
```

### Bước 2: Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv

# Trên Windows
venv\Scripts\activate

# Trên macOS/Linux
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Sử dụng

### Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

### Hướng dẫn sử dụng

1. **Upload file INP**
   - Chọn file .inp của Abaqus từ máy tính
   - File phải có định dạng .inp hợp lệ

2. **Chọn tham số k**
   - Giá trị k cho tính toán module đàn hồi phân lớp
   - Phạm vi: 0 - 2.0
   - Giá trị mặc định: 0

3. **Xem kết quả**
   - Kiểm tra bảng tọa độ Z được trích xuất
   - Xem kết quả tính toán module đàn hồi

4. **Tải file mới**
   - Download file INP đã được xử lý
   - File mới sẽ có vật liệu phân lớp

## 📊 Công thức tính toán

### Module đàn hồi phân lớp
```
E = Eb + (Et - Eb) × ((2z + h)/(2h))^k
```

Trong đó:
- **E**: Module đàn hồi tại tọa độ z
- **Eb**: Module đàn hồi vật liệu dưới = 70 GPa
- **Et**: Module đàn hồi vật liệu trên = 380 GPa
- **h**: Chiều dày = 0.1
- **k**: Tham số phân lớp (người dùng nhập)
- **z**: Tọa độ Z của node

### Tính toán Ep
```
Ep = (4×E1 + 4×E2) / 8
```

## 📁 Cấu trúc dự án

```
abaqus-inp-processor/
├── app.py              # File Streamlit chính
├── backend.py          # Logic xử lý backend
├── requirements.txt    # Dependencies
├── README.md          # Hướng dẫn sử dụng
└── Job-demo.inp/      # File inp mẫu đầu vào
```

## 🔧 Chức năng chi tiết

### 1. Xử lý file INP
- Đọc và parse file INP
- Trích xuất thông tin node
- Lấy các tọa độ Z được chia trên mô hình

### 2. Tính toán vật liệu
- Tính module đàn hồi cho từng lớp
- Tạo 10 lớp vật liệu (ALU1-ALU10)
- Mật độ: 2700 kg/m³
- Hệ số Poisson: 0.33

### 3. Tạo file INP mới
- Thêm định nghĩa vật liệu
- Tạo elset cho từng lớp
- Chèn solid section cho mỗi lớp

## ⚠️ Lưu ý quan trọng

1. **Định dạng file**: Chỉ chấp nhận file .inp hợp lệ
2. **Cấu trúc file**: File phải có section *Node với tọa độ Z
3. **Kích thước file**: Không giới hạn, nhưng file lớn có thể mất thời gian xử lý
4. **Backup**: Luôn backup file gốc trước khi xử lý

## 🐛 Xử lý lỗi

### Lỗi thường gặp

1. **"Không trích được tọa độ z từ file .inp"**
   - Kiểm tra file có section *Node không
   - Đảm bảo tọa độ Z ở cột thứ 4

2. **"Lỗi khi tạo file"**
   - Kiểm tra cấu trúc file INP
   - Đảm bảo có section *INSTANCE

3. **File không upload được**
   - Kiểm tra định dạng file (.inp)
   - Đảm bảo file không bị hỏng

## 🤝 Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request


## 📞 Liên hệ

- **Tác giả**: Nguyễn Nhật Minh
- **Email**: NhatMinh1452003@gmail.com
- **GitHub**: github.com/tonynnm145

## 🙏 Cảm ơn

Cảm ơn bạn đã sử dụng Abaqus INP File Processor! Nếu có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ với chúng tôi. 
