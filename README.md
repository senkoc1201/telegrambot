# Telegram Member Adder

This script helps you automatically add members to your Telegram channel.

## Prerequisites

1. Python 3.7 or higher
2. Telegram account with admin privileges in the target channel
3. Telegram API credentials (API_ID and API_HASH)

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get your Telegram API credentials:
   - Go to https://my.telegram.org/auth
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application
   - Copy the API_ID and API_HASH

3. Configure the `.env` file:
   - Copy the `.env` file and rename it to `.env`
   - Fill in your API_ID, API_HASH, phone number, and channel username

## Usage

1. Open `telegram_member_adder.py`
2. In the `user_ids` list, add the Telegram user IDs you want to add to your channel
3. Run the script:
   ```bash
   python telegram_member_adder.py
   ```

## Important Notes

- The script includes delays to avoid rate limiting
- Make sure you have admin privileges in the target channel
- User IDs must be valid and users must not have privacy settings that prevent them from being added to channels
- The script will show a summary of successful and failed additions

## Troubleshooting

If you encounter any issues:
1. Make sure your API credentials are correct
2. Verify that you have admin privileges in the channel
3. Check that the user IDs are valid
4. Ensure your phone number is in the correct format (+countrycode) 