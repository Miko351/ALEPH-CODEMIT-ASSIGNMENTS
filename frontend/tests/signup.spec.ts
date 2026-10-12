import { test, expect, type Page } from "@playwright/test";

const password = "my-safe-password-123";
async function fillForm(page: Page, email: string) {
  await page.getByLabel("이름", { exact: false }).fill("김아름");
  await page.getByLabel("이메일", { exact: false }).fill(email);
  await page.locator("#password").fill(password);
  await page.locator("#confirmation").fill(password);
}

test("등록 성공과 정규화된 이메일 중복을 실제 API로 처리한다", async ({
  page,
}, testInfo) => {
  const email = `e2e-${testInfo.project.name}-${Date.now()}@example.com`;
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await fillForm(page, email);
  await page.screenshot({
    path: testInfo.outputPath("signup.png"),
    fullPage: true,
  });
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("김아름님, 환영합니다!");
  await expect(page.locator("#password")).toHaveCount(0);
  await page.getByRole("button", { name: "다른 계정 가입하기" }).click();
  await expect(page.locator("#password")).toHaveValue("");
  await fillForm(page, email.toUpperCase());
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.locator("form").getByRole("alert")).toContainText(
    "이미 가입된 이메일",
  );
  await expect(page.locator("#email")).toBeFocused();
  await expect(
    page.getByRole("button", { name: "회원가입", exact: true }),
  ).toBeEnabled();
  expect(errors).toEqual([]);
});

test("빈 입력과 확인 비밀번호 불일치는 요청 전에 검증한다", async ({
  page,
}) => {
  let requests = 0;
  page.on("request", (request) => {
    if (request.url().endsWith("/api/auth/register")) requests++;
  });
  await page.goto("/");
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.locator("#name")).toHaveAttribute("aria-invalid", "true");
  await expect(page.locator("#name")).toBeFocused();
  await fillForm(page, "validation@example.com");
  await page.locator("#confirmation").fill("different-password");
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.locator("#confirmation-description")).toContainText(
    "일치하지 않습니다",
  );
  await expect(page.locator("#confirmation")).toBeFocused();
  expect(requests).toBe(0);
});

test("비밀번호 보기와 네트워크 오류 후 재시도를 지원한다", async ({ page }) => {
  await page.goto("/");
  await fillForm(page, `retry-${Date.now()}@example.com`);
  await expect(page.locator("#password")).toHaveAttribute("type", "password");
  await page
    .getByRole("button", { name: "비밀번호 보기", exact: true })
    .click();
  await expect(page.locator("#password")).toHaveAttribute("type", "text");
  await page
    .getByRole("button", { name: "비밀번호 숨기기", exact: true })
    .click();
  await expect(page.locator("#password")).toHaveAttribute("type", "password");
  await page.route("**/api/auth/register", (route) => route.abort("failed"));
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.locator("form").getByRole("alert")).toContainText(
    "서버에 연결할 수 없습니다",
  );
  await expect(
    page.getByRole("button", { name: "회원가입", exact: true }),
  ).toBeEnabled();
  await page.unroute("**/api/auth/register");
  await page.getByRole("button", { name: "회원가입", exact: true }).click();
  await expect(page.getByRole("status")).toContainText(
    "회원가입이 완료되었습니다",
  );
});

test("가로 스크롤 없이 화면에 맞게 표시한다", async ({ page }) => {
  await page.goto("/");
  const fits = await page.evaluate(
    () => document.documentElement.scrollWidth <= window.innerWidth,
  );
  expect(fits).toBe(true);
  await expect(
    page.getByRole("heading", { name: "나만의 시작을 만들어보세요" }),
  ).toBeVisible();
});
