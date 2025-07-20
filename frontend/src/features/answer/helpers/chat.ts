import type { Message } from "../../../components/messages/types/MessageList";
import { simulateStreaming } from "../../../utils/streaming";


export const createUserMessage = (content: string): Message => ({
  id: Date.now(),
  type: 'user',
  content,
  timestamp: new Date(),
});

export const createBotMessage = (content: string): Message => ({
  id: Date.now() + 1,
  type: 'bot',
  content,
  timestamp: new Date(),
});


export const handleChatSuccess = async (
  answer: string,
  setStreamingMessage: (value: string) => void,
  appendMessage: (message: Message) => void
) => {
  const finalMessage = await simulateStreaming(answer, setStreamingMessage);
  appendMessage(createBotMessage(finalMessage));
  setStreamingMessage('');
};
