import { test, expect } from "@playwright/test";
import { randomUUID } from "node:crypto";

test("기존 Flask API의 로그인·DB 메모 CRUD·취소·오류·새로고침 유지", async ({
  page,
}, testInfo) => {
  test.skip(
    !process.env.TEST_USERNAME || !process.env.TEST_PASSWORD,
    "실습 계정 TEST_USERNAME·TEST_PASSWORD 필요",
  );
  const errors = [];
  const createdIds = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => {
    const path = new URL(response.url()).pathname;
    if (path.startsWith("/api/notes"))
      console.log(
        `[DB ${testInfo.project.name}] ${response.request().method()} ${path} -> ${response.status()}`,
      );
  });
  await page.goto("/");
  await page
    .getByRole("navigation")
    .getByRole("link", { name: "DB 메모", exact: true })
    .click();
  await expect(page).toHaveURL(/\/db-notes$/);
  await expect(
    page.getByRole("heading", { name: "DB 메모 로그인" }),
  ).toBeVisible();
  expect((await page.request.get("/api/notes")).status()).toBe(401);
  await page
    .getByLabel("아이디", { exact: true })
    .fill(process.env.TEST_USERNAME);
  await page
    .getByLabel("비밀번호", { exact: true })
    .fill("wrong-test-password");
  await page.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(page.locator(".db-login").getByRole("alert")).toContainText(
    "올바르지 않습니다",
  );
  await page
    .getByLabel("비밀번호", { exact: true })
    .fill(process.env.TEST_PASSWORD);
  await page.getByRole("button", { name: "로그인", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "DB 관찰 메모" }),
  ).toBeVisible();
  const title = `Next.js DB 실습 ${randomUUID().slice(0, 8)}`;
  try {
    await page.getByLabel("제목", { exact: true }).fill(title);
    await page.getByLabel("내용", { exact: true }).fill("   ");
    await page.getByRole("button", { name: "DB 저장", exact: true }).click();
    await expect(page.locator(".db-error")).toContainText("제목과 내용을 확인");
    let listed = await (await page.request.get("/api/notes")).json();
    expect(listed.notes.some((note) => note.title === title)).toBe(false);
    await page
      .getByLabel("내용", { exact: true })
      .fill("  실제 PostgreSQL에 저장할 내용입니다.  ");
    await page
      .getByLabel("처리 상태", { exact: true })
      .selectOption("in_progress");
    await page.getByRole("button", { name: "DB 저장", exact: true }).click();
    await expect(
      page
        .locator(".db-detail")
        .getByRole("heading", { name: title, exact: true }),
    ).toBeVisible();
    listed = await (await page.request.get("/api/notes")).json();
    const id = listed.notes.find((note) => note.title === title).id;
    createdIds.push(id);
    await expect(page.locator(".db-detail .note-content")).toHaveText(
      "실제 PostgreSQL에 저장할 내용입니다.",
    );
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "DB 관찰 메모" }),
    ).toBeVisible();
    await page
      .locator(".db-list")
      .getByRole("button", { name: new RegExp(title) })
      .click();
    await expect(page.locator(".db-detail .note-content")).toHaveText(
      "실제 PostgreSQL에 저장할 내용입니다.",
    );
    await page
      .locator(".db-detail")
      .getByRole("button", { name: "수정", exact: true })
      .click();
    await expect(page.getByLabel("제목", { exact: true })).toHaveValue(title);
    await expect(page.getByLabel("내용", { exact: true })).toHaveValue(
      "실제 PostgreSQL에 저장할 내용입니다.",
    );
    await page.getByLabel("내용", { exact: true }).fill("저장하지 않을 내용");
    await page.getByRole("button", { name: "수정 취소" }).click();
    await expect(page.locator(".db-detail .note-content")).toHaveText(
      "실제 PostgreSQL에 저장할 내용입니다.",
    );
    await page
      .locator(".db-detail")
      .getByRole("button", { name: "수정", exact: true })
      .click();
    await page.getByLabel("내용", { exact: true }).fill(" \n ");
    await page.getByRole("button", { name: "DB 저장", exact: true }).click();
    await expect(page.locator(".db-error")).toContainText("제목과 내용을 확인");
    let detail = await (await page.request.get(`/api/notes/${id}`)).json();
    expect(detail.note.body).toBe("실제 PostgreSQL에 저장할 내용입니다.");
    await page
      .getByLabel("내용", { exact: true })
      .fill("수정 후에도 DB에 남는 내용");
    await page
      .getByLabel("처리 상태", { exact: true })
      .selectOption("completed");
    await page.getByRole("button", { name: "DB 저장", exact: true }).click();
    await expect(page.locator(".db-detail .note-content")).toHaveText(
      "수정 후에도 DB에 남는 내용",
    );
    await page.reload();
    await page
      .locator(".db-list")
      .getByRole("button", { name: new RegExp(title) })
      .click();
    detail = await (await page.request.get(`/api/notes/${id}`)).json();
    expect(detail.note.body).toBe("수정 후에도 DB에 남는 내용");
    console.log(
      `[DB ${testInfo.project.name}] 새로고침 후 수정한 본문과 처리 상태를 API에서 재조회하여 확인`,
    );
    expect(detail.note.status).toBe("completed");
    // Request a genuinely deleted ID from Flask and show its JSON 404 in React.
    const temporary = await (
      await page.request.post("/api/notes", {
        data: { title: "404 검증", body: "임시 메모" },
      })
    ).json();
    createdIds.push(temporary.note.id);
    await page.request.delete(`/api/notes/${temporary.note.id}`);
    await page.route(`**/api/notes/${id}`, (route) =>
      route.continue({
        url: `http://127.0.0.1:3100/api/notes/${temporary.note.id}`,
      }),
    );
    await page
      .locator(".db-list")
      .getByRole("button", { name: new RegExp(title) })
      .click();
    await expect(page.locator(".db-error")).toContainText("찾을 수 없습니다");
    await page.unroute(`**/api/notes/${id}`);
    await page
      .locator(".db-list")
      .getByRole("button", { name: new RegExp(title) })
      .click();
    await page
      .locator(".db-detail")
      .getByRole("button", { name: "삭제", exact: true })
      .click();
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "취소", exact: true })
      .click();
    expect((await page.request.get(`/api/notes/${id}`)).status()).toBe(200);
    await page
      .locator(".db-detail")
      .getByRole("button", { name: "삭제", exact: true })
      .click();
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "삭제 확정" })
      .click();
    await expect(page.locator(".db-list")).not.toContainText(title);
    expect((await page.request.get(`/api/notes/${id}`)).status()).toBe(404);
    expect(
      (
        await page.request.put(`/api/notes/${id}`, {
          data: { title: "제목", body: "내용" },
        })
      ).status(),
    ).toBe(404);
    expect((await page.request.delete(`/api/notes/${id}`)).status()).toBe(404);
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "DB 관찰 메모" }),
    ).toBeVisible();
    await expect(page.locator(".db-list")).not.toContainText(title);
    const afterDelete = await (await page.request.get("/api/notes")).json();
    expect(afterDelete.notes.some((note) => note.id === id)).toBe(false);
    console.log(
      `[DB ${testInfo.project.name}] 삭제 취소: 메모 보존, 삭제 확정: 해당 ID만 삭제, 새로고침 후 API 목록에서 제거 확인`,
    );
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    expect(errors).toEqual([]);
    await page.screenshot({
      path: `.cache/db-notes-${testInfo.project.name}.png`,
      fullPage: true,
    });
  } finally {
    for (const id of createdIds) await page.request.delete(`/api/notes/${id}`);
  }
  await page.getByRole("button", { name: "로그아웃", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "DB 메모 로그인" }),
  ).toBeVisible();
  expect((await page.request.get("/api/notes")).status()).toBe(401);
});
