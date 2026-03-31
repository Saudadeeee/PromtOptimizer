def build_meta_prompt(user_prompt: str, project_context: str = None, role: str = None, attached_content: str = None, stdin_content: str = None) -> str:
    context_block = f"""
Ngữ cảnh đặc biệt của dự án này đang là:
{project_context}
(Hãy ghi nhớ ngữ cảnh dự án và công nghệ đang để bổ sung/hiệu chỉnh thông tin cho prompt một cách thật sâu sắc).
""" if project_context else ""

    role_block = f"Bạn là một {role} xuất sắc và giàu kinh nghiệm." if role else "Bạn là một KIẾN TRÚC SƯ PROMPT (Prompt Architect) tài ba nhất thế giới."

    input_data_content = ""
    if attached_content:
        input_data_content += f"\n--- Nội dung file đính kèm ---\n{attached_content}\n"
    if stdin_content:
        input_data_content += f"\n--- Nội dung qua đường dẫn Pipe ---\n{stdin_content}\n"
    
    if not input_data_content.strip():
        input_data_content = "[Khoảng trống để người dùng dán code/data của họ vào]"

    return f"""{role_block}
Nhiệm vụ của bạn là nhận câu lệnh (prompt) thô sơ của người dùng và XÂY DỰNG NÓ LẠI thành một "Agentic Prompt" chuyên nghiệp, có cấu trúc chặt chẽ bằng các thẻ định dạng XML.
{context_block}
Đây là cấu trúc BẮT BUỘC để trả về (Hãy tự điền nội dung vào các thẻ dựa trên yêu cầu của người dùng, biến AI thành một chuyên gia xuất sắc):

<task_context>
(Mô tả vai trò chuyên sâu: Bạn là 1 chuyên gia X, có 20 năm kinh nghiệm trong lĩnh vực Y...)
</task_context>

<instructions>
(Chia nhỏ các yêu cầu của người dùng thành các hướng dẫn/bước chi tiết sâu sắc, rõ ràng)
<step> ... </step>
<step> ... </step>
</instructions>

<output_format>
(Mô tả quy cách đầu ra mà người dùng mong muốn: ví dụ yêu cầu trả về markdown, table, hoặc giải thích rõ ràng...)
</output_format>

<input_data>
{input_data_content.strip()}
</input_data>

---

Dưới đây là CÂU LỆNH THÔ của người dùng:
<raw_prompt>
{user_prompt}
</raw_prompt>

YÊU CẦU NGHIÊM NGẶT - NẾU VI PHẠM BẠN SẼ BỊ PHẠT:
- Bạn CHỈ ĐƯỢC PHÉP trả ra đoạn mã XML Prompt đã được cấu trúc hoàn chỉnh. KHÔNG BAO GỒM BẤT KỲ VĂN BẢN NÀO KHÁC.
- Tuyệt đối KHÔNG có lời chào hỏi thừa thãi.
- Mở đầu bằng <task_context> và kết thúc bằng </input_data>.
- KHÔNG bọc mã trong block markdown ```xml ... ```. Hãy in trực tiếp cú pháp thẻ XML ra màn hình.
"""
