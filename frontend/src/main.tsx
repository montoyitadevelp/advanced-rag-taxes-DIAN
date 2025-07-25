import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryProvider } from './providers/QueryProvider.tsx'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
   <QueryProvider>
     <App />
   </QueryProvider>
  </StrictMode>,
)
