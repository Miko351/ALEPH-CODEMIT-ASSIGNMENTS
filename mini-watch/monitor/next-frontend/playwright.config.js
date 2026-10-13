import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests",
  reporter: "list",
  outputDir: ".cache/test-results",
  use: {
    baseURL: "http://127.0.0.1:3101",
    locale: "ko-KR",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "desktop",
      use: { browserName: "chromium", viewport: { width: 1440, height: 1000 } },
    },
    {
      name: "mobile",
      use: { browserName: "chromium", viewport: { width: 390, height: 844 } },
    },
  ],
  webServer: {
    command:
      "node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port 3101",
    url: "http://127.0.0.1:3101",
    reuseExistingServer: false,
    timeout: 120000,
  },
});
