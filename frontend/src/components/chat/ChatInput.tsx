import { Send } from 'lucide-react';

export const ChatInput = ({
  value,
  onChange,
  onSubmit,
  disabled
}: {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  disabled: boolean;
}) => {
  return (
    <footer className="bg-white border-t px-4 py-4">
      <form onSubmit={(e) => { e.preventDefault(); onSubmit(); }} className="max-w-4xl mx-auto flex items-center space-x-3">
        <input
          type="text"
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder="Escribe tu consulta tributaria..."
          className="flex-1 px-4 py-3 pr-12 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={!value.trim() || disabled}
          className="w-10 h-10 bg-gray-800 hover:bg-gray-700 rounded-md flex items-center justify-center transition disabled:opacity-50"
        >
          <Send className="w-4 h-4 text-white" />
        </button>
      </form>
    </footer>
  );
};