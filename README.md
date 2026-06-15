# 42 - Python Modules 🐍

A deep dive into the Python ecosystem, focusing on software engineering best practices, rigorous static typing, and code quality under the **42 Network** curriculum framework.

---

## 🛠️ Quality Assurance & Tools

To match the strict evaluation standards of 42, this repository leverages an isolated virtual environment (`.venv`) utilizing static analysis tools to enforce code quality before any commit:

* **Flake8:** Enforces style guide consistency in compliance with **PEP 8**.
* **Mypy:** Enforces strict static typing (`--strict` mode), bringing the type-safety assurance of the C world into Python's dynamic nature.

---

## 📂 Repository Structure

The project is structured into progressive modules. The current roadmap and progress are detailed below:

| Module | Focus / Topics | Status |
| :--- | :--- | :---: |
| `module_00` | Starting, basic syntax, data structures, and recursion | ⏳ In Progress |
| `module_01` to `module_09` | OOP, advanced data manipulation, data science basics, and vectorization | 🔒 Locked |

---

## 🚀 Getting Started & Automation

All environment provisioning and testing pipelines are fully automated via the `Makefile`. No manual local Python configuration is required.

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/42-python-modules.git](https://github.com/your-username/42-python-modules.git)
cd 42-python-modules
