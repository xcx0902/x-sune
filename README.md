# X-Sune
A chatbot built with FastAPI, OpenAI-SDK and SQLite.

## Features
- User registration and login
- Chat with the AI
- Multiple providers and models
- Save chat history into database

## Configuration

To configure the application, update the `config.json` file with the following details:

- `secret_key`: A secret key for encoding and decoding JWT tokens.
- `models`: An array of model configurations. Each model should have:
  - `url`: The base URL of the API.
  - `name`: The name of the model.
  - `api_key`: The API key for accessing the model.
  - `cookie` (optional): Cookie information if needed for the model.
  - `user_agent` (optional): User agent string for API requests.
- `category`: Configuration for categorizing models, such as:
  - `fast`: An array of model indices for fast responses.
  - `accurate`: An array of model indices for accurate responses.
- `system_prompt`: A string that defines the behavior and identity of the chatbot.

Ensure that the `config.json` file is placed in the root directory of the project and properly formatted as JSON.

For example, you can refer to the `sample_config.json` file for the configuration template.

## Database

The application uses SQLite to manage user data and chat history. The database is initialized with the following tables:

- `users`: Stores user information, including:
  - `id`: An integer that serves as the primary key and auto-increments.
  - `username`: A unique text field for the user's name.
  - `password`: A text field for the user's password.

- `chat_history`: Keeps a record of chat sessions, including:
  - `id`: An integer that serves as the primary key and auto-increments.
  - `username`: The text field indicating which user the chat history belongs to.
  - `role`: A text field indicating the role of the message sender (user or assistant).
  - `content`: A text field containing the actual message content.

After creating the `config.json` file, you can create the `users.db` file and then run `init.sql` to initialize the database and create the required tables.
