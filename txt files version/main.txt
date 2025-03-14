import sys
import os
import time
try:
    from colorama import init, Fore, Style
    colorama_available = True
except ImportError:
    colorama_available = False
    print("For better UI, install colorama: pip install colorama")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header."""
    width = 50
    if colorama_available:
        print(Fore.CYAN + "=" * width + Style.RESET_ALL)
        print(Fore.YELLOW + title.center(width) + Style.RESET_ALL)
        print(Fore.CYAN + "=" * width + Style.RESET_ALL)
    else:
        print("=" * width)
        print(title.center(width))
        print("=" * width)

def vernam_cipher_program():
    # Same implementation as before
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    try:
        import vernamcyph
        if hasattr(vernamcyph, 'VernamMain'):
            vernamcyph.VernamMain.main()
    except ImportError:
        print_error("Could not find vernamcyph module. Please check its location.")
        input("\nPress Enter to return to the main menu...")

def vignere_cipher_program():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    try:
        import vignere
        if hasattr(vignere, 'main'):
            vignere.main()
    except ImportError:
        print_error("Could not find vignere module. Please check its location.")
        input("\nPress Enter to return to the main menu...")

def bitwise_xor_program():
    # Same implementation with error handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    try:
        import BitwiseXOR
        if hasattr(BitwiseXOR, 'main'):
            BitwiseXOR.main()
    except ImportError:
        print_error("Could not find BitwiseXOR module. Please check its location.")
        input("\nPress Enter to return to the main menu...")

def custom_algorithm_program():
    # Same implementation with error handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    try:
        import customcipher
        if hasattr(customcipher, 'EncryptionApp'):
            customcipher.EncryptionApp.run()
    except ImportError:
        print_error("Could not find customcipher module. Please check its location.")
        input("\nPress Enter to return to the main menu...")

def print_error(message):
    """Print error message with formatting."""
    if colorama_available:
        print(Fore.RED + "\n⚠️ " + message + Style.RESET_ALL)
    else:
        print("\n⚠️ " + message)

def print_menu():
    """Display the main program menu."""
    if colorama_available:
        print(Fore.GREEN + "\n📋 ENCRYPTION ALGORITHMS" + Style.RESET_ALL)
        print(Fore.WHITE + "------------------------" + Style.RESET_ALL)
        print(Fore.CYAN + "1." + Style.RESET_ALL + " Vernam Cipher")
        print(Fore.CYAN + "2." + Style.RESET_ALL + " Vignere Cipher")
        print(Fore.CYAN + "3." + Style.RESET_ALL + " Bitwise XOR")
        print(Fore.CYAN + "4." + Style.RESET_ALL + " Custom Algorithm")
        print(Fore.CYAN + "5." + Style.RESET_ALL + " Exit")
    else:
        print("\n📋 ENCRYPTION ALGORITHMS")
        print("------------------------")
        print("1. Vernam Cipher")
        print("2. Vignere Cipher")
        print("3. Bitwise XOR")
        print("4. Custom Algorithm")
        print("5. Exit")

def main():
    if colorama_available:
        init(autoreset=True)  # Initialize colorama
        
    try:
        while True:
            clear_screen()
            print_header("ENCRYPTION TOOL")
            print_menu()
            choice = input("\n👉 Enter your choice (1-5): ")

            if choice == "1":
                clear_screen()
                print_header("VERNAM CIPHER")
                vernam_cipher_program()
            elif choice == "2":
                clear_screen()
                print_header("VIGNERE CIPHER")
                vignere_cipher_program()
            elif choice == "3":
                clear_screen()
                print_header("BITWISE XOR")
                bitwise_xor_program()
            elif choice == "4":
                clear_screen()
                print_header("CUSTOM ALGORITHM")
                custom_algorithm_program()
            elif choice == "5":
                clear_screen()
                print_header("GOODBYE!")
                print("\nThank you for using the Encryption Tool.")
                print("Exiting program...\n")
                time.sleep(1)
                break
            else:
                print_error("Invalid choice. Please enter a number from 1-5.")
                time.sleep(1.5)
    except KeyboardInterrupt:
        clear_screen()
        print_header("GOODBYE!")
        print("\nProgram terminated by user.")
        print("Exiting program...\n")
        sys.exit(0)

if __name__ == "__main__":
    main()