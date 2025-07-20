export const simulateStreaming = async (
  text: string,
  update: (chunk: string) => void
): Promise<string> => {
  let display = '';
  for (const word of text.split(' ')) {
    display += word + ' ';
    update(display.trim());
    await new Promise(res => setTimeout(res, word.length > 6 ? 100 : 40));
  }
  return display.trim();
};
