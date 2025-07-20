import { Bot } from 'lucide-react';
import { MessageList } from '../messages/MessageList';
import { ChatInput } from './ChatInput';
import { useChatLogicAnswer } from '../../features/answer/hooks/useChatLogicAnswer';

export const ChatContainer = () => {
  const {
    messages,
    inputValue,
    streamingMessage,
    isPending,
    handleSubmit,
    setInputValue,
  } = useChatLogicAnswer();


  return (
    <div className="flex flex-col h-screen bg-gray-50 px-4 sm:px-6 md:px-10 lg:px-20">
      {/* Header */}
      <header className="bg-white border-b px-6 py-4 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Asistente DIAN</h1>
            <p className="text-sm text-gray-600">
              Consultas sobre normativa tributaria en Colombia
            </p>
          </div>
        </div>
      </header>

      {/* Messages */}
      <MessageList
        messages={messages}
        streamingMessage={streamingMessage}
        isPending={isPending}
      />

      {/* Input */}
      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSubmit={handleSubmit}
        disabled={isPending}
      />
    </div>
  );
};
