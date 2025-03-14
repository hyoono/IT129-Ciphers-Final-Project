import hashlib
import base64
import hmac
import os
import time
from colorama import init, Fore, Style, Back

# Initialize colorama
try:
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class DummyColor:
        def __getattr__(self, name):
            return ''
    Fore = Style = Back = DummyColor()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

class WordEncryptor:
    """Class for handling word encryption and decryption operations with enhanced security."""
    
    __LCG_A = 1103515245
    __LCG_C = 12345
    __LCG_M = 2**31
    
    @staticmethod
    def derive_seed_and_key(passphrase):
        """
        Derive a numeric seed and encryption key from a single passphrase.
        
        Args:
            passphrase (str): The user's passphrase
            
        Returns:
            tuple: (seed, key) where seed is an integer and key is a string
        """
        if not passphrase:
            raise ValueError("Passphrase cannot be empty")
        
        passphrase_bytes = passphrase.encode('utf-8')
        hash_obj = hashlib.sha256(passphrase_bytes)
        hash_hex = hash_obj.hexdigest()
        
        seed = int(hash_hex[:16], 16) 
        
        key = hash_hex[16:32]
        
        return seed, key
    
    @staticmethod
    def create_verification_hash(original_word, passphrase):
        """
        Create a verification hash for the original word and passphrase.
        
        Args:
            original_word (str): The original word before encryption
            passphrase (str): The user's passphrase
            
        Returns:
            str: Base64-encoded HMAC-SHA256 hash
        """
        key = passphrase.encode('utf-8')
        message = original_word.encode('utf-8')
        h = hmac.new(key, message, hashlib.sha256)
        return base64.b64encode(h.digest()).decode('utf-8')
    
    @staticmethod
    def verify_hash(word, passphrase, stored_hash):
        """
        Verify if the decrypted word and passphrase match the stored hash.
        
        Args:
            word (str): The decrypted word
            passphrase (str): The user's passphrase
            stored_hash (str): The hash created during encryption
            
        Returns:
            bool: True if the hash matches, False otherwise
        """
        calculated_hash = WordEncryptor.create_verification_hash(word, passphrase)
        return hmac.compare_digest(calculated_hash, stored_hash)
    
    @staticmethod
    def shuffle_word(word, seed):
        """
        Shuffle the characters of a word using a seeded random number generator.
        
        Args:
            word (str): The word to be shuffled
            seed (int): Seed for the random number generator
        
        Returns:
            str: The shuffled word
        """
        if not word:
            return word
            
        chars = list(word)
        n = len(chars)
        indices = list(range(n))
        
        current_prng = seed
        for i in range(n - 1, 0, -1):
            current_prng = (WordEncryptor.__LCG_A * current_prng + WordEncryptor.__LCG_C) % WordEncryptor.__LCG_M
            j = current_prng % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        
        return ''.join(chars[i] for i in indices)

    @staticmethod
    def deshuffle_word(shuffled_word, seed):
        """
        Reverse the shuffling process to recover the original word.
        
        Args:
            shuffled_word (str): The shuffled word
            seed (int): The same seed used for shuffling
        
        Returns:
            str: The original word
        """
        if not shuffled_word:
            return shuffled_word
            
        chars = list(shuffled_word)
        n = len(chars)
        indices = list(range(n))
        
        current_prng = seed
        for i in range(n - 1, 0, -1):
            current_prng = (WordEncryptor.__LCG_A * current_prng + WordEncryptor.__LCG_C) % WordEncryptor.__LCG_M
            j = current_prng % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        
        inv_indices = [0] * n
        for original_pos, shuffled_pos in enumerate(indices):
            inv_indices[shuffled_pos] = original_pos
        
        return ''.join(chars[i] for i in inv_indices)

    @staticmethod
    def generate_vigenere_key(word, key):
        """
        Generate a repeating key of appropriate length for Vigenère cipher.
        
        Args:
            word (str): The word to be encrypted
            key (str): The original key
        
        Returns:
            str: The extended key matching the word length
        """
        if not key:
            raise ValueError("Key cannot be empty")
            
        if len(word) <= len(key):
            return key[:len(word)]
        
        repeated_key = key * (len(word) // len(key) + 1)
        return repeated_key[:len(word)]

    @staticmethod
    def encrypt_vigenere(word, key):
        """
        Encrypt a word using the Vigenère cipher.
        
        Args:
            word (str): The word to encrypt
            key (str): The encryption key
        
        Returns:
            str: The encrypted word
        """
        if not word or not key:
            return word
            
        key = WordEncryptor.generate_vigenere_key(word, key)
        encrypted_text = []
        
        for i, char in enumerate(word):
            if char.isalpha():
                key_char = key[i % len(key)]
                base = ord('A') if key_char.isdigit() or not key_char.isalpha() else \
                       ord('A') if key_char.isupper() else ord('a')
                shift = ord(key_char) - base if key_char.isalpha() else int(key_char) % 26
                
                if char.isupper():
                    encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                else:
                    encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        
        return ''.join(encrypted_text)

    @staticmethod
    def decrypt_vigenere(word, key):
        """
        Decrypt a word using the Vigenère cipher.
        
        Args:
            word (str): The encrypted word
            key (str): The encryption key
        
        Returns:
            str: The decrypted word
        """
        if not word or not key:
            return word
            
        key = WordEncryptor.generate_vigenere_key(word, key)
        decrypted_text = []
        
        for i, char in enumerate(word):
            if char.isalpha():
                key_char = key[i % len(key)]
                base = ord('A') if key_char.isdigit() or not key_char.isalpha() else \
                       ord('A') if key_char.isupper() else ord('a')
                shift = ord(key_char) - base if key_char.isalpha() else int(key_char) % 26
                
                if char.isupper():
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                
                decrypted_text.append(decrypted_char)
            else:
                decrypted_text.append(char)
        
        return ''.join(decrypted_text)
    
    @staticmethod
    def encrypt(word, passphrase):
        """
        Encrypt a word using all security layers.
        
        Args:
            word (str): The word to encrypt
            passphrase (str): The user's passphrase
        
        Returns:
            tuple: (encrypted_word, verification_hash)
        """
        if not word:
            return word, ""
            
        verification_hash = WordEncryptor.create_verification_hash(word, passphrase)
        
        seed, key = WordEncryptor.derive_seed_and_key(passphrase)
        
        shuffled = WordEncryptor.shuffle_word(word, seed)
        encrypted = WordEncryptor.encrypt_vigenere(shuffled, key)
        
        return encrypted, verification_hash
    
    @staticmethod
    def decrypt(encrypted_word, passphrase, verification_hash):
        """
        Decrypt a word and verify its integrity.
        
        Args:
            encrypted_word (str): The encrypted word
            passphrase (str): The user's passphrase
            verification_hash (str): The hash created during encryption
        
        Returns:
            tuple: (decrypted_word, is_verified)
        """
        if not encrypted_word:
            return encrypted_word, False
            
        seed, key = WordEncryptor.derive_seed_and_key(passphrase)
        
        decrypted_vigenere = WordEncryptor.decrypt_vigenere(encrypted_word, key)
        original_word = WordEncryptor.deshuffle_word(decrypted_vigenere, seed)
        
        is_verified = WordEncryptor.verify_hash(original_word, passphrase, verification_hash)
        
        return original_word, is_verified

class FileEncryptor:
    """Class for handling file encryption and decryption operations."""
    
    @staticmethod
    def encrypt_file(input_path, output_path, passphrase):
        """
        Encrypt a text file line by line.
        
        Args:
            input_path (str): Path to the file to encrypt
            output_path (str): Path to save the encrypted file
            passphrase (str): The user's passphrase
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            encryptor = WordEncryptor()
            
            with open(input_path, 'r', encoding='utf-8') as infile, \
                 open(output_path, 'w', encoding='utf-8') as outfile:
                
                outfile.write("===ENCRYPTED FILE===\n")
                
                for line in infile:
                    line = line.rstrip('\n')
                    
                    if not line:
                        outfile.write('\n')
                        continue
                    
                    encrypted_line, verification_hash = encryptor.encrypt(line, passphrase)
                    
                    outfile.write(f"{encrypted_line}|||{verification_hash}\n")
                    
            return True
                
        except Exception as e:
            print(f"Error encrypting file: {str(e)}")
            return False
    
    @staticmethod
    def decrypt_file(input_path, output_path, passphrase):
        """
        Decrypt a text file that was encrypted with this tool.
        
        Args:
            input_path (str): Path to the encrypted file
            output_path (str): Path to save the decrypted file
            passphrase (str): The user's passphrase
            
        Returns:
            tuple: (success, verification_result) where:
                   success is True if operation completed, False otherwise
                   verification_result is a dict with counts of verified/failed lines
        """
        try:
            encryptor = WordEncryptor()
            verification_results = {"verified": 0, "failed": 0, "total": 0}
            
            with open(input_path, 'r', encoding='utf-8') as infile, \
                 open(output_path, 'w', encoding='utf-8') as outfile:
                
                first_line = infile.readline().strip()
                if first_line != "===ENCRYPTED FILE===":
                    return False, {"error": "Not a valid encrypted file"}
                
                for line in infile:
                    line = line.rstrip('\n')
                    

                    if not line:
                        outfile.write('\n')
                        continue
                    
                    try:
                        encrypted_line, verification_hash = line.split("|||", 1)
                    except ValueError:
                        outfile.write(f"{line}\n")
                        continue
                    
                    decrypted_line, is_verified = encryptor.decrypt(encrypted_line, passphrase, verification_hash)
                    outfile.write(f"{decrypted_line}\n")

                    verification_results["total"] += 1
                    if is_verified:
                        verification_results["verified"] += 1
                    else:
                        verification_results["failed"] += 1
                    
            return True, verification_results
                
        except Exception as e:
            print(f"Error decrypting file: {str(e)}")
            return False, {"error": str(e)}

class EncryptionApp:
    """Class for handling the encryption application UI and workflow."""
    
    @staticmethod
    def show_banner():
        """Display a stylish banner for the application."""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.YELLOW}{Style.BRIGHT}             ENHANCED ENCRYPTION TOOL                {Fore.CYAN} ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    @staticmethod
    def show_help():
        """Display help information about the application."""
        clear_screen()
        EncryptionApp.show_banner()
        
        help_text = f"""
{Fore.GREEN}{Style.BRIGHT}===== Enhanced Encryption Tool Help ====={Style.RESET_ALL}

This program allows you to encrypt words and text files with enhanced security features.
It uses the following, in a layered approach, to secure your data:

{Fore.YELLOW}1.{Fore.WHITE} Shuffling of characters based on a derived seed
{Fore.YELLOW}2.{Fore.WHITE} Vigenère cipher encryption with a passphrase-derived key  
{Fore.YELLOW}3.{Fore.WHITE} Cryptographic hashing for verification of decrypted data

{Fore.CYAN}{Style.BRIGHT}Available Options:{Style.RESET_ALL}
{Fore.YELLOW}• Encrypt a word{Fore.WHITE} - Securely encrypt individual words
{Fore.YELLOW}• Decrypt a word{Fore.WHITE} - Recover encrypted words using your passphrase
{Fore.YELLOW}• Encrypt a file{Fore.WHITE} - Encrypt entire text files line by line
{Fore.YELLOW}• Decrypt a file{Fore.WHITE} - Recover encrypted files with verification
        """
        print(help_text)
        input(f"\n{Fore.GREEN}Press Enter to return to the main menu...{Style.RESET_ALL}")

    @staticmethod
    def display_menu():
        """Display the main menu with styled options."""
        EncryptionApp.show_banner()
        
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}Select an option:{Style.RESET_ALL}

{Fore.GREEN}[1]{Fore.WHITE} Encrypt a word
{Fore.GREEN}[2]{Fore.WHITE} Decrypt a word
{Fore.GREEN}[3]{Fore.WHITE} Encrypt a text file
{Fore.GREEN}[4]{Fore.WHITE} Decrypt a text file
{Fore.GREEN}[5]{Fore.WHITE} Help
{Fore.GREEN}[6]{Fore.WHITE} Exit

{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}
        """
        print(menu)
    
    @staticmethod
    def display_progress(progress, total):
        """Display a progress bar for file operations."""
        bar_length = 40
        filled_length = int(bar_length * progress // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percent = (progress / total) * 100
        print(f"\r{Fore.CYAN}Progress: |{bar}| {percent:.1f}%", end='')
    
    @staticmethod
    def display_result(success, message, details=None):
        """Display an operation result with appropriate styling."""
        print("\n" + "─" * 50)
        if success:
            print(f"{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}✗ {message}{Style.RESET_ALL}")
        
        if details:
            print(f"{Fore.WHITE}{details}")
        print("─" * 50)
    
    @staticmethod
    def run():
        """Run the encryption application."""
        encryptor = WordEncryptor()
        file_encryptor = FileEncryptor()
        
        while True:
            clear_screen()
            EncryptionApp.display_menu()
            choice = input(f"{Fore.YELLOW}Enter your choice (1-6): {Style.RESET_ALL}")

            if choice == '1':  # Encrypt a word
                clear_screen()
                print(f"{Fore.CYAN}{Style.BRIGHT}[ WORD ENCRYPTION ]{Style.RESET_ALL}\n")
                
                word = input(f"{Fore.YELLOW}Enter the word to encrypt: {Style.RESET_ALL}")
                if not word:
                    EncryptionApp.display_result(False, "Word cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                    
                passphrase = input(f"{Fore.YELLOW}Enter your passphrase: {Style.RESET_ALL}")
                if not passphrase:
                    EncryptionApp.display_result(False, "Passphrase cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"\n{Fore.CYAN}Encrypting...{Style.RESET_ALL}")
                time.sleep(0.5)  # Small delay for visual effect
                
                encrypted, verification_hash = encryptor.encrypt(word, passphrase)
                
                EncryptionApp.display_result(True, "Encryption Complete", 
                                           f"Original: {Fore.WHITE}{word}\n"
                                           f"Encrypted: {Fore.YELLOW}{encrypted}\n"
                                           f"Verification Hash: {Fore.CYAN}{verification_hash}")
                input("\nPress Enter to continue...")
                
            elif choice == '2':  # Decrypt a word
                clear_screen()
                print(f"{Fore.CYAN}{Style.BRIGHT}[ WORD DECRYPTION ]{Style.RESET_ALL}\n")
                
                encrypted_word = input(f"{Fore.YELLOW}Enter the encrypted word: {Style.RESET_ALL}")
                if not encrypted_word:
                    EncryptionApp.display_result(False, "Encrypted word cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                    
                verification_hash = input(f"{Fore.YELLOW}Enter the verification hash: {Style.RESET_ALL}")
                if not verification_hash:
                    EncryptionApp.display_result(False, "Verification hash cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                    
                passphrase = input(f"{Fore.YELLOW}Enter your passphrase: {Style.RESET_ALL}")
                if not passphrase:
                    EncryptionApp.display_result(False, "Passphrase cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"\n{Fore.CYAN}Decrypting...{Style.RESET_ALL}")
                time.sleep(0.5)  # Small delay for visual effect
                
                decrypted_word, is_verified = encryptor.decrypt(encrypted_word, passphrase, verification_hash)
                
                if is_verified:
                    EncryptionApp.display_result(True, "Decryption and Verification Successful", 
                                              f"Encrypted: {Fore.YELLOW}{encrypted_word}\n"
                                              f"Decrypted: {Fore.GREEN}{decrypted_word}")
                else:
                    EncryptionApp.display_result(False, "Verification Failed", 
                                              f"Encrypted: {Fore.YELLOW}{encrypted_word}\n"
                                              f"Decrypted: {Fore.RED}{decrypted_word}\n"
                                              f"The passphrase may be incorrect or the data has been tampered with.")
                input("\nPress Enter to continue...")
            
            elif choice == '3':  # Encrypt a file
                clear_screen()
                print(f"{Fore.CYAN}{Style.BRIGHT}[ FILE ENCRYPTION ]{Style.RESET_ALL}\n")
                
                input_path = input(f"{Fore.YELLOW}Enter the path of the file to encrypt: {Style.RESET_ALL}")
                if not input_path:
                    EncryptionApp.display_result(False, "File path cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                output_path = input(f"{Fore.YELLOW}Enter the path for the encrypted file: {Style.RESET_ALL}")
                if not output_path:
                    EncryptionApp.display_result(False, "Output path cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                passphrase = input(f"{Fore.YELLOW}Enter your passphrase: {Style.RESET_ALL}")
                if not passphrase:
                    EncryptionApp.display_result(False, "Passphrase cannot be empty")
                    input("\nPress Enter to continue...")
                    continue

                input_path = os.path.abspath(input_path)
                output_path = os.path.abspath(output_path)
                
                print(f"\n{Fore.CYAN}Encrypting file... Please wait.{Style.RESET_ALL}")
                success = file_encryptor.encrypt_file(input_path, output_path, passphrase)
                
                if success:
                    EncryptionApp.display_result(True, "File Encryption Complete", 
                                              f"Encrypted file saved to: {Fore.GREEN}{output_path}")
                else:
                    EncryptionApp.display_result(False, "File Encryption Failed", 
                                              "Please check file paths and permissions. Try 'Run as Administrator' if needed.")
                
                input("\nPress Enter to continue...")
            
            elif choice == '4':  # Decrypt a file
                clear_screen()
                print(f"{Fore.CYAN}{Style.BRIGHT}[ FILE DECRYPTION ]{Style.RESET_ALL}\n")
                
                input_path = input(f"{Fore.YELLOW}Enter the path of the encrypted file: {Style.RESET_ALL}")
                if not input_path:
                    EncryptionApp.display_result(False, "File path cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                output_path = input(f"{Fore.YELLOW}Enter the path for the decrypted file: {Style.RESET_ALL}")
                if not output_path:
                    EncryptionApp.display_result(False, "Output path cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                passphrase = input(f"{Fore.YELLOW}Enter your passphrase: {Style.RESET_ALL}")
                if not passphrase:
                    EncryptionApp.display_result(False, "Passphrase cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                input_path = os.path.abspath(input_path)
                output_path = os.path.abspath(output_path)

                print(f"\n{Fore.CYAN}Decrypting file... Please wait.{Style.RESET_ALL}")
                success, results = file_encryptor.decrypt_file(input_path, output_path, passphrase)
                
                if success:
                    if "error" in results:
                        EncryptionApp.display_result(False, "File Decryption Error", 
                                                  f"Error: {results['error']}")
                    else:
                        total_lines = results["total"]
                        verified_lines = results["verified"]
                        failed_lines = results["failed"]
                        
                        if total_lines > 0:
                            success_rate = (verified_lines / total_lines) * 100
                            details = f"Decrypted file saved to: {Fore.GREEN}{output_path}\n" \
                                     f"Verification summary: {verified_lines}/{total_lines} lines verified ({success_rate:.1f}%)"
                            
                            if failed_lines > 0:
                                details += f"\n{Fore.RED}Warning: {failed_lines} lines failed verification."
                                
                            EncryptionApp.display_result(True, "File Decryption Complete", details)
                        else:
                            EncryptionApp.display_result(True, "File Decryption Complete", 
                                                      f"Decrypted file saved to: {Fore.GREEN}{output_path}")
                else:
                    EncryptionApp.display_result(False, "File Decryption Failed", 
                                              "Please check if it's a valid encrypted file. Try 'Run as Administrator' if needed.")
                
                input("\nPress Enter to continue...")
                
            elif choice == '5':  # Help
                EncryptionApp.show_help()
                
            elif choice == '6':  # Exit
                clear_screen()
                print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.YELLOW}{Style.BRIGHT}        Thank you for using this application!        {Fore.CYAN} ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
                """)
                time.sleep(1.5)
                break
                
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number from 1-6.{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    EncryptionApp.run()
