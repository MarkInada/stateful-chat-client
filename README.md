# stateful-chat-client

Conversation Logger for MongoDB

A Python package to facilitate recording and retrieving AI conversations from a MongoDB database.

## Features

- Record conversations to MongoDB in real-time.
- Retrieve past conversations from the database.
- Organize conversations based on unique thread IDs.

## Installation

To install the package, use pip:

```sh
pip install stateful-chat-client
```

## Quickstart

1. Setting up the logger
    ```python
    from stateful_chat_client import ConversationLogger

    logger = ConversationLogger(host='localhost', port=27017,    database_name='conversation_database', collection_name='conversations')
    ```
2. Recording a conversation
    ```python
    from stateful_chat_client.conversation_logger import record_conversation
    from langchain.llms import OpenAI
    from langchain.chains import ConversationChain
    from langchain.chains.conversation.memory import ConversationBufferMemory

    conversation = ConversationChain(
        llm=OpenAI(),
        memory=ConversationBufferMemory(),
        verbose=True,
    )
    conversation.predict(input="Hello!")
    thread_id = str(uuid.uuid4())
    messages = conversation.memory.buffer_as_messages
    record_conversation(messages, thread_id, logger=logger)
    ```
3. Retrieve past conversations and save to memory
    ```python
    from stateful_chat_client.conversation_logger import retrieve_and_save_to_memory

    new_conversation = ConversationChain(
        llm=OpenAI(),
        memory=ConversationBufferMemory(),
        verbose=True,
    )
    new_conversation = retrieve_and_save_to_memory(thread_id, new_conversation_instance, logger=logger)
    new_conversation.predict(input="Hello! What did I say first?")
    ```

## Requirements

- MongoDB server (local or remote)
- Python 3.8.1 or newer
