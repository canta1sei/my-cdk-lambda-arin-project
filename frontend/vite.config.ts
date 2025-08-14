import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiEndpoint = env.VITE_API_ENDPOINT_URL;

  if (!apiEndpoint) {
    throw new Error('VITE_API_ENDPOINT_URL is not defined. Please create a .env file and define it there.');
  }

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: apiEndpoint,
          changeOrigin: true,
          // The backend is at the root of the stage, so remove the /api prefix
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})