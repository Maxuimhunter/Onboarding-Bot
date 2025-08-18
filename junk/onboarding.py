import os
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from .env
DISCORD_WEBHOOK = os.getenv('DISCORD_TOKEN')
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma3')

# Validate Discord webhook if provided
if DISCORD_WEBHOOK and not DISCORD_WEBHOOK.startswith('https://discord.com/api/webhooks/'):
    print("[!] Warning: DISCORD_TOKEN in .env doesn't appear to be a valid Discord webhook URL.")
    print("   Discord notifications will be disabled. To enable them, please update .env with a valid webhook URL.")
    DISCORD_WEBHOOK = None

def get_valid_input(prompt, input_type=str, min_length=1, default=None):
    """Helper function to get and validate user input
    
    Args:
        prompt: The prompt to display to the user
        input_type: The expected type of input (str, int, etc.)
        min_length: Minimum length of input required
        default: Default value to return if input can't be read (for testing)
    """
    while True:
        try:
            try:
                user_input = input(prompt).strip()
            except EOFError:
                if default is not None:
                    print(f"Using default value: {default}")
                    return default
                print("\nInput cancelled. Please try again.")
                continue
                
            if len(user_input) < min_length:
                print(f"Input must be at least {min_length} character(s) long.")
                continue
                
            if input_type == int:
                try:
                    return int(user_input)
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                    
            return user_input
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            if default is not None:
                return default
            continue

def save_to_excel(data, filename="onboarding_data.xlsx"):
    """Save onboarding data to an Excel file"""
    try:
        # Check if file exists to append or create new
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            new_df = pd.DataFrame([data])
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            df = pd.DataFrame([data])
        
        # Save to Excel
        df.to_excel(filename, index=False)
        print(f"\nData successfully saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return False

def send_discord_notification(message):
    """Send notification to Discord webhook"""
    if not DISCORD_WEBHOOK:
        print("Discord webhook not configured. Skipping notification.")
        return False
        
    try:
        response = requests.post(
            DISCORD_WEBHOOK,
            json={"content": message}
        )
        if response.status_code == 204:
            print("Notification sent to Discord successfully!")
            return True
        else:
            print(f"Failed to send Discord notification. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending Discord notification: {e}")
        return False

def handle_document_upload(test_mode=False):
    """Handle document upload/scanning
    
    Args:
        test_mode: If True, automatically skips document upload
    """
    if test_mode:
        print("Test mode: Skipping document upload")
        return "test_document.pdf"
        
    while True:
        try:
            print("\nDocument Upload:")
            print("1. Upload document")
            print("2. Scan document")
            print("3. Skip for now")
            
            try:
                choice = input("Enter your choice (1-3): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nReturning to main menu...")
                return None
                
            if choice == '1':
                try:
                    file_path = input("Enter the path to your document: ").strip()
                    if os.path.exists(file_path):
                        print(f"File '{os.path.basename(file_path)}' uploaded successfully!")
                        return file_path
                    print("File not found. Please check the path and try again.")
                except (EOFError, KeyboardInterrupt):
                    print("\nDocument upload cancelled.")
                    continue
                    
            elif choice == '2':
                print("\nPlease prepare your document for scanning...")
                # In a real implementation, you would integrate with a scanning library here
                print("Document scanned successfully!")
                return "scanned_document.pdf"  # Placeholder
                
            elif choice == '3':
                print("Skipping document upload.")
                return None
                
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            if test_mode:
                return None

def main(test_mode=False):
    """Main function to run the onboarding process
    
    Args:
        test_mode: If True, uses test data and skips interactive prompts
    """
    print("=== Employee Onboarding System ===\n")
    
    # Test data for non-interactive mode
    test_data = {
        'full_name': 'Test User',
        'employee_id': 'EMP123',
        'kra_number': 'A123456789X'
    } if test_mode else {}
    
    # Collect basic information
    full_name = get_valid_input(
        "Enter your full name: ", 
        min_length=3,
        default=test_data.get('full_name')
    )
    employee_id = get_valid_input(
        "Enter your employee ID: ", 
        min_length=1,
        default=test_data.get('employee_id')
    )
    kra_number = get_valid_input(
        "Enter your KRA number: ", 
        min_length=1,
        default=test_data.get('kra_number')
    )
    
    # Verify KRA (commented out as requested)
    # is_valid, message = verify_kra(kra_number)
    # print(f"KRA Verification: {message}")
    # if not is_valid:
    #     print("Please correct your KRA number and try again.")
    #     return
    
    # Document upload
    document_path = handle_document_upload(test_mode=test_mode)
    
    # Prepare data for saving
    onboarding_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'full_name': full_name,
        'employee_id': employee_id,
        'kra_number': kra_number,
        'document_uploaded': 'Yes' if document_path else 'No',
        'document_path': document_path or 'N/A'
    }
    
    # Save to Excel and send notification
    if save_to_excel(onboarding_data):
        print("\n=== Onboarding Summary ===")
        summary = []
        for key, value in onboarding_data.items():
            if key != 'document_path' or value != 'N/A':
                line = f"{key.replace('_', ' ').title()}: {value}"
                print(line)
                summary.append(line)
        
        # Send Discord notification
        discord_message = "New onboarding submission!\n" + "\n".join(summary)
        send_discord_notification(discord_message)
    else:
        error_msg = "There was an error saving the onboarding information."
        print(f"\n{error_msg}")
        send_discord_notification(f"❌ {error_msg}")

if __name__ == "__main__":
    import sys
    test_mode = '--test' in sys.argv
    main(test_mode=test_mode)
