import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(async ({ command }) => {
  const plugins = [react(), tailwindcss()]
  
  if (command === 'serve') {
    const mkcert = (await import('vite-plugin-mkcert')).default
    plugins.push(mkcert())
  }

  return {
    plugins,
    server: {
      https: true
    }
  }
})
