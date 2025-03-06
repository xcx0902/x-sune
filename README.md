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

## Models Configuration

The application comes with preset models that are used to process chat messages. These models are configured in the `backend.py` file and are mapped to specific providers. Below is an overview of how you can modify them:

### Preset Categories

- **fast**: This model prioritizes speed over accuracy. It is suitable for scenarios where quick responses are more important than detailed ones.
- **accurate**: This model prioritizes accuracy and provides detailed responses. It may take longer to respond compared to the fast model.

### Modifying Models

To modify the existing models or add new ones, you need to update the `PROVIDERS` and `CATEGORY` variables in the `backend.py` file.

1. **Modify Providers**: Add or update entries in the `PROVIDERS` list. Each entry should be a tuple containing the base URL of the API and the model identifier.

   ```python
   PROVIDERS = [
       ("<base_url>", "<model_name>"),
       # Add new providers here
   ]
   ```

2. **Modify Categories**: Add or update entries in the `CATEGORY` dictionary to map model types (e.g., "fast", "accurate") to the appropriate provider index.

   ```python
   CATEGORY = {
       "fast": [],  # Use the index of the provider for the fast model
       "accurate": [],  # Use the index of the provider for the accurate model
       # Add new model categories here
   }
   ```

Ensure that any new models you add are supported by the respective API providers and that you have the necessary API keys configured in the `secret.txt` file.
