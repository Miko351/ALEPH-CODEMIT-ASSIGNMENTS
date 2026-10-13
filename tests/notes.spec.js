import { test, expect } from "@playwright/test";

test("홈의 카운터 증가·초기화와 Link 이동", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await expect(page.getByLabel("현재 숫자")).toHaveText("00");
  await page.getByRole("button", { name: "숫자 올리기" }).click();
  await page.getByRole("button", { name: "숫자 올리기" }).click();
  await expect(page.getByLabel("현재 숫자")).toHaveText("02");
  await page.getByRole("button", { name: "초기화" }).click();
  await expect(page.getByLabel("현재 숫자")).toHaveText("00");
  await page.getByRole("link", { name: "메모 시작하기" }).click();
  await expect(page).toHaveURL(/\/notes$/);
  await expect(page.locator("article[data-note-id]")).toHaveCount(2);
  await page
    .getByRole("navigation")
    .getByRole("link", { name: "홈", exact: true })
    .click();
  await expect(page).toHaveURL(/\/$/);
  expect(errors).toEqual([]);
});

test("같은 내용 두 개를 고유 ID로 구별하고 한쪽만 수정", async ({ page }) => {
  await page.goto("/notes");
  for (let i = 0; i < 2; i++) {
    await page
      .getByLabel("메모 내용", { exact: true })
      .fill("  같은 내용의 메모  ");
    await page.getByRole("button", { name: "메모 등록", exact: true }).click();
  }
  const duplicates = page
    .locator("article[data-note-id]")
    .filter({ hasText: "같은 내용의 메모" });
  await expect(duplicates).toHaveCount(2);
  const firstId = await duplicates.nth(0).getAttribute("data-note-id");
  const secondId = await duplicates.nth(1).getAttribute("data-note-id");
  expect(firstId).not.toBe(secondId);
  await duplicates.nth(0).getByRole("button", { name: /수정$/ }).click();
  await expect(page.getByLabel("메모 내용", { exact: true })).toHaveValue(
    "같은 내용의 메모",
  );
  await page
    .getByLabel("메모 내용", { exact: true })
    .fill("첫 메모만 수정했습니다.");
  await page.getByRole("button", { name: "수정 저장" }).click();
  await expect(
    page.locator(`article[data-note-id="${firstId}"] .note-content`),
  ).toHaveText("첫 메모만 수정했습니다.");
  await expect(
    page.locator(`article[data-note-id="${secondId}"] .note-content`),
  ).toHaveText("같은 내용의 메모");
  await expect(page.locator("article[data-note-id]")).toHaveCount(4);
});

test("공백 등록·수정은 거절하고 원래 메모 보존", async ({ page }) => {
  await page.goto("/notes");
  await page.getByLabel("메모 내용", { exact: true }).fill(" \n\t ");
  await page.getByRole("button", { name: "메모 등록", exact: true }).click();
  await expect(page.locator(".note-compose").getByRole("alert")).toContainText(
    "공백만 입력할 수 없습니다",
  );
  await expect(page.locator("article[data-note-id]")).toHaveCount(2);
  await page.getByRole("button", { name: "메모 1 수정", exact: true }).click();
  await page.getByLabel("메모 내용", { exact: true }).fill(" \n ");
  await page.getByRole("button", { name: "수정 저장" }).click();
  await expect(page.locator(".note-compose").getByRole("alert")).toContainText(
    "공백만 입력할 수 없습니다",
  );
  await expect(
    page.locator('article[data-note-id="note-1"] .note-content'),
  ).toHaveText("배운 내용을 내 말로 정리하기.");
});

test("수정 취소와 삭제 취소는 원래 내용 유지", async ({ page }) => {
  await page.goto("/notes");
  await page.getByRole("button", { name: "메모 1 수정", exact: true }).click();
  await page
    .getByLabel("메모 내용", { exact: true })
    .fill("저장하지 않을 내용");
  await page.getByRole("button", { name: "수정 취소" }).click();
  await expect(
    page.locator('article[data-note-id="note-1"] .note-content'),
  ).toHaveText("배운 내용을 내 말로 정리하기.");
  await page.getByRole("button", { name: "메모 1 삭제", exact: true }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "취소", exact: true })
    .click();
  await expect(page.locator("article[data-note-id]")).toHaveCount(2);
});

test("수정 중인 ID를 삭제하면 해당 메모만 삭제하고 등록 폼으로 복귀", async ({
  page,
}) => {
  await page.goto("/notes");
  await page.getByRole("button", { name: "메모 1 수정", exact: true }).click();
  await page.getByRole("button", { name: "메모 1 삭제", exact: true }).click();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "삭제 확정" })
    .click();
  await expect(page.locator('article[data-note-id="note-1"]')).toHaveCount(0);
  await expect(page.locator('article[data-note-id="note-2"]')).toHaveCount(1);
  await expect(
    page.getByRole("heading", { name: "새 메모 작성", exact: true }),
  ).toBeVisible();
  await expect(page.getByLabel("메모 내용", { exact: true })).toHaveValue("");
  await expect(
    page.getByRole("button", { name: "메모 등록", exact: true }),
  ).toBeVisible();
});

test("빈 목록과 새로고침 초기화, 반응형 화면", async ({ page }, testInfo) => {
  await page.goto("/notes");
  while (await page.locator("article[data-note-id]").count()) {
    await page
      .locator("article[data-note-id]")
      .first()
      .getByRole("button", { name: /삭제$/ })
      .click();
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "삭제 확정" })
      .click();
  }
  await expect(
    page.getByRole("heading", { name: "등록된 메모가 없습니다." }),
  ).toBeVisible();
  await expect(
    page.getByText(
      "작성 칸에서 첫 메모를 남겨 보세요. 새로고침하면 초기 메모로 돌아옵니다.",
      { exact: true },
    ),
  ).toBeVisible();
  await page.reload();
  await expect(page.locator("article[data-note-id]")).toHaveCount(2);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: `.cache/notes-${testInfo.project.name}.png`,
    fullPage: true,
  });
  await page
    .getByRole("navigation")
    .getByRole("link", { name: "홈", exact: true })
    .click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.screenshot({
    path: `.cache/home-${testInfo.project.name}.png`,
    fullPage: true,
  });
});
