import sys
import importlib


def help_command():
    print("Available commands:")
    for command in commands:
        print(f"- {command}")


def reload_command():
    print("Reloading script functions...")
    # importlib.invalidate_caches()
    for module_name in ["commands_module", "cube"]:
        module = importlib.import_module(module_name)
        importlib.reload(module)
        globals().update(module.__dict__)
    print("Functions reloaded.")


def quit_command():
    print("Exiting...")
    sys.exit()


commands = {"help": help_command, "reload": reload_command, "quit": quit_command}
