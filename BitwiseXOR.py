import os
import sys
import time

import pyperclip  # For clipboard functionality
from colorama import init, Fore, Style  # For colored output

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print(f"{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}           XOR BITWISE CIPHER TOOL")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def xor_encrypt(text, key):
    # Initialize an empty string for encrypted text
    encrypted_text = ""
    
    # Iterate over each character in the text
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    
    # Return the encrypted text
    return encrypted_text

def xor_decrypt(text, key):
    return xor_encrypt(text, key)  # XOR encryption and decryption are identical

def display_result(original, result, operation):
    """Display the result of encryption/decryption with formatting."""
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.GREEN}Original {'Text' if operation == 'encrypt' else 'Ciphertext'}:")
    print(f"{Fore.WHITE}{original}")
    
    print(f"\n{Fore.GREEN}{operation.capitalize()}ed {'Ciphertext' if operation == 'encrypt' else 'Plaintext'}:")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{result}")
    print(f"{Fore.CYAN}{'=' * 50}")
    
    # Add clipboard functionality
    pyperclip.copy(result)
    print(f"{Fore.MAGENTA}Result copied to clipboard!{Style.RESET_ALL}")

def save_to_file(content, operation):
    """Save the result to a file."""
    try:
        filename = input(f"\nEnter filename to save {operation}ed text (or press Enter to skip): ")
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"{Fore.GREEN}Successfully saved to {filename}!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving file: {e}{Style.RESET_ALL}")

def process_text(operation):
    clear_screen()
    print_header()
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{operation.capitalize()} Mode")
    
    # Get input text with proper prompting
    input_prompt = "Enter text to be encrypted: " if operation == "encrypt" else "Enter ciphertext to be decrypted: "
    text = input(f"\n{Fore.WHITE}{input_prompt}")
    
    # Get key with validation
    while True:
        key = input(f"{Fore.WHITE}Enter encryption key: ")
        if not key:
            print(f"{Fore.RED}Key cannot be empty. Please enter a valid key.{Style.RESET_ALL}")
        else:
            break
    
    # Show processing animation
    print(f"\n{Fore.CYAN}Processing", end="")
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.3)
    print()
    
    # Perform operation
    if operation == "encrypt":
        result = xor_encrypt(text, key)
    else:
        result = xor_decrypt(text, key)
    
    # Display and handle the result
    display_result(text, result, operation)
    
    # Option to save result
    save_to_file(result, operation)
    
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def encrypt():
    while True:
        process_text("encrypt")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}Would you like to encrypt another? ({Fore.GREEN}Y{Fore.YELLOW}/{Fore.RED}N{Fore.YELLOW}): ").upper()
            if choice == 'Y':
                break
            elif choice == 'N':
                return
            else:
                print(f"{Fore.RED}Invalid input. Please choose between Y or N only.{Style.RESET_ALL}")

def decrypt():
    while True:
        process_text("decrypt")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}Would you like to decrypt another? ({Fore.GREEN}Y{Fore.YELLOW}/{Fore.RED}N{Fore.YELLOW}): ").upper()
            if choice == 'Y':
                break
            elif choice == 'N':
                return
            else:
                print(f"{Fore.RED}Invalid input. Please choose between Y or N only.{Style.RESET_ALL}")

def show_help():
    """Display help information about the application."""
    clear_screen()
    print_header()
    print(f"\n{Fore.GREEN}{Style.BRIGHT}HELP INFORMATION")
    print(f"{Fore.WHITE}This tool uses XOR bitwise operation to encrypt and decrypt text.")
    print(f"{Fore.WHITE}The same key is used for both encryption and decryption.")
    print(f"{Fore.WHITE}The security of the encryption depends on the key's complexity.")
    print(f"\n{Fore.YELLOW}Tips:")
    print(f"{Fore.WHITE}- Use longer, random keys for better security")
    print(f"{Fore.WHITE}- Do not use this for sensitive data without understanding its limitations")
    print(f"{Fore.WHITE}- The encrypted text may contain unprintable characters")
    
    input(f"\n{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")

def main():
    while True:
        clear_screen()
        print_header()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}MAIN MENU")
        print(f"{Fore.YELLOW}1. {Fore.WHITE}Encryption")
        print(f"{Fore.YELLOW}2. {Fore.WHITE}Decryption") 
        print(f"{Fore.YELLOW}3. {Fore.WHITE}Help")
        print(f"{Fore.YELLOW}4. {Fore.WHITE}Exit")
        
        try:
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-4): ")
            
            if choice == '1':
                encrypt()
            elif choice == '2':
                decrypt()
            elif choice == '3':
                show_help()
            elif choice == '4':
                clear_screen()
                print(f"{Fore.YELLOW}Thank you for using the XOR Bitwise Cipher Tool. Goodbye!")
                time.sleep(1.5)
                break
            else:
                print(f"{Fore.RED}Invalid input. Please enter a number between 1 and 4.{Style.RESET_ALL}")
                time.sleep(1.5)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            time.sleep(1.5)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Program interrupted. Exiting...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            time.sleep(2)

if __name__ == "__main__":
    main()