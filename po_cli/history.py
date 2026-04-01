import os
import time
from pathlib import Path
from rich.console import Console

console = Console()
HISTORY_DIR = Path.home() / ".po_history"

def init_history_dir():
    if not HISTORY_DIR.exists():
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)

def save_history(user_prompt: str, optimized_prompt: str):
    init_history_dir()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_prompt = "".join([c if c.isalnum() else "_" for c in user_prompt[:20].strip()])
    if not safe_prompt:
        safe_prompt = "empty"
    filename = f"{timestamp}_{safe_prompt}.md"
    filepath = HISTORY_DIR / filename
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Mệnh lệnh gốc\n\n{user_prompt}\n\n---\n\n# Agentic Prompt\n\n```xml\n{optimized_prompt}\n```\n")
    except Exception as e:
        console.print(f"[bold red]Lỗi lưu lịch sử:[/bold red] {e}")

def list_history(limit: int = 10):
    init_history_dir()
    files = sorted(HISTORY_DIR.glob("*.md"), reverse=True)
    if not files:
        console.print("[italic yellow]Chưa có lịch sử prompt nào được lưu.[/italic yellow]")
        return
    
    console.print(f"\n[bold blue]Lịch sử {min(limit, len(files))} prompt gần nhất:[/bold blue]\n")
    for i, filepath in enumerate(files[:limit]):
        # Read the original prompt snippet
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                snippet = content.split("---")[0].replace("# Mệnh lệnh gốc", "").strip()
                snippet = snippet[:60] + "..." if len(snippet) > 60 else snippet
        except:
            snippet = "Lỗi đọc nội dung"
            
        parts = filepath.stem.split('_')
        time_str = parts[0] + " " + parts[1][:2] + ":" + parts[1][2:4] + ":" + parts[1][4:] if len(parts) >= 2 else filepath.stem
        console.print(f"- [{i+1}] [cyan]{time_str}[/cyan]: [yellow]{snippet}[/yellow]")
        console.print(f"    [dim italic]File: {filepath.absolute()}[/dim italic]")
    console.print()
