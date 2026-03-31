# PO CLI (Prompt Optimizer)

PO CLI là một công cụ dòng lệnh (CLI) được viết bằng Python hỗ trợ tối ưu hóa quy trình làm việc với các trung tâm trí tuệ nhân tạo (LLM). Thay vì phải viết các mô tả dài dòng thủ công, công cụ sẽ tự động nén bối cảnh dự án, file kỹ thuật, và cây cấu trúc mã nguồn thành một cấu trúc thẻ XML Agentic hoàn chỉnh dựa trên câu lệnh đầu vào của bạn. Phiên bản tối ưu này sẽ được tự động sao chép vào Clipboard để sử dụng ở bất kỳ nền tảng nào.

## Các tính năng chính

- **Sinh Meta-Prompt tự động:** Hệ thống tạo cấu trúc mô tả tối ưu và gửi thẳng vào Clipboard của hệ điều hành.
- **Phân tích Pipelining (stdin):** Hỗ trợ nhận dữ liệu đầu vào chuỗi Unix thông thường (ví dụ: `cat log.txt | po fix "Kiểm tra lỗi"`).
- **Trích xuất Cây Thư Mục (--tree):** Quét và hiển thị cấu trúc sơ đồ dự án theo dạng ASCII nhằm cung cấp cho mô hình AI góc nhìn bao quát về kiến trúc hệ thống.
- **Đính kèm file kỹ thuật (-a):** Cho phép gắn nội dung thực tế của các file mã nguồn trực tiếp vào cấu trúc Prompt bằng tham số `-a file_name.ext`.
- **Tương tác API Streaming:** Hỗ trợ kết nối và hiển thị kết quả truy xuất dữ liệu theo thời gian thực (streaming) thông qua thư viện `litellm` (hỗ trợ OpenAI, Gemini, Anthropic).
- **Hệ thống theo dõi Token:** Tích hợp thư viện OpenAI `tiktoken` đo lường số lượng token trong câu lệnh và tự động ngắt nếu dữ liệu vượt tải cấu hình của LLM.
- **Đồng bộ hóa Context từ cộng đồng (po pull):** Khả năng tải tập ngữ cảnh/mô tả bối cảnh mẫu được chia sẻ từ Github Gist hay Markdown URL về máy local nhanh chóng.
- **Quản lý đa bối cảnh dự án (po add):** Tự tạo và lưu giữ bối cảnh dự án trong file cấu hình để tái sử dụng với tham số `-p`.
- **Bảo mật .env nội bộ:** Tách bạch hệ thống lưu trữ Configuration nội bộ và API Keys để tránh tuyệt đối rò rỉ dữ liệu. Các thông tin nhạy cảm được cô lập qua biến hệ thống.

## Hướng dẫn cài đặt

Bạn có thể tải hoặc clone dự án về máy, sau đó cài đặt thiết lập toàn cục (global) bằng pip:

```bash
git clone https://github.com/Saudadeeee/PromtOptimizer.git
cd PromtOptimizer
pip install -e .
```
*(Yêu cầu Python 3.10 trở lên)*

## Cấu hình hệ thống

PO CLI hoạt động linh hoạt thông qua 2 cơ chế Engine: Gọi qua API trực tiếp hoặc gọi qua câu lệnh CLI local. Thiết lập dưới đây dùng để kích hoạt cấu hình chế độ API:

```bash
# Lựa chọn engine hoạt động là API
po config set engine api

# Cấu hình Model AI muốn sử dụng (vd: Gemini, GPT)
po config set model gemini-2.5-flash

# Cài đặt phương thức API Token (Dữ liệu sẽ được bảo vệ tại ~/.po_env)
po config set GEMINI_API_KEY <Mã_API_Của_Bạn_Tại_Đây>
```

## Các lệnh sử dụng cơ bản

**1. Tạo prompt cơ bản kết hợp định danh vai trò (Role)**
```bash
po fix "Tạo form đăng nhập bằng thư viện React" -r "Chuyên gia UI"
```

**2. Tạo prompt kèm file và cấu trúc cây thư mục**
Phân tích một hoặc nhiều file mã nguồn, kèm cấu trúc phân bổ của dự án với độ sâu quét tùy chọn:
```bash
po fix "Viết hàm Fetch Data ở file này dựa theo thư mục cấu trúc" -a ./src/api.js --tree ./src --depth 3
```

**3. Lưu nháp và gọi lại Context của một dự án (Project Context)**
Quản lý các bối cảnh để AI luôn nhớ được framework và tiêu chuẩn code mà bạn và công ty quy định:
```bash
# Khai báo ngữ cảnh
po add next_ecom "Dự án Thương Mại Điện Tử dùng NextJS 14, TailwindCSS. Tuân thủ Clean Code và Server Actions."

# Gọi và sử dụng bất cứ lúc nào
po fix "Thêm nút thanh toán" -p next_ecom
```

**4. Kéo Context từ internet về máy**
```bash
po pull "chuyen_gia_db" "https://raw.githubusercontent.com/.../database_expert.md"
```

**5. Lịch sử sử dụng**
Kiểm tra lại nội dung các lệnh bạn vừa xuất trước đây bằng lệnh:
```bash
po history
```

---
**Version:** 0.1
