# 🚀 PO CLI - Prompt Optimizer (v0.1)

**PO CLI** (Prompt Optimizer) là một công cụ dòng lệnh (CLI) siêu tiện lợi chạy bằng Python, giúp biến những câu lệnh (prompt) văn xuôi lười biếng của bạn thành một "Cấu trúc Agentic XML Prompt" xịn sò để tối ưu hóa năng lực Code/Tư duy của các siêu AI như ChatGPT, Claude 3.5, hay Gemini 1.5.

Thay vì bắt bạn viết prompt thủ công dài dòng, `po_cli` tự động nén toàn bộ "**Mô tả bối cảnh dự án**", "**File đính kèm**", "**Cấu trúc cây thư mục**" thành một XML gọn gàng và tự động chép vào Clipboard của máy bạn để tiện dán đi muôn nơi.

---

## 🔥 Tính năng Nổi Bật

1. **Sinh Meta-Prompt vào Clipboard:** Chạy trên Terminal, chép kết quả liền tay vào RAM (Clipboard).
2. **Luồng dữ liệu Pipelining (`stdin`):** Hỗ trợ đường ống Unix standard (`cat log.txt | po fix "Xem lỗi"`). 
3. **Cây Thư Mục Dự án (`--tree`):** AI sẽ thấu hiểu toàn bộ cấu trúc dự án của bạn đến từng ngóc ngách nhờ sơ đồ ASCII Tree đính kèm.
4. **Đính file đa dạng (`-a`):** Ném file source code vào như một biến môi trường bằng `-a index.js`.
5. **Streaming Trực tiếp:** Hỗ trợ kết nối qua thư viện `litellm`. Đọc output nhả chữ trực tiếp từ Gemini/OpenAI ngay trên console Terminal.
6. **Token Guardian:** Báo cáo ước tính số lượng Token (bằng `tiktoken`) và chặn lại ngay nếu input vượt ngưỡng quá tải.
7. **Social Context (`po pull`):** Kéo mẫu context dự án chia sẻ từ Github Gist hay Markdown URL về dùng chỉ trong nháy mắt.
8. **Bảo mật `.env`:** Bảo vệ 100% cực kỳ an toàn các API Key khỏi việc lưu rò rỉ ở text thô.

---

## 🛠 Hướng dẫn Cài đặt

1. Kéo mã nguồn về:
```bash
git clone https://github.com/Saudadeeee/PromtOptimizer.git
cd PromtOptimizer
```

2. Cài đặt hệ thống dưới dạng package global:
```bash
pip install -e .
```
*(Yêu cầu Python 3.10+)*

---

## ⚙️ Cấu Hình Ban Đầu

Hệ thống hỗ trợ 2 chế độ Engine: **Gọi API thuần (`api`)** (Nhanh, xịn, dùng Token trực tiếp) hoặc **Gọi lệnh CMD Gemin cũ (`cli`)**. 
Chúng tôi khuyến nghị sử dụng **API Mode**:

```bash
# Chọn chế độ API
po config set engine api

# Chọn Model yêu thích (hỗ trợ OpenAI, Gemini, Anthropic qua LiteLLM)
po config set model gemini-2.5-flash

# Truyền API Key vào hệ thống (Nó sẽ bảo mật riêng ở ~/.po_env)
po config set GEMINI_API_KEY <Mã API của bạn>
```

---

## 🚀 Cách Dùng Thần Thánh

**1. Chỉ đạo cơ bản (Dễ dùng)**
```bash
po fix "Tạo form Đăng Nhập bằng React" -r "Chuyên gia UI"
```

**2. Quăng File và Quét Cây thư mục (Cực kì lợi hại khi debug codebase lớn)**
```bash
po fix "Viết hàm Fetch Data ở file này dựa theo thư mục cấu trúc" -a ./src/api.js --tree ./src --depth 3
```

**3. Tạo một lưu trữ dự án dài hơi (`po add`)**
Mỗi dự án công ty bạn có cách viết code riêng, hãy lưu Context lại:
```bash
po add next_ecom "Dự án Thương Mại Điện Tử dùng NextJS 14, TailwindCSS. Tuân thủ Clean Code và Server Actions."
```
Và xài nó mọi lúc mọi nơi bằng tham số `-p`:
```bash
po fix "Thêm nút thanh toán" -p next_ecom
```

**4. Kéo Context từ Cộng Đồng (`po pull`)**
```bash
po pull "chuyen_gia_db" "https://raw.githubusercontent.com/.../database_expert.md"
```

---

## 📜 Lịch sử thao tác (`po history`)
Đừng lo nếu lỡ làm mất Clipboard, gõ: `po history` để xem lại 10 prompt xịn sò nhất mà AI vừa sinh ra cho bạn.

---

> *Project tự hào được nâng cấp tự động hoá và tối ưu cùng AI cho luồng công việc của Developer.*
>  **Author:** Saudadeeee
>  **Version:** 0.1
