from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from stateful_chat_client import ConversationLogger
from stateful_chat_client.conversation_logger import record_conversation, retrieve_and_save_to_memory
import os
from dotenv import load_dotenv

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
logger = ConversationLogger(host=os.environ["MONGO_HOST"], port=int(os.environ["MONGO_PORT"]),
                            database_name='conversation_database', collection_name='conversations')

@app.event("message")
def handle_message_events(body, logger):
    """
    handler received
    """
    logger.info(body)
    return None

@app.event("app_mention")
def llm_reply(event, say):
    """
    handler mentioned
    """
    input_message = event["text"]
    thread_ts = event.get("thread_ts") or None
    channel = event["channel"]

    slack_id = os.environ["SLACK_BOT_ID"]
    input_message = input_message.replace(f"<@{slack_id}>", "")

    if thread_ts is not None: # reply in thread
        # get thread id
        parent_thread_ts = event["thread_ts"]

        # define conversation
        conversation = ConversationChain(
            llm=OpenAI(),
            memory=ConversationBufferMemory(),
            verbose=True,
        )

        # retrive all conversation history
        conversation = retrieve_and_save_to_memory(parent_thread_ts, conversation, logger=logger)

        # reply message in slack thread
        reply_message = conversation.predict(input=input_message)
        say(text=reply_message, thread_ts=parent_thread_ts, channel=channel)

        # record last conversation
        messages = conversation.memory.buffer_as_messages
        record_conversation(messages, thread_ts, logger=logger)
    else: # create thread
        # get thread id
        response = app.client.conversations_replies(channel=channel, ts=event["ts"])
        thread_ts = response["messages"][0]["ts"]

        # define conversation
        conversation = ConversationChain(
            llm=OpenAI(),
            memory=ConversationBufferMemory(),
            verbose=True,
        )

        # reply message in slack thread
        reply_message = conversation.predict(input=input_message)
        say(text=reply_message, thread_ts=thread_ts, channel=channel)

        # record last conversation
        messages = conversation.memory.buffer_as_messages
        record_conversation(messages, thread_ts, logger=logger)

def run():
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()