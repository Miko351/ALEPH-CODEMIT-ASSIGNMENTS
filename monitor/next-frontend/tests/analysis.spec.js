import { test, expect } from "@playwright/test";
import { spawnSync } from "node:child_process";
import { resolve, join } from "node:path";
import { mkdirSync, writeFileSync } from "node:fs";

const root = resolve(process.cwd(), "../..");
function learningCommand(module, count) {
  const docker =
    process.env.DOCKER_BINARY ||
    (process.platform === "win32"
      ? join(
          process.env.LOCALAPPDATA,
          "Programs/DockerDesktop/resources/bin/docker.exe",
        )
      : "docker");
  const args = [
    "compose",
    "--env-file",
    process.env.ANALYSIS_ENV_FILE || join(root, ".env"),
    "-f",
    process.env.ANALYSIS_COMPOSE_FILE || join(root, "compose-monitor.yaml"),
    "exec",
    "-T",
    "-e",
    "CAPTURE_PASSWORD",
    "monitor-api",
    "python",
    "-m",
    module,
  ];
  if (count !== undefined) args.push(String(count));
  const result = spawnSync(docker, args, {
    encoding: "utf8",
    timeout: 30000,
    env: {
      ...process.env,
      CAPTURE_PASSWORD: process.env.TEST_ACCOUNT_PASSWORD,
    },
  });
  expect(result.status, result.stderr).toBe(0);
  return JSON.parse(result.stdout);
}
function capture(count) {
  const observation = learningCommand("learning.capture_case", count);
  const folder = join(root, "monitor/backend/learning/data");
  mkdirSync(folder, { recursive: true });
  writeFileSync(
    join(folder, "observation.json"),
    JSON.stringify(observation, null, 2),
  );
  return observation;
}

test("실제 4/12/10회 요청: 파일·화면·같은 근거·새 관찰을 검증", async ({
  page,
}) => {
  test.skip(
    !process.env.TEST_ACCOUNT_PASSWORD,
    "Set TEST_ACCOUNT_PASSWORD for real local capture.",
  );
  const four = capture(4);
  expect(four.records).toHaveLength(5);
  expect(
    four.records.filter((row) => row.event_type === "post_list"),
  ).toHaveLength(4);
  expect(learningCommand("learning.lesson2").normalized_count).toBe(5);
  expect(learningCommand("learning.lesson3").view_count).toBe(4);
  expect(learningCommand("learning.lesson3").candidate).toBe(false);

  await page.goto("/");
  await page.getByLabel("아이디", { exact: true }).fill("operator");
  await page
    .getByLabel("비밀번호", { exact: true })
    .fill(process.env.TEST_ACCOUNT_PASSWORD);
  await page.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "HTTP 조회 분석" }),
  ).toBeVisible();
  const panel = page.getByRole("region", { name: "HTTP 조회 분석" });
  async function begin() {
    await panel.getByRole("button", { name: "새 관찰 시작" }).click();
    await expect(
      panel.getByRole("button", { name: "결과 불러오기" }),
    ).toBeEnabled();
  }
  async function load() {
    const received = page.waitForResponse((response) =>
      response.url().includes("/api/analysis?"),
    );
    await panel.getByRole("button", { name: "결과 불러오기" }).click();
    const response = await received;
    expect(response.status()).toBe(200);
    return response.json();
  }
  await begin();
  const twelve = capture(12);
  const first = await load();
  expect(first.cards).toHaveLength(1);
  await expect(panel.getByTestId("analysis-count")).toHaveText("12");
  await expect(panel.getByTestId("analysis-verdict")).toHaveText("검토 후보");
  await expect(panel.getByTestId("analysis-evidence-count")).toHaveText("13");
  expect(first.cards[0].evidence).toEqual(
    twelve.records.map((row) => "http-" + row.id),
  );
  await panel.locator("summary").click();
  await expect(
    panel.getByRole("table", { name: "분석 원본 근거" }).locator("tbody tr"),
  ).toHaveCount(13);
  await panel.getByLabel("비교 기준").fill("20");
  const second = await load();
  expect(second.after_id).toBe(first.after_id);
  expect(second.reference_time).toBe(first.reference_time);
  expect(second.cards[0].evidence).toEqual(first.cards[0].evidence);
  await expect(panel.getByTestId("analysis-count")).toHaveText("12");
  await expect(panel.getByTestId("analysis-verdict")).toHaveText("기준 미해당");
  await panel.getByLabel("비교 기준").fill("10");
  await load();
  await expect(panel.getByTestId("analysis-verdict")).toHaveText("검토 후보");

  await begin();
  capture(10);
  await load();
  await expect(panel.getByTestId("analysis-count")).toHaveText("10");
  await expect(panel.getByTestId("analysis-verdict")).toHaveText("검토 후보");
  await expect(panel.getByTestId("analysis-evidence-count")).toHaveText("11");
  const beforeEmpty = (await (await page.request.get("/api/events")).json())
    .events.length;
  await begin();
  const empty = await load();
  expect(empty.cards[0].observed_value).toBe(0);
  expect(empty.cards[0].records).toEqual([]);
  expect(
    (await (await page.request.get("/api/events")).json()).events,
  ).toHaveLength(beforeEmpty);
  await begin();
  capture(12);
  await load();
  await expect(panel.getByTestId("analysis-count")).toHaveText("12");
  await expect(panel.getByTestId("analysis-evidence-count")).toHaveText("13");
  mkdirSync(".cache", { recursive: true });
  await panel.screenshot({ path: ".cache/http-analysis.png" });
  console.log('Real capture: 4→5 raw, 12→13 evidence; 10/20 preserves IDs/time; boundary 10→11; new observation 0 with old rows retained.');
});
