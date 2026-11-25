import { defineConfig } from '@playwright/test'

const baseURL = 'http://127.0.0.1:4173'

export default defineConfig({
  testDir: './ui-tests',
  outputDir: '.vitepress/ui-check',
  workers: 1,
  use: {
    baseURL,
    browserName: 'chromium',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'python3 -m http.server 4173 --bind 127.0.0.1 --directory .vitepress/dist',
    url: baseURL,
    reuseExistingServer: false,
  },
})
