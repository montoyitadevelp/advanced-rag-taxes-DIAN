export type Message = {
  id: number;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
};
