import sys
import urllib.request
import typer
from rich.console import Console
from rich.panel import Panel
import pyperclip
import tiktoken
from typing import Optional, List
from pathlib import Path

from .context import (add_project, get_project, list_projects, remove_project, 
                      update_project, set_config_value, list_configs, get_config_value)
from .meta_prompt import build_meta_prompt
from .engine import generate_meta_prompt
from .history import save_history, list_history

app = typer.Typer(help="Prompt Optimizer (po) - Trợ thủ đắc lực định dạng Agentic Prompt bằng AI")
config_app = typer.Typer(help="Quản lý biến hệ thống và Engine API")
app.add_typer(config_app, name="config")
console = Console()

@app.command()
def fix(
    prompt: Optional[str] = typer.Argument(None, help="Câu mệnh lệnh (prompt) văn xuôi bạn muốn nâng cấp"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Khóa định danh (ID/tên) của dự án để truyền nội dung ngữ cảnh mồi"),
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Vai trò chuyên gia mà bạn muốn AI nhập vai"),
    attach: Optional[List[Path]] = typer.Option(None, "--attach", "-a", help="Đính kèm nội dung các file vào prompt"),
    tree: Optional[Path] = typer.Option(None, "--tree", "-t", help="Tạo sơ đồ cấu trúc thư mục tự động đính kèm (ASCII Tree)"),
    depth: int = typer.Option(3, "--depth", "-d", help="Độ sâu tối đa khi quét cây thư mục (mặc định = 3)")
):
    """
    Định dạng lại câu prompt và sao chép vào clipboard. Hỗ trợ dữ liệu từ stdin (Pipe).
    """
    
    def generate_tree(dir_path: Path, max_depth: int, current_depth: int = 0) -> str:
        if current_depth > max_depth or not dir_path.is_dir():
            return ""
        ignore_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', '.env', 'dist', 'build'}
        tree_str = f"{dir_path.name}/\n" if current_depth == 0 else ""
        try:
            items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            filtered_items = [i for i in items if i.name not in ignore_dirs]
            for idx, item in enumerate(filtered_items):
                prefix = "│   " * current_depth + ("├── " if idx < len(filtered_items) - 1 else "└── ")
                tree_str += f"{prefix}{item.name}\n"
                if item.is_dir():
                    tree_str += generate_tree(item, max_depth, current_depth + 1)
        except PermissionError:
            pass
        return tree_str
        
    def count_tokens(text: str) -> int:
        try:
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            return 0
    stdin_content = ""
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        
    if not prompt and not stdin_content:
        console.print("[bold red]Lỗi:[/bold red] Bạn phải nhập nội dung truy vấn hoặc Pipe dòng lệnh vào. Gõ: po fix --help")
        sys.exit(1)
        
    actual_prompt = prompt if prompt else "Vui lòng xử lý toàn bộ data trong file đầu vào này."

    project_context = None
    if project:
        project_context = get_project(project)
        if not project_context:
            console.print(f"[bold yellow]Cảnh báo:[/bold yellow] Không tìm thấy dự án '{project}'.")
        else:
            console.print(f"[bold cyan]Đang nạp context dự án:[/bold cyan] {project}\n")
            
    attached_content = ""
    if attach:
        for p in attach:
            if p.exists() and p.is_file():
                try:
                    content = p.read_text(encoding="utf-8")
                    attached_content += f"\n// --- Kèm nội dung file: {p.name} ---\n{content}\n"
                except Exception as e:
                    console.print(f"[yellow]Không thể đọc file {p.name}: {e}[/yellow]")
            else:
                console.print(f"[yellow]Bỏ qua file không tồn tại: {p}[/yellow]")

    if tree and tree.exists() and tree.is_dir():
        struct = generate_tree(tree, max_depth=depth)
        attached_content += f"\n// --- Sơ đồ cấu trúc thư mục (Depth={depth}): {tree.name} ---\n{struct}\n"
        console.print(f"[bold cyan]Đã đính kèm cấu trúc dự án:[/bold cyan] {tree}")

    meta_prompt = build_meta_prompt(
        user_prompt=actual_prompt, 
        project_context=project_context,
        role=role,
        attached_content=attached_content.strip() if attached_content else None,
        stdin_content=stdin_content if stdin_content else None
    )
    
    tokens = count_tokens(meta_prompt)
    if tokens > 0:
        console.print(f"[bold dim]Ước lượng token đầu vào: {tokens} tokens[/bold dim]")
        if tokens > 50000:
            console.print(Panel(
                "[bold red]CẢNH BÁO:[/bold red] Dữ liệu truyền vào quá lớn (>50k tokens).\nViệc này có thể gây tiêu tốn nhiều chi phí API hoặc vượt quá giới hạn của LLM.",
                title="Cảnh báo: Dữ liệu quá lớn", border_style="red"
            ))
            if not typer.confirm("Bạn có chắc chắn muốn tiếp tục gọi engine xử lý?"):
                raise typer.Abort()
    engine = get_config_value("engine", "cli")
    if engine.lower() == "api":
        optimized_prompt = generate_meta_prompt(meta_prompt)
    else:
        with console.status("[bold green]AI Engine đang định dạng cấu trúc XML Prompt...", spinner="dots"):
            optimized_prompt = generate_meta_prompt(meta_prompt)
    
    save_history(actual_prompt, optimized_prompt)

    console.print(Panel(
        optimized_prompt, 
        title="[bold green]Hoàn thành (Đã sao chép vào Clipboard)[/bold green]", 
        border_style="green",
        expand=False
    ))
    
    try:
        pyperclip.copy(optimized_prompt)
        console.print("[dim italic]* Dùng Ctrl+V dán thành quả vào cửa sổ Chat/IDE là chiến thôi.[/dim italic]")
    except Exception as e:
        console.print(f"[bold red]Lỗi Clipboard ({e}).[/bold red] Hãy copy thủ công ở ô trên.")

@app.command()
def add(name: str, description: str):
    """Đăng ký thông tin dự án (Project Context)."""
    add_project(name, description)
    console.print(f"[bold green]Đã lưu thông tin dự án: {name}[/bold green]")

@app.command()
def rm(name: str):
    """Xóa thông tin dự án."""
    if remove_project(name):
        console.print(f"[bold green]Đã xóa dự án: {name}[/bold green]")
    else:
        console.print(f"[bold red]Không tìm thấy dự án: {name}[/bold red]")

@app.command()
def edit(name: str):
    """Cập nhật nội dung Project."""
    old_desc = get_project(name)
    if not old_desc:
        console.print(f"[bold red]Dự án '{name}' không tồn tại.[/bold red]")
        return
    console.print(f"Cập nhật thông tin cho [cyan]{name}[/cyan] (Bấm Enter để đóng)")
    new_desc = typer.prompt("Mô tả mới", default=old_desc)
    update_project(name, new_desc)
    console.print(f"[bold green]Đã cập nhật dự án thành công.[/bold green]")

@app.command()
def ls():
    """Liệt kê danh sách dự án."""
    projects = list_projects()
    if not projects:
        console.print("[italic yellow]Hiện trong máy chưa có lưu cấu hình dự án nào.[/italic yellow]")
        return
    console.print("\n[bold blue]Danh sách dự án khả dụng:[/bold blue]\n")
    for name, desc in projects.items():
        console.print(f"- [bold cyan]{name}[/bold cyan]: {desc}")
    console.print()

@app.command()
def history(limit: int = 10):
    """Xem lịch sử các Meta-prompt đã tạo."""
    list_history(limit)
    
@app.command()
def pull(name: str, url: str):
    """Tải project template từ đường dẫn URL."""
    console.print(f"\n[cyan]Đang tải dữ liệu từ:[/cyan] {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            add_project(name, content)
            console.print(f"[bold green]Đã lưu dự án: {name} ({len(content)} ký tự)[/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]Lỗi tải file:[/bold red] {e}")

@config_app.command("set")
def config_set(key: str, value: str):
    """Cấu hình biến chung (engine/model/OPENAI_API_KEY). VD: po config set engine api"""
    set_config_value(key, value)
    console.print(f"[bold green]Cấu hình {key} = {value} thành công.[/bold green]")

@config_app.command("get")
def config_get():
    """Hiển thị toàn bộ biến cấu hình hiện hữu."""
    configs = list_configs()
    console.print("\n[bold blue]Cấu hình hệ thống:[/bold blue]\n")
    for k, v in configs.items():
        val = "***" if "API_KEY" in k.upper() else v
        console.print(f" - {k}: [cyan]{val}[/cyan]")
    console.print()

if __name__ == "__main__":
    app()
