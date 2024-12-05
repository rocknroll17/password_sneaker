import platform  # Add this import
from Windows import windows

def main():
    current_os = platform.system()
    if current_os == "Windows":
        win = windows()
        win.main()
    else:
        print("Unsupported OS")
    

if __name__ == "__main__":
    main()