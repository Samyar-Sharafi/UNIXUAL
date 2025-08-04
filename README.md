
      ██╗   ██╗    ███╗   ██╗    ██╗    ██╗  ██╗    ██╗   ██╗     █████╗     ██╗                  ██████╗     ███████╗
      ██║   ██║    ████╗  ██║    ██║    ╚██╗██╔╝    ██║   ██║    ██╔══██╗    ██║                 ██╔═══██╗    ██╔════╝
      ██║   ██║    ██╔██╗ ██║    ██║     ╚███╔╝     ██║   ██║    ███████║    ██║                 ██║   ██║    ███████╗
      ██║   ██║    ██║╚██╗██║    ██║     ██╔██╗     ██║   ██║    ██╔══██║    ██║                 ██║   ██║    ╚════██║
      ╚██████╔╝    ██║ ╚████║    ██║    ██╔╝ ██╗    ╚██████╔╝    ██║  ██║    ███████╗            ╚██████╔╝    ███████║
       ╚═════╝     ╚═╝  ╚═══╝    ╚═╝    ╚═╝  ╚═╝     ╚═════╝     ╚═╝  ╚═╝    ╚══════╝             ╚═════╝     ╚══════╝
                                                                                                                
                                                          U N I X U A L   O S



# UNIXUL OS — The Python UNIX-Like OS
A command-line terminal project that mimics basic Unix-like terminal behavior in Python, including login/registration with user roles, command handling, system information display, and basic shell commands.

---


## 🛠 Features

* User authentication (register & login)
* Role-based access control: `SYSTEM`, `admin`, `user`
* Unix-style commands:

  * `neofetch`, `top`, `ls`, `cat`, `date`, `uptime`, `whoami`
  * `sudo` command emulation
  * Basic `help` system
  * `terminal` passthrough command
  
* Tracks command history and session control

---

## 🚀 Getting Started

### 1. **Install Requirements**

This script requires `rich` and `psutil`:

```bash
pip install rich psutil
```

### 2. **Run the Program**

```bash
python main.py
```

---

## 🔐 User Management

On first launch, the program creates a `users.csv` file and auto-registers a `SYSTEM` user. Regular users can:

* **Register**: Creates a new user (the first becomes `admin`)
* **Login**: Authenticates with a SHA256-hashed password
* **Sudo**: Executes a command with elevated privileges if SYSTEM password is correct

---

## 💻 Supported Commands

| Command    | Description                                                |
| ---------- | ---------------------------------------------------------- |
| `help`     | List all available commands                                |
| `logout`   | Logs out the current user                                  |
| `pm`       | Simulates a package manager (`scoop` for Windows)          |
| `sudo`     | Prompts for SYSTEM password and runs the provided command  |
| `neofetch` | Displays system info (CPU, RAM, OS, etc.)                  |
| `ls`       | Lists files in the current directory                       |
| `top`      | Shows real-time CPU and RAM usage                          |
| `whoami`   | Prints the current username                                |
| `cat`      | Outputs the contents of a file                             |
| `uptime`   | Shows how long the system has been running                 |
| `date`     | Displays the current system date and time                  |
| `terminal` | Opens a passthrough terminal (`exit` with `terminal_exit`) |
| `clear`    | Clears the screen using `cls` or `clear`                   |
| `exit`     | Exits the program                                          |

---

## 🧠 Design Overview

### `startup_sequence()`

Simulates a boot loader with timed messages.

### `show_banner()`

Prints a stylized ASCII banner.

### `ensure_system_user()`

Ensures that the critical `SYSTEM` user is present in `users.csv`.

### `login()`

Handles user registration and login, checking for SHA256-password match.

### `shell()`

The core REPL loop for handling commands per session.

---

## 📦 File Requirements

* `users.csv`: Stores user data in `username,hashed_password,role` format.
* `.core/.backup/_sys/`: Directory containing optional multimedia and Python modules used by the program.

---

## 💡 Notes

* The terminal UI is purely simulated; it does not support actual bash scripting or command pipelines.
* The program is designed to be cross-platform but uses Windows-friendly conventions when possible.
* User data is not encrypted beyond hashing; avoid using real credentials in testing.

---

## ✅ Best Practices

* Do **not** use real system commands with `sudo`; they will be passed directly to `os.system`.
* Always back up `users.csv` before production use.
* When deploying, set secure permissions on `.core/` and sensitive files.

---
