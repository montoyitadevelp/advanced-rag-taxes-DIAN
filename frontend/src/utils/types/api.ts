type Methods = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface RequestOptions {
  method?: Methods;
  headers?: Record<string, string>;
  body?: any;
  params?: Record<string, string | number>;
};
