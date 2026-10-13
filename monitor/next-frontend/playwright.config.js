import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  workers: 1,
  timeout: 90000,
  expect: { timeout: 10000 },
  use: {
    baseURL: process.env.MONITOR_BASE_URL || "http://localhost:8082",
    headless: true,
    trace: "retain-on-failure",
  },
  outputDir: ".cache/playwright",
});
