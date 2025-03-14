import os
import pyperclip  # For clipboard functionality
from colorama import init, Fore, Style

# Try to import colorama for cross-platform colored output
try:
    init(autoreset=True)  # Initialize colorama
    HAS_COLOR = True
except ImportError:
    # Create dummy color classes if colorama is not available
    HAS_COLOR = False
    class DummyColor:
        def __getattr__(self, name):
            return ''
    Fore = Style = Back = DummyColor()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def vigenere_encrypt(plaintext, key):
    """Encrypts plaintext using Vigenère cipher with the given key."""
    ciphertext = []
    key = key.upper()
    key_index = 0
    
    for char in plaintext:
        if not char.isalpha():
            ciphertext.append(char)
            continue
            
        key_char = key[key_index % len(key)]
        key_shift = ord(key_char) - ord('A')
        key_index += 1
        
        if char.isupper():
            shifted = (ord(char) - ord('A') + key_shift) % 26 + ord('A')
        else:
            shifted = (ord(char) - ord('a') + key_shift) % 26 + ord('a')
            
        ciphertext.append(chr(shifted))
        
    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    """Decrypts ciphertext using Vigenère cipher with the given key."""
    plaintext = []
    key = key.upper()
    key_index = 0
    
    for char in ciphertext:
        if not char.isalpha():
            plaintext.append(char)
            continue
            
        key_char = key[key_index % len(key)]
        key_shift = ord(key_char) - ord('A')
        key_index += 1
        
        if char.isupper():
            shifted = (ord(char) - ord('A') - key_shift) % 26 + ord('A')
        else:
            shifted = (ord(char) - ord('a') - key_shift) % 26 + ord('a')
            
        plaintext.append(chr(shifted))
        
    return ''.join(plaintext)

def print_banner():
    """Print the application banner."""
    clear_screen()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Style.BRIGHT}          VIGENÈRE CIPHER TOOL          {Style.NORMAL}   ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════╝{Style.RESET_ALL}")

def display_menu():
    """Display the main menu options."""
    print_banner()
    print(f"\n{Fore.YELLOW}[{Fore.WHITE}1{Fore.YELLOW}]{Fore.RESET} Encrypt a message")
    print(f"{Fore.YELLOW}[{Fore.WHITE}2{Fore.YELLOW}]{Fore.RESET} Decrypt a message")
    print(f"{Fore.YELLOW}[{Fore.WHITE}3{Fore.YELLOW}]{Fore.RESET} Help / About")
    print(f"{Fore.YELLOW}[{Fore.WHITE}4{Fore.YELLOW}]{Fore.RESET} Exit")
    return input(f"\n{Fore.GREEN}Select an option (1-4): {Fore.RESET}")

def get_valid_key():
    """Get a valid encryption/decryption key from the user."""
    while True:
        key = input(f"{Fore.GREEN}Enter the key (alphabetic characters only): {Fore.RESET}")
        if key and all(c.isalpha() for c in key):
            return key
        print(f"{Fore.RED}Error: Key must contain only alphabetic characters and cannot be empty.{Fore.RESET}")

def show_results(original, key, result, operation_type, inverse_op):
    """Display operation results with formatting."""
    print(f"\n{Fore.CYAN}╔═══════════ RESULTS ═══════════╗{Fore.RESET}")
    print(f"{Fore.CYAN}║{Fore.RESET} {operation_type} completed successfully!")
    print(f"{Fore.CYAN}╠═════════════════════════════════╣{Fore.RESET}")
    print(f"{Fore.CYAN}║{Fore.RESET} {inverse_op} Message: {Fore.YELLOW}{original}{Fore.RESET}")
    print(f"{Fore.CYAN}║{Fore.RESET} Key:      {Fore.YELLOW}{key}{Fore.RESET}")
    print(f"{Fore.CYAN}║{Fore.RESET} Result:   {Fore.GREEN}{result}{Fore.RESET}")
    print(f"{Fore.CYAN}╚═════════════════════════════════╝{Fore.RESET}")
    
    try:
        pyperclip.copy(result)
        print(f"\n{Fore.GREEN}✓ Result copied to clipboard!{Fore.RESET}")
        input(f"{Fore.GREEN}Press Enter to continue...{Fore.RESET}")
    except:
        pass

def show_help():
    """Display help information about the Vigenère cipher."""
    print_banner()
    print(f"\n{Fore.CYAN}ABOUT THE VIGENÈRE CIPHER:{Fore.RESET}")
    print("The Vigenère cipher is a method of encrypting alphabetic text by using")
    print("a simple form of polyalphabetic substitution. It employs a keyword to")
    print("determine different shift values for different characters in the message.")
    print("\nUnlike the Caesar cipher which uses a single shift value, Vigenère")
    print("uses a sequence of shifts based on the letters of the keyword.")
    
    print(f"\n{Fore.CYAN}HOW IT WORKS:{Fore.RESET}")
    print("1. Each letter of the key is converted to a number (A=0, B=1, etc.)")
    print("2. The plaintext is processed letter by letter")
    print("3. Each letter is shifted by the corresponding number from the key")
    print("4. The key is repeated as needed to match the length of the message")

    input(f"\n{Fore.GREEN}Press Enter to return to the main menu...{Fore.RESET}")


def main():
    while True:
        choice = display_menu()
        
        if choice == '1':  # Encrypt
            clear_screen()
            print(f"\n{Fore.CYAN}╔═══════════ ENCRYPTION ═══════════╗{Fore.RESET}")
            message = input(f"\n{Fore.GREEN}Enter the message to encrypt: {Fore.RESET}")
            key = get_valid_key()
            
            encrypted = vigenere_encrypt(message, key)
            show_results(message, key, encrypted, "Encryption", "Original")
            
        elif choice == '2':  # Decrypt
            clear_screen()
            print(f"\n{Fore.CYAN}╔═══════════ DECRYPTION ═══════════╗{Fore.RESET}")
            message = input(f"\n{Fore.GREEN}Enter the message to decrypt: {Fore.RESET}")
            key = get_valid_key()
            
            decrypted = vigenere_decrypt(message, key)
            show_results(message, key, decrypted, "Decryption", "Encrypted")

        elif choice == '3':
            show_help()
            
        elif choice == '4':  # Exit
            print("Goodbye!")
            break
# Main program loop
if __name__ == "__main__":
    main()