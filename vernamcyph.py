import os
import time
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print(f"{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}           VERNAM CIPHER TOOL")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def alphabetnums():
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return alphabet

def vernam_encryption(message, reference_key, alphabet):
    index = 0
    encrypted = ""
    c = 0
    for x in message:
        if x.isspace():
            encrypted = encrypted + " "
            continue
        else:
            a = alphabet.index(x.upper()) if x.upper() in alphabet else 0
            b = alphabet.index(reference_key[index].upper()) if reference_key[index].upper() in alphabet else 0
            
            b = b + 1
            c = a + b
            
            if c >= 25:
                c = c - 26
                encrypted = encrypted + alphabet[c]
            else: 
                encrypted = encrypted + alphabet[c]
            index = index + 1
            if index >= len(reference_key):
                index = 0 
    return encrypted

def vernam_decryption(message, reference_key, alphabet):
    index = 0
    decrypted = ""
    c = 0
    for x in message:
        if x.isspace():
            decrypted = decrypted + " "
            continue
        else:
            a = alphabet.index(x.upper()) if x.upper() in alphabet else 0
            b = alphabet.index(reference_key[index].upper()) if reference_key[index].upper() in alphabet else 0
            
            b = b + 1
            c = a - b
            
            if c < 0:
                c = c + 25
                decrypted = decrypted + alphabet[c]
            elif c > 25:
                c = c - 25
                decrypted = decrypted + alphabet[c]
            else: 
                decrypted = decrypted + alphabet[c]
            index = index + 1
            if index >= len(reference_key):
                index = 0
    return decrypted

def print_banner():
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════╗
║{Fore.WHITE}{Style.BRIGHT}             VERNAM CIPHER             {Fore.CYAN} ║
╚════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def print_menu():
    menu = f"""
{Fore.GREEN}[1]{Fore.WHITE} Encrypt a message
{Fore.GREEN}[2]{Fore.WHITE} Decrypt a message
{Fore.GREEN}[3]{Fore.WHITE} Help
{Fore.GREEN}[4]{Fore.WHITE} Exit
    """
    print(menu)

def show_result(original, result, operation):
    print(f"\n{Fore.YELLOW}{'=' * 50}")
    print(f"{Fore.CYAN}Original text: {Fore.WHITE}{original}")
    print(f"{Fore.MAGENTA}{operation} text: {Fore.WHITE}{result}")
    print(f"{Fore.YELLOW}{'=' * 50}\n")
    input(f"{Fore.GREEN}Press Enter to continue...")

def show_help():
    clear_screen()
    print_header()
    print(f"\n{Fore.GREEN}{Style.BRIGHT}HELP INFORMATION")
    print(f"{Fore.WHITE}The Vernam cipher is a substitution cipher that uses a key to shift letters in the alphabet.")
    print(f"{Fore.WHITE}Each letter of the message is shifted based on the corresponding letter in the key.")
    print(f"{Fore.WHITE}If the key is shorter than the message, it is repeated until it matches the message length.")
    print(f"\n{Fore.YELLOW}Tips:")
    print(f"{Fore.WHITE}- For true security, use a key that's as long as the message and truly random")
    print(f"{Fore.WHITE}- The key should never be reused for multiple messages")
    print(f"{Fore.WHITE}- Spaces are preserved but other special characters may not work correctly")
    
    input(f"\n{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")


class VernamMain:
    @staticmethod   
    def main():
        getlist = alphabetnums()

        while True:
            clear_screen()
            print_banner()
            print_menu()
            
            choice = input(f"{Fore.YELLOW}Enter your choice: {Fore.WHITE}")
            
            if choice == '1':
                clear_screen()
                print_banner()
                print(f"{Fore.CYAN}=== ENCRYPTION MODE ===\n")
                message = input(f"{Fore.YELLOW}Enter the Message to encrypt: {Fore.WHITE}")
                reference_key = input(f"{Fore.YELLOW}Enter the key: {Fore.WHITE}")
                
                print(f"\n{Fore.GREEN}Encrypting...", end="")
                for _ in range(3):
                    time.sleep(0.3)
                    print(f"{Fore.GREEN}.", end="", flush=True)
                
                encrypted = vernam_encryption(message, reference_key, getlist)
                show_result(message, encrypted, "Encrypted")
            
            elif choice == '2':
                clear_screen()
                print_banner()
                print(f"{Fore.CYAN}=== DECRYPTION MODE ===\n")
                message = input(f"{Fore.YELLOW}Enter the Message to decrypt: {Fore.WHITE}")
                reference_key = input(f"{Fore.YELLOW}Enter the key: {Fore.WHITE}")
                
                print(f"\n{Fore.GREEN}Decrypting...", end="")
                for _ in range(3):
                    time.sleep(0.3)
                    print(f"{Fore.GREEN}.", end="", flush=True)
                
                decrypted = vernam_decryption(message, reference_key, getlist)
                show_result(message, decrypted, "Decrypted")
            
            elif choice == '4':
                clear_screen()
                print(f"{Fore.CYAN}Thank you for using Vernam Cipher!\n")
                break
            else:
                print(f"\n{Fore.RED}Invalid choice. Please try again.")
                time.sleep(1.5)

if __name__ == "__main__":
    VernamMain.main()