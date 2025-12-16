# Nexus Job Portal - Standalone Edition

Welcome to the **Nexus Job Portal**, a high-performance **Standalone Desktop Application** built with Python and CustomTkinter.

> **Stealth Mode Update**: This version features a "Cyberpunk/Stealth" monochrome aesthetic, smooth animations, and direct local database integration. No backend server is required!

---

## 🚀 Quick Start Guide

### How to Install & Run

We have simplified the process to a single click.

1.  **Open the Project Folder**.
2.  Double-click **`run_gui.bat`**.
    - _First time?_ It will automatically create a virtual environment (`venv`) and install dependencies.
    - _Subsequent runs?_ It launches the app instantly.
3.  **That's it!** The app will fade in.

---

## 📖 Code Documentation & Working Concepts

This section provides a detailed explanation of "every single file" and the core concepts behind them, as requested.

### 1. Conceptual Architecture

- **Standalone MVC**: Unlike web apps, this is a desktop app that runs entirely on your machine.
  - **Model (`models.py`)**: Defines the data structure (User, Task, Order).
  - **View (`*ui.py`)**: The visual interface (Windows, Buttons, Animations).
  - **Controller (`database_service.py`)**: The brain that connects the View to the Model.
- **Direct Database Access**: We use **SQLAlchemy** to talk directly to a local SQLite file (`instance/database.db`). There is no network lag.
- **Threading**: To keep the "Fade-in" and "Slide-up" animations smooth, all database operations (loading tasks, creating orders) run in background threads. This prevents the UI from freezing.

### 2. File-by-File Explanation

#### 📂 Root Directory

- **`run_gui.bat`**: The automation script. It checks if Python is installed, creates a virtual environment, installs libraries from `requirements.txt`, and launches `src/gui/main.py`.
- **`requirements.txt`**: Lists the visual and logic libraries needed (e.g., `customtkinter`, `sqlalchemy`, `bcrypt`).

#### � `src/gui/` (The Frontend & Logic)

This is where 99% of the action happens now.

- **`main.py`**: **The Bootstrapper**.
  - _Concept_: It creates the main window application.
  - _Key Logic_: Sets the global `Theme`, initializes the `DatabaseService`, and triggers the startup `Animator.fade_in(self)`.
- **`auth_ui.py`**: **Access Control**.
  - _Concept_: Handles Login and Registration.
  - _Key Logic_: Uses `Animator.slide_up()` to make the login card float up. It validates inputs and calls `db_service.login()`.
- **`dashboard_ui.py`**: **The Command Center**.
  - _Concept_: The main screen after login.
  - _Key Logic_: Implements a Sidebar navigation system. Uses **Threading** to fetch Tasks and Orders without blocking clicks. It dynamically generates UI "Cards" for each item.
- **`database_service.py`**: **The Engine** (Crucial).
  - _Concept_: Replaces the old API Client. It talks to the SQLite database.
  - _Key Logic_: Contains methods like `create_user`, `get_tasks`, `create_order`. It manages the user session (`current_user_id`).
- **`theme.py`**: **The Palette**.
  - _Concept_: Centralized file for colors and fonts.
  - _Values_: Defines the "Stealth" colors (Black `#121212`, Surface `#1e1e1e`, Accent White `#ffffff`).
- **`animator.py`**: **Visual FX**.
  - _Concept_: A helper class for smooth transitions.
  - _Key Logic_: `fade_in` increases window opacity over time. `slide_up` adjusts widget padding to simulate movement.

#### 📂 `src/` (The Data Layer)

- **`models.py`**: **Data Blueprint**.
  - _Concept_: Defines what a "User" or "Task" looks like in the database (columns, types, relationships).
- **`db.py`**: **Connection Manager**.
  - _Logic_: Sets up the SQLAlchemy Engine to read `instance/database.db`.

#### 📂 Legacy Backend Files (Keep for Reference)

The following files were part of the old Client-Server architecture. They are **not used** by the standalone app but are kept if you ever want to revert to a web-server model.

- `app.py`, `routes.py`, `auth.py`, `api_client.py`.

---

## 🛠️ How to Use the Software

### 1. Authentication (The "Access Control" Screen)

- **Register**: Click **"NO CREDENTIALS? APPLY"**. Enter a Codename, Email, and Password. Creates a secure local account.
- **Login**: Enter your Email and Password. The system validates your hash.

### 2. Dashboard Navigation

- **OPERATIONS (Tasks)**:
  - View your active mission list.
  - Click **"NEW OPERATION"** to add a task.
  - Click **"DELETE"** to remove one.
- **LOGISTICS (Orders)**:
  - View product orders.
  - Click **"NEW ORDER"** to simulate a purchase.
- **TERMINATE SESSION**: Logs you out and returns to the Login screen.

---

## ❓ Troubleshooting

- **App won't start?**: Run `run_gui.bat` and watch for error messages. Ensure you have Python installed.
- **Database Locked?**: This is a local file. If the app crashes hard, you might need to restart your computer or delete `instance/database.db` to reset.

---

**Developed for Advanced Python Demonstration.**
_Architecture: Standalone Event-Driven Desktop Application._
