### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

### 📧 Contact Information for Projects
- **Always use real contacts** from `common/contacts_registry.py` when creating README files or documentation.
- **Never use placeholder contacts** like "your@email.com" or "YourName" in production code.
- **Use appropriate contact profile**:
  - `lazy_income_public` - For Lazy Income AI projects (default)
  - `client_public` - For client projects in public repositories
  - `client_private` - For client projects in private repositories

**Usage Example:**
```python
from common.contacts_registry import get_contacts

# Get contacts for your project
contacts = get_contacts("lazy_income_public")
readme_section = contacts.to_readme_section()

# Add to README.md
with open("README.md", "a") as f:
    f.write("\n\n")
    f.write(readme_section)
```

**For Client Projects:**
```python
from common.contacts_registry import update_client_profile

# Update client profile with real data
client_contacts = update_client_profile(
    profile_type="client_public",
    github_username="ClientCompany",
    company_name="Client Company Inc.",
    website="https://clientcompany.com"
)

readme_section = client_contacts.to_readme_section()
# Will include "Developed by Nikita Solovey | Lazy Income AI"
```

### ⚠️ Use-Case Specific Rules

**ВАЖЛИВО:** Деякі use-case мають специфічні workflow правила.

**Для `agent-factory-with-subagents`:**
- Читай `.claude/rules.md` та `CLAUDE.md` в директорії use-case
- Ці правила **ПЕРЕВИЗНАЧАЮТЬ** загальні правила вище
- Використовує: обов'язкове переключення в роль, Archon MCP Server, модульну архітектуру знань

**Якщо є конфлікт правил:**
- Пріоритет: Use-case правила > Агентні правила > Загальні правила (цей файл)