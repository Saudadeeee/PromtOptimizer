# PO CLI (Prompt Optimizer)

PO CLI is a Python-based command-line tool designed to streamline prompt engineering workflows. It acts as a compiler that takes simple user instructions and safely packs project context, file attachments, and directory structures into an optimized, XML-structured Agentic Prompt. The result is automatically copied to your clipboard, ready to be pasted into ChatGPT, Claude, or Gemini.

## Core Features

- **Automated Meta-Prompt Generation:** Compiles inputs into structured XML blocks and copies the final prompt directly to your system clipboard.
- **Project Structure Mapping (`--tree`):** Scans and attaches an ASCII representation of your project directory up to a custom depth, allowing LLMs to understand the codebase layout.
- **File Attachments (`-a`):** Easily inject raw source code or logs into your prompt by referencing local file paths.
- **API Engine with Streaming (`stream=True`):** Optionally connect to cloud LLMs directly through `litellm` (Google, OpenAI, Anthropic) and stream the generation output live in your terminal.
- **Token Estimation (`tiktoken`):** Automatically counts tokens before processing heavy attachments. Alerts you if the input exceeds 50,000 tokens to prevent accidental quota exhaustion.
- **Context Management (`po add` / `po pull`):** Create local project contexts or directly pull `.md` guidelines shared by the community via URL to instruct the AI with specific frameworks.
- **Secure `.env` Handling:** Safely segregates API Keys by transparently utilizing `python-dotenv` behind the scenes, ensuring credentials are never exposed in plaintext configuration files.

## How It Works

```text
[User Input Streams]
 ├── Argument:  po fix "Write tests"
 ├── Pipeline:  cat log.json | po fix "Check logs"
 ├── Attach:    -a ./src/api.js
 ├── Dir Tree:  --tree ./src --depth 3
 └── Context:   -p nextjs_app -r "QA Expert"
        │
        ▼
[Meta-Prompt Compiler] ---> (tiktoken checks API cost limit)
        │
    (Formats safely into XML)
        │
        ▼
   <XML Payload>
        │
  (Engine: API) ---> Connects via litellm (Gemini/OpenAI) 
        │            Streams generated output directly to console
        ▼
[Clipboard Cache] ---> Ready to paste anywhere (Ctrl+V)
```

## Installation

```bash
git clone https://github.com/Saudadeeee/PromtOptimizer.git
cd PromtOptimizer
pip install -e .
```
*(Requires Python 3.10+)*

## Getting Started

Set up the CLI to use the API engine and configure your API Key. Your credentials will be handled securely.

```bash
po config set engine api
po config set model gemini-2.5-flash
po config set GEMINI_API_KEY <YOUR_API_KEY>
```

## Usage Examples

**1. Basic Prompt Generation**
Generate a structured architecture prompt and instruct the AI to act as a specific expert:
```bash
po fix "Create a login form using React" -r "UI/UX Expert"
```

**2. Attaching Files and Directory Trees**
Pass a codebase file and append the overall directory structure up to 3 levels deep:
```bash
po fix "Refactor this fetch function based on the project structure" -a ./src/api.js --tree ./src --depth 3
```

**3. Saving and Reusing Project Contexts**
Maintain predefined project guidelines for consistent code generation:
```bash
# Register a new project context
po add my_project "E-commerce built with NextJS 14 and TailwindCSS. Strict Clean Code patterns."

# Use it later
po fix "Add a checkout button component" -p my_project
```

**4. Pulling Remote Context Templates**
```bash
po pull "expert_db" "https://raw.githubusercontent.com/.../database_expert.md"
```

**5. View History**
Review your previously generated meta-prompts:
```bash
po history
```

---
**Version:** 0.1
