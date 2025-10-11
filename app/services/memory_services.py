from langchain.memory import ConversationBufferWindowMemory

class VirtualGirlfriendMemoryManager:
    def __init__(self):
        self.memory = None

    def get_VirtualGirlfriend_memory(self):
        if self.memory is None:
            self.memory = ConversationBufferWindowMemory(
                k=5,
                return_messages=True,
                input_key="girlfriend_input",
                memory_key="girlfriend_history"
            )
        return self.memory
    
memory_manager = VirtualGirlfriendMemoryManager()

def get_memory_manager():
    return memory_manager