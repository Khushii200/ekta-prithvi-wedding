import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

// `vite build --mode preview-single` packs the whole site into one HTML file.
export default defineConfig(({ mode }) => ({
  plugins: [react(), ...(mode === 'preview-single' ? [viteSingleFile()] : [])],
  build: {
    outDir: mode === 'preview-single' ? 'dist-single' : 'dist',
    assetsInlineLimit: mode === 'preview-single' ? 100000000 : 4096,
  },
}))
