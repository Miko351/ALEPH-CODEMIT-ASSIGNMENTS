import { test, expect } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { randomUUID } from "node:crypto";

test("두 Compose gateway에서 로그인 기록과 DB 메모를 확인", async ({
  page,
  context,
}) => {
  test.skip(
    !process.env.TEST_ACCOUNT_PASSWORD,
    "Set TEST_ACCOUNT_PASSWORD for local test accounts.",
  );
  const generalBase = process.env.GENERAL_BASE_URL || "http://localhost:8081";
  const general = await context.newPage();
  await general.goto(generalBase);
  await expect(general).toHaveURL(/\/login$/);
  await general.getByLabel("아이디", { exact: true }).fill("student");
  await general
    .getByLabel("비밀번호", { exact: true })
    .fill("wrong-practice-password");
  await general.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(general.getByRole("alert")).toContainText("올바르지 않습니다");
  await general
    .getByLabel("비밀번호", { exact: true })
    .fill(process.env.TEST_ACCOUNT_PASSWORD);
  await general.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(general).toHaveURL(generalBase + "/");
  await expect(
    general.getByRole("link", { name: "+ 새 글 작성" }),
  ).toBeVisible();

  await page.goto("/");
  await page.getByLabel("아이디", { exact: true }).fill("operator");
  await page
    .getByLabel("비밀번호", { exact: true })
    .fill(process.env.TEST_ACCOUNT_PASSWORD);
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

test("Waitress·Next 프록시의 게시글/메모 수정·삭제·CSRF·DB 유지", async ({
  page,
}) => {
  test.skip(!process.env.TEST_ACCOUNT_PASSWORD, "Set TEST_ACCOUNT_PASSWORD.");
  const general = process.env.GENERAL_BASE_URL || "http://localhost:8081";
  const password = process.env.TEST_ACCOUNT_PASSWORD;
  expect(
    (
      await page.request.post(general + "/auth/login", {
        data: { username: "student", password },
      })
    ).status(),
  ).toBe(200);
  const title = "클라우드 CRUD " + randomUUID().slice(0, 8);
  const created = await page.request.post(general + "/board/new", {
    form: { title, body: "저장 본문" },
    maxRedirects: 0,
  });
  expect(created.status()).toBe(303);
  const detailPath = created.headers().location;
  expect(await (await page.request.get(general + detailPath)).text()).toContain(
    "저장 본문",
  );
  expect(
    (
      await page.request.post(general + detailPath + "/edit", {
        form: { title: title + " 수정", body: "수정 본문" },
        maxRedirects: 0,
      })
    ).status(),
  ).toBe(303);
  expect(await (await page.request.get(general + detailPath)).text()).toContain(
    "수정 본문",
  );
  expect(
    (await page.request.get(general + detailPath + "/delete")).status(),
  ).toBe(200);
  expect(
    (
      await page.request.post(general + detailPath + "/delete", {
        maxRedirects: 0,
      })
    ).status(),
  ).toBe(303);
  expect((await page.request.get(general + detailPath)).status()).toBe(404);

  const anonymous = await (await page.request.get("/api/auth/me")).json();
  const login = await page.request.post("/api/auth/login", {
    data: { username: "operator", password },
    headers: { "X-CSRF-Token": anonymous.csrf_token },
  });
  expect(login.status()).toBe(200);
  const headers = { "X-CSRF-Token": (await login.json()).csrf_token };
  const saved = await page.request.post("/api/notes", {
    data: { title, body: "메모 본문", status: "pending" },
    headers,
  });
  expect(saved.status()).toBe(201);
  const id = (await saved.json()).note.id;
  try {
    expect(
      (
        await page.request.put(`/api/notes/${id}`, {
          data: { title, body: "수정" },
        })
      ).status(),
    ).toBe(403);
    expect(
      (
        await page.request.put(`/api/notes/${id}`, {
          data: { title: " ", body: "수정" },
          headers,
        })
      ).status(),
    ).toBe(400);
    expect(
      (await (await page.request.get(`/api/notes/${id}`)).json()).note.body,
    ).toBe("메모 본문");
    expect(
      (
        await page.request.put(`/api/notes/${id}`, {
          data: { title, body: "DB 수정 본문", status: "completed" },
          headers,
        })
      ).status(),
    ).toBe(200);
    await page.goto("/notes");
    await page
      .locator(".db-list")
      .getByRole("button", { name: new RegExp(title) })
      .click();
    await expect(page.locator(".db-detail .note-content")).toHaveText(
      "DB 수정 본문",
    );
    await page.reload();
    const reread = (await (await page.request.get(`/api/notes/${id}`)).json())
      .note;
    expect(reread.body).toBe("DB 수정 본문");
    expect(reread.status).toBe("completed");
    expect(
      (await page.request.delete(`/api/notes/${id}`, { headers })).status(),
    ).toBe(200);
    expect((await page.request.get(`/api/notes/${id}`)).status()).toBe(404);
  } finally {
    await page.request.delete(`/api/notes/${id}`, { headers });
  }
});
