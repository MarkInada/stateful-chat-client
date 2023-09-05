# slack example

## Requirement

Create slack token [follwing steps](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started#tokens-and-installing-apps).

- SLACK_BOT_TOKEN
- SLACK_APP_TOKEN

※ Required Bot Token Scopes: app_mentions:read, channels:history, chat:write, files:read, groups:history, im:history, mpim:history

※ Required User Token Scopes: chat:write

※ Required Subscribe to bot events: message.channels, message.groups, message.im, message.mpim, app_mention

Create openai api key [follwing steps](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

- OPENAI_API_KEY
- OPENAI_ORG

Create Mongo DB. (Easiest way is to just run `docker run --rm --name mongodb -p 27017:27017 -d mongo:latest`)

- MONGO_HOST
- MONGO_PORT

## Quickstart

Follow these steps to quickly set up and run the heptapods:

1. Install python3.10, if not already installed.
2. Clone the repository: `git clone https://github.com/MarkInada/stateful-chat-client.git`
3. Navigate to the cloned repository directory: `cd /path/to/stateful-chat-client/example/slack`
4. Install poetry: `pip install poetry`
5. Create a new virtual environment with Python 3.10: `poetry env use python3.10`
6. Activate the virtual environment: `poetry shell`
7. Install app dependencies: `poetry install`
8. Set the required environment variables in `.env` (see `sample.env`):

    ```
    SLACK_BOT_ID=
    SLACK_BOT_TOKEN=
    SLACK_APP_TOKEN=
    OPENAI_API_KEY=
    OPENAI_ORG=
    MONGO_HOST=
    MONGO_PORT=
    ```

9.  Run the API locally: `poetry run python main.py`
