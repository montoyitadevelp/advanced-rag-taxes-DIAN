import React from "react";
import type { Message } from "../../../components/messages/types/MessageList";
import { createBotMessage, createUserMessage, handleChatSuccess} from "../helpers/chat";
import { useCreateAnswer } from "./useCreateAnswer";

export const useChatLogicAnswer = () => {
  const { mutate: sendQuestion, isPending } = useCreateAnswer();
  const [messages, setMessages] = React.useState<Message[]>([createBotMessage('¡Hola! Soy tu asistente especializado en normativa tributaria de la DIAN. ¿En qué puedo ayudarte?')]);
  const [inputValue, setInputValue] = React.useState('');
  const [streamingMessage, setStreamingMessage] = React.useState('');


  const handleSubmit = () => {
    if (!inputValue.trim() || isPending) return;

    const userMessage = createUserMessage(inputValue);
    setMessages(prev => [...prev, userMessage]);

    const userQuestion = inputValue;
    setInputValue('');
    setStreamingMessage('');

    sendQuestion(userQuestion, {
      onSuccess: (data) => handleChatSuccess(
        data.answer,
        setStreamingMessage,
        (message) => setMessages(prev => [...prev, message])
      ),
      onError: () => setStreamingMessage('❌ Hubo un error al procesar tu solicitud.')
    });
  };

  return {
    inputValue,
    setInputValue,
    messages,
    streamingMessage,

    handleSubmit,
    isPending
  };
}
