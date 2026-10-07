export class ApiError extends Error {
  constructor(message, status = 0, fields = {}) {
    super(message);
    this.status = status;
    this.fields = fields;
  }
}

export async function apiRequest(path, options = {}) {
  let response;
  try {
    response = await fetch(`/api${path}`, {
      credentials: 'same-origin',
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: AbortSignal.timeout(10000),
    });
  } catch {
    throw new ApiError('서버에 연결하지 못했습니다. 서버 실행 상태를 확인한 뒤 다시 시도해 주세요.');
  }
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    if (response.status === 401 && path !== '/auth/login' && path !== '/auth/me') {
      window.dispatchEvent(new Event('session-expired'));
    }
    throw new ApiError(data?.error || 'API 요청에 실패했습니다. 감시 서버 실행 상태를 확인해 주세요.', response.status, data?.fields);
  }
  if (!data) throw new ApiError('서버 응답을 읽지 못했습니다. 다시 시도해 주세요.');
  return data;
}
