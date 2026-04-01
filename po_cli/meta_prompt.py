def build_meta_prompt(user_prompt: str, project_context: str = None, role: str = None, attached_content: str = None, stdin_content: str = None) -> str:
    context_block = f"""
Ngữ cảnh dự án:
{project_context}
(Sử dụng ngữ cảnh này để tinh chỉnh prompt phù hợp nhất).
""" if project_context else ""

    role_block = f"Bạn là một {role} chuyên nghiệp." if role else "Bạn là một Chuyên gia Kiến trúc Prompt (Prompt Architect)."

    input_data_content = ""
    if attached_content:
        input_data_content += f"\n--- Nội dung file đính kèm ---\n{attached_content}\n"
    if stdin_content:
        input_data_content += f"\n--- Nội dung qua đường dẫn Pipe ---\n{stdin_content}\n"
    
    if not input_data_content.strip():
        input_data_content = "[Khoảng trống để người dùng dán code/data của họ vào]"

    return f"""{role_block}
Nhiệm vụ của bạn là tái cấu trúc prompt thô của người dùng thành một Agentic Prompt chuyên nghiệp, cấu trúc bằng các thẻ XML.
{context_block}
Yêu cầu bắt buộc về cấu trúc đầu ra:

<task_context>
(Mô tả chi tiết vai trò chuyên gia)
</task_context>

<instructions>
(Chia nhỏ yêu cầu thành các bước hướng dẫn cụ thể, rõ ràng)
<step> ... </step>
<step> ... </step>
</instructions>

<output_format>
(Mô tả quy cách đầu ra: ví dụ markdown, dạng bảng, json...)
</output_format>

<input_data>
{input_data_content.strip()}
</input_data>

---

Dưới đây là CÂU LỆNH THÔ của người dùng:
<raw_prompt>
{user_prompt}
</raw_prompt>

YÊU CẦU NGHIÊM NGẶT:
- Chỉ trả về cấu trúc XML hợp lệ, tuyệt đối không chèn thêm văn bản thừa.
- Không có lời chào hỏi.
- Bắt đầu bằng <task_context> và kết thúc bằng </input_data>.
- Không bọc mã trong markdown code block (```xml). Trả văn bản thuần túy trực tiếp.
"""
