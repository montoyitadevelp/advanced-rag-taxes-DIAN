import { useMutation } from '@tanstack/react-query';
import type { AnswerResponse } from './types/useChatAnswer';
import { api } from '../../../utils/api';

/**
 * Custom React hook that provides a mutation for submitting a question and receiving an answer.
 *
 * Utilizes `useMutation` from React Query to handle the asynchronous API call to the `/answer/create` endpoint.
 * The mutation function sends a POST request with the provided question and expects an `AnswerResponse` in return.
 *
 * @returns {UseMutationResult<AxiosResponse<AnswerResponse>, unknown, string>} 
 *   The mutation object from React Query, which includes methods and state for managing the mutation.
 */
export const useCreateAnswer = () => {
  return useMutation({
    mutationFn: async (question: string) => {
      return await api.post<AnswerResponse>('/answer/create', { question });
    },
  });
};
