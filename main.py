import csv
import hashlib
import os
from os import system, name as os_name
from rich.console import Console
from rich import print as richP
import time
import psutil  # For system stats (install via pip if needed)
import platform
import datetime

console = Console()

# ANSI escape codes for colors
COLORS = {
    "SYSTEM": "\033[95m",  # Light magenta
    "admin": "\033[1;34m",  # Bold Blue (extra fancy)
    "user": "\033[92m",    # Green
    "reset": "\033[0m"     # Reset
}


def show_banner():
    banner = r"""
 __  __  _   _  _   _  _  _  _    _    _
|  \/  || | | || \ | || || || |  | |  | |
| |\/| || | | ||  \| || || || |  | |  | |
| |  | || |_| || |\  || || || |__| |__| |
|_|  |_| \___/ |_| \_||_||_| \____/\____/
         Welcome to UNIXUL OS
"""
    richP(banner)


def ensure_system_user():
    SYSTEM_USERNAME = "SYSTEM"
    SYSTEM_PASSWORD = "SYSTEM"
    SYSTEM_ROLE = "SYSTEM"
    if not os.path.exists("users.csv") or os.path.getsize("users.csv") == 0:
        richP("🛠️ users.csv missing or empty. Creating SYSTEM user...")
        with open("users.csv", "w", newline="") as file:
            writer = csv.writer(file)
            hashed_pw = hashlib.sha256(SYSTEM_PASSWORD.encode()).hexdigest()
            writer.writerow([SYSTEM_USERNAME, hashed_pw, SYSTEM_ROLE])
        richP(
            f"🔐 SYSTEM user '{SYSTEM_USERNAME}' created with default password '{SYSTEM_PASSWORD}'. Please change it immediately!"
        )


def login():
    def hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(username: str, password: str):
        # Check if user already exists
        if os.path.exists('users.csv'):
            with open('users.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username:
                        richP(f"User '{username}' already exists. Try logging in.")
                        return False
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # First non-SYSTEM user becomes admin, else user
            role = "user"
            with open('users.csv', 'r') as f:
                users = list(csv.reader(f))
            non_system_users = [u for u in users if u and u[0].upper() != "SYSTEM"]
            if len(non_system_users) == 0:
                role = "admin"
            writer.writerow([username, hash_password(password), role])
        richP(f"User '{username}' registered successfully with role '{role}'.")
        return True

    def login_user(username: str, password: str):
        if username.upper() == "SYSTEM":
            richP(
                "Direct SYSTEM login not allowed. Use 'sudo' command after logging in as a normal user."
            )
            return None

        hashed_password = hash_password(password)
        if not os.path.exists('users.csv'):
            richP("No users registered yet. Please register first.")
            return None
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue
                if row[0] == username and row[1] == hashed_password:
                    return row[2]  # return role
        return None

    while True:
        action = input("Do you want to (register/login/exit)? ").strip().lower()
        if action == 'register':
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            register_user(username, password)
        elif action == 'login':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            role = login_user(username, password)
            if role:
                richP(f"Login successful! Welcome, {username} ({role}).")
                return username, role
            else:
                richP("Login failed. Please check your username and password.")
        elif action == 'exit':
            richP("Exiting the program.")
            return None, None
        else:
            richP("Invalid option. Please choose 'register', 'login', or 'exit'.")


def prompt_user(username, role):
    color = COLORS.get(role.lower(), COLORS["reset"])
    return input(f"{color}{username}@unixul ~> {COLORS['reset']}")


def simulate_package_manager():
    if os.name == 'nt':
        richP("🔧 Using Scoop...")
        os.system("scoop help")
    else:
        richP("🔧 Using Linux package manager...")
        os.system("echo 'apt or pacman or yum depending on distro'")


def run_sudo_command(system_password_hash):
    entered_pw = input("SUDO Password: ")
    if hashlib.sha256(entered_pw.encode()).hexdigest() == system_password_hash:
        richP("SUDO access granted! Running command as SYSTEM...")
        return True
    else:
        richP("SUDO: Incorrect password!")
        return False


# Unix-like command implementations

def cmd_neofetch():
    ascii_logo = r"""
      .--.
     |o_o |
     |:_/ |
    //   \ \
   (|     | )
  /'\_   _/`\
  \___)=(___/
"""
    uname = platform.uname()
    richP(ascii_logo)
    richP(f"OS: {uname.system} {uname.release}")
    richP(f"Node Name: {uname.node}")
    richP(f"Machine: {uname.machine}")
    richP(f"Processor: {uname.processor}")
    richP(f"Python Version: {platform.python_version()}")
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    richP(f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    richP(f"CPU Usage: {psutil.cpu_percent()}%")
    richP(f"RAM Usage: {psutil.virtual_memory().percent}%")


def cmd_ls():
    try:
        files = os.listdir(".")
        for f in files:
            richP(f)
    except Exception as e:
        richP(f"Error listing directory: {e}")


def cmd_top():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    richP(f"CPU Usage: {cpu}%")
    richP(f"RAM Usage: {ram.percent}% ({ram.used // (1024 ** 2)} MB used / {ram.total // (1024 ** 2)} MB total)")


def cmd_whoami(username):
    richP(username)


def cmd_cat(args):
    if not args:
        richP("Usage: cat <filename>")
        return
    filename = args[0]
    if not os.path.exists(filename):
        richP(f"cat: {filename}: No such file or directory")
        return
    try:
        with open(filename, "r") as file:
            richP(file.read())
    except Exception as e:
        richP(f"Error reading file: {e}")


def cmd_uptime():
    uptime_sec = time.time() - psutil.boot_time()
    uptime_str = str(datetime.timedelta(seconds=int(uptime_sec)))
    richP(f"Uptime: {uptime_str}")


def cmd_date():
    now = datetime.datetime.now()
    richP(now.strftime("%a %b %d %H:%M:%S %Y"))

def legecy():
    os.rename( "./legacy/audio_test.mp3.bak", "./legacy/audio_test.mp3" )
    os.rename( "./legacy/lyric_test.lrc.bak", "./legacy/lyric_test.lrc" )
    os.rename( "./.core/.backup/_sys/_sys_audio_driver_check.py.bak", "./.core/.backup/_sys/_sys_audio_driver_check.py" )
    os.system("python ./.core/.backup/_sys/_sys_audio_driver_check.py")

def shell(username, role):
    while True:
        cmd = prompt_user(username, role).strip()

        if not cmd:
            continue

        parts = cmd.split()
        command = parts[0].lower()
        args = parts[1:]

        match command:
            case "logout":
                richP("👋 Logging out...")
                return  # back to login loop

            case _ if command == "sudo":
                system_pw_hash = None
                with open('users.csv', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[0] == "SYSTEM":
                            system_pw_hash = row[1]
                            break

                if system_pw_hash and run_sudo_command(system_pw_hash):
                    sudo_cmd = " ".join(args)
                    richP(f"[SYSTEM]$ {sudo_cmd}")
                    os.system(sudo_cmd)
                else:
                    richP("Failed to get SYSTEM privileges.")

            case "help":
                richP("📜 Available commands: help, logout, pm, sudo <command>, neofetch, ls, top, whoami, cat, uptime, date")

            case "pm":
                simulate_package_manager()

            case "neofetch":
                cmd_neofetch()

            case "ls":
                cmd_ls()

            case "top":
                cmd_top()

            case "whoami":
                cmd_whoami(username)

            case "cat":
                cmd_cat(args)

            case "uptime":
                cmd_uptime()

            case "date":
                cmd_date()

            case "terminal":
                while True:
                    console.print("[magenta]Terminal >>> [/magenta]", end="")
                    terminal_input = input()
                    if terminal_input == "terminal_exit":
                        break
                    system(terminal_input)

            case "clear":
                system("cls" if os_name == "nt" else "clear")

            case "exit":
                for i in range(4):
                    richP(
                        f"[bold yellow]Exiting the console{'...'[:i+1]}{' ' * (3 - i)}[/bold yellow]",
                        end="\r",
                    )
                    time.sleep(0.5)
                system("cls" if os_name == "nt" else "clear")
                exit()

            case _:
                richP(
                    f"""[red]{cmd} : The term '{cmd}' is not recognized as the name of a command, function, script file, 
    or operable program. Check the spelling of the name, or if a path was included, verify 
    that the path is correct and try again.[/red]"""
                )


def main():
    show_banner()
    ensure_system_user()

    while True:
        username, role = login()
        if not username:
            richP("Goodbye!")
            break
        shell(username, role)


if __name__ == "__main__":
    main()
