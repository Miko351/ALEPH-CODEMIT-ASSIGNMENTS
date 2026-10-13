import { test, expect } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";

test("두 Compose gateway에서 로그인 기록과 DB 메모를 확인", async ({
  page,
  context,
}) => {
  const general = await context.newPage();
  await general.goto("http://localhost:8081");
  await expect(general).toHaveURL(/\/login$/);
  await general.getByLabel("아이디", { exact: true }).fill("student");
  await general
    .getByLabel("비밀번호", { exact: true })
    .fill("wrong-practice-password");
  await general.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(general.getByRole("alert")).toContainText("올바르지 않습니다");
  await general.getByLabel("비밀번호", { exact: true }).fill("Learn123!");
  await general.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(general).toHaveURL("http://localhost:8081/");
  await expect(
    general.getByRole("link", { name: "+ 새 글 작성" }),
  ).toBeVisible();

  await page.goto("/");
  await page.getByLabel("아이디", { exact: true }).fill("operator");
  await page.getByLabel("비밀번호", { exact: true }).fill("Learn123!");
  await page.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "DB 관찰 메모" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "기록 불러오기" }).click();
  await page
    .getByLabel("경로 · 상태 코드 · 기록 종류 검색")
    .fill("login_failure");
  await expect(page.locator("tbody tr").first()).toContainText("login_failure");
  await expect(page.locator("tbody tr").first()).toContainText("401");
  await page
    .getByLabel("경로 · 상태 코드 · 기록 종류 검색")
    .fill("login_success");
  await expect(page.locator("tbody tr").first()).toContainText("login_success");
  await expect(page.locator("tbody tr").first()).toContainText("200");

  await page.getByLabel("제목", { exact: true }).fill("Docker 점검");
  await page
    .getByLabel("내용", { exact: true })
    .fill("로그인 실패와 성공을 확인했다");
  const savedResponse = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/notes") &&
      response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "DB 저장", exact: true }).click();
  const saved = await savedResponse;
  expect(saved.status()).toBe(201);
  const { note } = await saved.json();
  await expect(page.locator(".db-detail .note-content")).toHaveText(
    "로그인 실패와 성공을 확인했다",
  );
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "DB 관찰 메모" }),
  ).toBeVisible();
  await page
    .locator(".db-list")
    .getByRole("button", { name: /Docker 점검/ })
    .first()
    .click();
  await expect(page.locator(".db-detail .note-content")).toHaveText(
    "로그인 실패와 성공을 확인했다",
  );
  const events = (await (await page.request.get("/api/events")).json()).events;
  const failure = events.find(
    (event) =>
      event.event_kind === "login_failure" && event.status_code === 401,
  );
  const success = events.find(
    (event) =>
      event.event_kind === "login_success" && event.status_code === 200,
  );
  expect(failure).toBeTruthy();
  expect(success).toBeTruthy();
  mkdirSync(".cache", { recursive: true });
  writeFileSync(
    ".cache/runtime-state.json",
    JSON.stringify({ noteId: note.id, eventIds: [failure.id, success.id] }),
  );
  await page.screenshot({
    path: ".cache/compose-dashboard.png",
    fullPage: true,
  });
  console.log(
    `Docker 화면 확인: login_failure/401, login_success/200, 메모 #${note.id} 저장·새로고침 조회`,
  );
});
