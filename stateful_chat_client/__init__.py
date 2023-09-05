from pymongo import MongoClient
from datetime import datetime

class ConversationLogger:
    def __init__(self, host='localhost', port=27017, database_name='conversation_database', collection_name='conversations'):
        self.client = MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def _insert_single_message(self, message, sender, thread_id):
        entry = {
            'timestamp': datetime.now(),
            'thread_id': thread_id,
            sender: {
                'content': message.content,
                'additional_kwargs': message.additional_kwargs,
                'example': False
            }
        }
        self.collection.insert_one(entry)

    def insert_conversation_exchange(self, messages, thread_id):
        for i, message in enumerate(messages):
            self._insert_single_message(message, message.type, thread_id)

    def get_conversations_by_thread_id(self, thread_id):
        return list(self.collection.find({"thread_id": thread_id}))
