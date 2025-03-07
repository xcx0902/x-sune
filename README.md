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
