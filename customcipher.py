#!/usr/bin/env python3
"""
Enhanced Word Encryption Program
This program allows users to encrypt words using multiple layers of security:
1. Character shuffling based on a derived seed
2. Vigenère cipher encryption
3. Passphrase-based protection (single input for both seed and key)
4. Cryptographic hashing for verification
"""

import hashlib
import base64
import hmac

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
    def run():
        """Run the encryption application."""
        encryptor = WordEncryptor()
        file_encryptor = FileEncryptor()
        
        while True:
            print("\n===== Enhanced Encryption Tool =====")
            print("1. Encrypt a word")
            print("2. Decrypt a word")
            print("3. Encrypt a file")
            print("4. Decrypt a file")
            print("5. Exit")
            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                word = input("Enter the word to encrypt: ")
                if not word:
                    print("Word cannot be empty. Please try again.")
                    continue
                    
                passphrase = input("Enter your passphrase (will be used for decryption): ")
                if not passphrase:
                    print("Passphrase cannot be empty. Please try again.")
                    continue
                
                encrypted, verification_hash = encryptor.encrypt(word, passphrase)
                
                print("\nEncryption Results:")
                print(f"Original word: {word}")
                print(f"Encrypted word: {encrypted}")
                print(f"Verification hash: {verification_hash}")
                print("\nStore both the encrypted word and verification hash to decrypt later.")
                
            elif choice == '2':
                encrypted_word = input("Enter the encrypted word: ")
                if not encrypted_word:
                    print("Encrypted word cannot be empty. Please try again.")
                    continue
                    
                verification_hash = input("Enter the verification hash: ")
                if not verification_hash:
                    print("Verification hash cannot be empty. Please try again.")
                    continue
                    
                passphrase = input("Enter your passphrase: ")
                if not passphrase:
                    print("Passphrase cannot be empty. Please try again.")
                    continue
                
                decrypted_word, is_verified = encryptor.decrypt(encrypted_word, passphrase, verification_hash)
                
                print("\nDecryption Results:")
                print(f"Encrypted word: {encrypted_word}")
                print(f"Decrypted word: {decrypted_word}")
                
                if is_verified:
                    print("\n✅ Verification successful! The decrypted word is authentic.")
                else:
                    print("\n⚠️ Verification failed! Either the passphrase is incorrect or the data has been tampered with.")
            
            elif choice == '3':
                input_path = input("Enter the path of the file to encrypt: ")
                if not input_path:
                    print("File path cannot be empty. Please try again.")
                    continue
                
                output_path = input("Enter the path for the encrypted file: ")
                if not output_path:
                    print("Output path cannot be empty. Please try again.")
                    continue
                
                passphrase = input("Enter your passphrase (will be used for decryption): ")
                if not passphrase:
                    print("Passphrase cannot be empty. Please try again.")
                    continue
                
                print("\nEncrypting file... Please wait.")
                success = file_encryptor.encrypt_file(input_path, output_path, passphrase)
                
                if success:
                    print(f"\n✅ File encrypted successfully and saved to: {output_path}")
                else:
                    print("\n⚠️ File encryption failed. Please check file paths and permissions.")
            
            elif choice == '4':
                input_path = input("Enter the path of the encrypted file: ")
                if not input_path:
                    print("File path cannot be empty. Please try again.")
                    continue
                
                output_path = input("Enter the path for the decrypted file: ")
                if not output_path:
                    print("Output path cannot be empty. Please try again.")
                    continue
                
                passphrase = input("Enter your passphrase: ")
                if not passphrase:
                    print("Passphrase cannot be empty. Please try again.")
                    continue
                
                print("\nDecrypting file... Please wait.")
                success, results = file_encryptor.decrypt_file(input_path, output_path, passphrase)
                
                if success:
                    print(f"\n✅ File decrypted and saved to: {output_path}")
                    
                    if "error" in results:
                        print(f"⚠️ Error: {results['error']}")
                    else:
                        total_lines = results["total"]
                        verified_lines = results["verified"]
                        failed_lines = results["failed"]
                        
                        if total_lines > 0:
                            success_rate = (verified_lines / total_lines) * 100
                            print(f"Verification summary: {verified_lines}/{total_lines} lines verified ({success_rate:.1f}%)")
                            
                            if failed_lines > 0:
                                print(f"⚠️ Warning: {failed_lines} lines failed verification. The passphrase may be incorrect or the file corrupted.")
                else:
                    print("\n⚠️ File decryption failed. Please check if it's a valid encrypted file.")
                
            elif choice == '5':
                print("Thank you for using the Enhanced Encryption Tool. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number from 1-5.")


if __name__ == "__main__":
    EncryptionApp.run()
