import { defineConfig, devices } from "@playwright/test";
import path from "node:path";

const backend = path.resolve(__dirname, "../backend");
const python = path.join(
  backend,
  ".venv",
  process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
);

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  workers: 1,
  reporter: "list",
  use: { baseURL: "http://127.0.0.1:3001", trace: "retain-on-failure" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    {
      name: "mobile",
      use: { ...devices["Pixel 7"], defaultBrowserType: "chromium" },
    },
  ],
  webServer: [
    {
      command: `"${python}" "${path.join(backend, "scripts/run_e2e.py")}"`,
      url: "http://127.0.0.1:8001/api/health",
      reuseExistingServer: false,
      timeout: 30000,
    },
    {
      command: "npm run dev -- --port 3001",
      url: "http://127.0.0.1:3001",
      env: {
        NEXT_PUBLIC_API_URL: "http://127.0.0.1:8001",
        NEXT_TELEMETRY_DISABLED: "1",
      },
      reuseExistingServer: false,
      timeout: 120000,
    },
  ],
});
