export async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", ...options.headers },
      signal: AbortSignal.timeout(10000),
    });
  } catch {
    throw new Error(
      "API 서버에 연결하지 못했습니다. Flask 서버 실행 상태를 확인해 주세요.",
    );
  }
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const error = new Error(data?.error || "API 요청에 실패했습니다.");
    error.status = response.status;
    error.fields = data?.fields || {};
    if (error.status === 401 && path !== "/auth/login" && path !== "/auth/me")
      window.dispatchEvent(new Event("session-expired"));
    throw error;
  }
  if (!data) throw new Error("서버 응답을 읽지 못했습니다.");
  return data;
}
