
import { Bot, User } from 'lucide-react';
import type { Message } from './types/MessageList';
import { formatTime } from '../../utils/main';

export const MessageList = ({ messages, streamingMessage, isPending }: {
  messages: Message[];
  streamingMessage: string;
  isPending?: boolean;
}) => {

  return (
    <main
      className="flex-1 overflow-y-auto px-2 sm:px-4 py-6 space-y-4">
      {messages.map(msg => (
        <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`flex items-end space-x-2 ${msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'} flex-wrap`}>
            {/* Avatar */}
            <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 
          bg-gray-800 text-white">
              {msg.type === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            {/* Bubble */}
            <div className={`px-4 py-3 rounded-2xl shadow-sm 
          ${msg.type === 'user' ? 'bg-gray-800 text-white rounded-br-md' : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'}
          max-w-[90%] sm:max-w-2xl md:max-w-3xl`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <p className={`text-xs mt-2 ${msg.type === 'user' ? 'text-gray-300' : 'text-gray-500'}`}>
                {formatTime(msg.timestamp)}
              </p>
            </div>
          </div>
        </div>
      ))}

      {/* Streaming / Loading Message */}
      {(isPending || streamingMessage) && (
        <div className="flex justify-start px-2 sm:px-4 py-2">
          <div className="flex items-end space-x-2 flex-wrap">
            <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="px-4 py-3 bg-white rounded-2xl rounded-bl-md shadow-sm border border-gray-200 
          text-sm text-gray-800 leading-relaxed whitespace-pre-wrap min-h-[20px] 
          max-w-[90%] sm:max-w-2xl md:max-w-3xl">
              {streamingMessage || 'Pensando'}
              <span className="inline-block w-0.5 h-4 bg-gray-800 ml-1 animate-pulse" />
            </div>
          </div>
        </div>
      )}
    </main>
  );
};