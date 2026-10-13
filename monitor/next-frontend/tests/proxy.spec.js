import { test, expect } from "@playwright/test";
import { GET, POST } from "../app/api/[...path]/route";

test("서버 프록시는 Cookie·CSRF·여러 Set-Cookie·상태 코드를 전달한다", async () => {
  const originalFetch = globalThis.fetch;
  const previous = process.env.MONITOR_API_URL;
  process.env.MONITOR_API_URL = "https://api.example.invalid";
  try {
    globalThis.fetch = async (url, options) => {
      expect(url.href).toBe("https://api.example.invalid/api/auth/login");
      expect(options.headers.get("cookie")).toBe("session=opaque");
      expect(options.headers.get("x-csrf-token")).toBe("opaque-csrf");
      const headers = new Headers({ "Content-Type": "application/json" });
      headers.append("Set-Cookie", "session=new; Path=/; HttpOnly");
      headers.append("Set-Cookie", "other=value; Path=/");
      return new Response('{"error":"test response"}', {
        status: 403,
        headers,
      });
    };
    const response = await POST(
      new Request("https://web.example.invalid/api/auth/login", {
        method: "POST",
        headers: {
          cookie: "session=opaque",
          "x-csrf-token": "opaque-csrf",
          "content-type": "application/json",
        },
        body: "{}",
      }),
      { params: Promise.resolve({ path: ["auth", "login"] }) },
    );
    expect(response.status).toBe(403);
    expect(response.headers.getSetCookie()).toHaveLength(2);
    expect(await response.json()).toEqual({ error: "test response" });
  } finally {
    globalThis.fetch = originalFetch;
    if (previous === undefined) delete process.env.MONITOR_API_URL;
    else process.env.MONITOR_API_URL = previous;
  }
});

test("프록시 연결 실패는 502이며 브라우저의 이벤트 수신 POST를 막는다", async () => {
  const originalFetch = globalThis.fetch;
  const previous = process.env.MONITOR_API_URL;
  process.env.MONITOR_API_URL = "http://127.0.0.1:1";
  try {
    globalThis.fetch = async () => {
      throw new Error("offline");
    };
    const failure = await GET(new Request("http://web.invalid/api/notes"), {
      params: Promise.resolve({ path: ["notes"] }),
    });
    expect(failure.status).toBe(502);
    expect((await failure.json()).error).toContain(
      "감시 API에 연결하지 못했습니다",
    );
    const rejected = await POST(
      new Request("http://web.invalid/api/events", { method: "POST" }),
      { params: Promise.resolve({ path: ["events"] }) },
    );
    expect(rejected.status).toBe(404);
  } finally {
    globalThis.fetch = originalFetch;
    if (previous === undefined) delete process.env.MONITOR_API_URL;
    else process.env.MONITOR_API_URL = previous;
  }
});
