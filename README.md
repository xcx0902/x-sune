# X-Sune
A chatbot built with FastAPI, OpenAI-SDK and SQLite.

## Features
- User registration and login
- Chat with the AI
- Multiple providers and models
- Save chat history into database

## Secret Configuration

The `secret.txt` file contains sensitive information required for the application to function securely. It includes keys and tokens that should be kept confidential and not shared publicly. The format of the file is key-value pairs separated by a colon (`:`). Here are the keys included:

- `secret_key`: Used for encoding and decoding JWT tokens.
- `apikey_*`: API keys for different providers.
- `qwen_cookie`: Cookie value used for authenticating with Qwen. Can be empty if you do not use Qwen.

Ensure this file is stored securely and is not exposed in version control systems.
