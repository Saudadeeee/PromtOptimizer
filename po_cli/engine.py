import subprocess
import sys
import os
from rich.console import Console
from .context import get_config_value, list_configs

console = Console()

def clean_output(output: str) -> str:
    output = output.strip()
    if output.startswith("```xml"):
        output = output[6:]
    if output.startswith("```"):
        output = output[3:]
    if output.endswith("```"):
        output = output[:-3]
    return output.strip()

def call_gemini_cli(prompt: str) -> str:
    """
    Sử dụng subprocess để gọi lệnh gemini -p "prompt"
    """
    try:
        result = subprocess.run(
            ['gemini', '-p', prompt],
            capture_output=True,
            text=True,
            encoding='utf-8' # Hỗ trợ unicode trên môi trường shell Windows
        )
        if result.returncode != 0:
            console.print(f"[bold red]Lỗi từ gemini cli:[/bold red]\n{result.stderr}")
            sys.exit(1)
        
        return clean_output(result.stdout)

    except FileNotFoundError:
        console.print("[bold red]LỖI: Không tìm thấy lệnh 'gemini' trên hệ thống.[/bold red]")
        console.print("Vui lòng đảm bảo Gemini CLI đã được cài đặt và tồn tại trong biến môi trường PATH.")
        console.print("Hoặc bạn có thể chuyển sang gọi API bằng lệnh: po config set engine api")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Lỗi hệ thống không xác định:[/bold red] {e}")
        sys.exit(1)

def call_api_engine(prompt: str) -> str:
    try:
        import litellm
    except ImportError:
        console.print("[bold red]Vui lòng cài đặt litellm: pip install litellm[/bold red]")
        sys.exit(1)
        
    model = get_config_value("model", "gemini-1.5-flash")
    
    # Load keys into os.environ for litellm
    configs = list_configs()
    api_key_found = False
    for k, v in configs.items():
        if "API_KEY" in k.upper():
            os.environ[k.upper()] = v
            api_key_found = True
            
    if not api_key_found:
        console.print("[bold yellow]Cảnh báo: Chưa có API_KEY nào được cấu hình trong po config.[/bold yellow]")
        console.print("Gõ lệnh: po config set GEMINI_API_KEY <key> hoặc OPENAI_API_KEY <key> để sử dụng API.")

    if model.startswith("gemini"):
        # For litellm to map to google generative ai correctly
        model = f"gemini/{model}"

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        console.print(f"\n[bold cyan]Đang nhận dữ liệu từ {model}...[/bold cyan]\n")
        full_text = ""
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            full_text += content
            sys.stdout.write(content)
            sys.stdout.flush()
            
        print("\n")
        return clean_output(full_text)
    except Exception as e:
        with open("error.log", "w", encoding="utf-8") as f: f.write(str(e))
        console.print(f"\n[bold red]Lỗi gọi API ({model}):[/bold red] {e}")
        sys.exit(1)

def generate_meta_prompt(prompt: str) -> str:
    engine = get_config_value("engine", "cli")
    if engine.lower() == "api":
        return call_api_engine(prompt)
    else:
        return call_gemini_cli(prompt)
