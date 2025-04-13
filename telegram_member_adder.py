import os
import time
import csv
import getpass
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.errors import UserPrivacyRestrictedError, FloodWaitError, SessionPasswordNeededError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')  # Your phone number with country code

# Channel username or ID
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

def read_members_from_csv(csv_file):
    """
    Read member information from CSV file
    Returns a list of usernames
    """
    usernames = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            # Skip the header row
            next(file)
            for line in file:
                # Split the line by comma and take the username
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[1]:  # Check if username exists
                    username = parts[1].strip()
                    if username:  # Make sure username is not empty
                        usernames.append(username)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        raise
    
    print(f"Successfully read {len(usernames)} usernames from CSV")
    return usernames

async def add_members(client, channel, usernames):
    """
    Add members to the specified channel using usernames
    """
    added_count = 0
    failed_count = 0
    privacy_restricted = 0
    
    # Get the channel entity properly
    try:
        channel_entity = await client.get_entity(channel)
        channel_input = InputPeerChannel(channel_entity.id, channel_entity.access_hash)
    except Exception as e:
        print(f"Error getting channel entity: {str(e)}")
        return added_count, failed_count, privacy_restricted
    
    for username in usernames:
        try:
            # Get user entity by username
            try:
                user = await client.get_entity(username)
                user_input = InputPeerUser(user.id, user.access_hash)
            except ValueError:
                print(f"Could not find user with username {username}")
                failed_count += 1
                continue
            
            # Add the user to the channel
            await client(InviteToChannelRequest(
                channel=channel_input,
                users=[user_input]
            ))
            
            print(f"Successfully added user {username}")
            added_count += 1
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
        except UserPrivacyRestrictedError:
            print(f"User {username} has privacy settings enabled")
            privacy_restricted += 1
            time.sleep(2)
        except FloodWaitError as e:
            print(f"Rate limit hit. Waiting for {e.seconds} seconds...")
            time.sleep(e.seconds)
        except Exception as e:
            print(f"Failed to add user {username}: {str(e)}")
            failed_count += 1
            time.sleep(5)  # Longer delay on failure
    
    return added_count, failed_count, privacy_restricted

async def main():
    # Create the client and connect
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    try:
        print("\nStarting Telegram authentication...")
        print("If you have 2FA enabled, you will be asked for your password.")
        print("Note: The password field will not show any characters as you type (this is normal for security).")
        
        # Start the client with phone number
        await client.start(phone=PHONE)
        
        # Get the channel entity
        channel = await client.get_entity(CHANNEL_USERNAME)
        
        # Read usernames from CSV file
        usernames = read_members_from_csv('dom_mem.csv')
        print(f"\nFound {len(usernames)} usernames to process")
        
        # Add members
        added, failed, privacy_restricted = await add_members(client, channel, usernames)
        
        print(f"\nSummary:")
        print(f"Successfully added: {added} members")
        print(f"Failed to add: {failed} members")
        print(f"Privacy restricted: {privacy_restricted} members")
        
    except SessionPasswordNeededError:
        print("\n2FA Password required!")
        print("Please enter your 2FA password below.")
        print("Note: The password field will not show any characters as you type.")
        password = getpass.getpass("Enter your 2FA password: ")
        await client.sign_in(password=password)
        
        # Continue with the rest of the process
        channel = await client.get_entity(CHANNEL_USERNAME)
        usernames = read_members_from_csv('dom_mem.csv')
        print(f"\nFound {len(usernames)} usernames to process")
        added, failed, privacy_restricted = await add_members(client, channel, usernames)
        
        print(f"\nSummary:")
        print(f"Successfully added: {added} members")
        print(f"Failed to add: {failed} members")
        print(f"Privacy restricted: {privacy_restricted} members")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 