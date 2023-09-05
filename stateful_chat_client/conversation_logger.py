from . import ConversationLogger

def record_conversation(messages, thread_id, logger=None):
    if logger is None:
        logger = ConversationLogger()

    logger.insert_conversation_exchange(messages[-2:], thread_id)

def retrieve_and_save_to_memory(thread_id, new_conversation, logger=None):
    if logger is None:
        logger = ConversationLogger()

    conversations_in_thread = logger.get_conversations_by_thread_id(thread_id)
    for i, c in enumerate(conversations_in_thread):
        sender = 'human' if i % 2 == 0 else 'ai'
        if sender == 'ai' and i > 0:
            new_conversation.memory.save_context(
                {"input": conversations_in_thread[i-1]['human']['content']},
                {"output": conversations_in_thread[i]['ai']['content']}
            )
    return new_conversation
