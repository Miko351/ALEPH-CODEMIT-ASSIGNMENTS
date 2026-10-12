import type { SignupValues, FieldErrors } from "./validation";

export type RegisteredMember = { id: string; name: string; created_at: string };
export class RegistrationError extends Error {
  constructor(
    message: string,
    public fields: FieldErrors = {},
  ) {
    super(message);
  }
}

export async function registerMember(
  values: SignupValues,
): Promise<RegisteredMember> {
  const baseUrl = (
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
  ).replace(/\/$/, "");
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: values.name.trim(),
        email: values.email.trim(),
        password: values.password,
      }),
      signal: AbortSignal.timeout(15000),
    });
  } catch {
    throw new RegistrationError(
      "서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.",
    );
  }
  const body = await response.json().catch(() => null);
  if (response.status === 409)
    throw new RegistrationError("이미 가입된 이메일입니다.", {
      email: "이미 가입된 이메일입니다. 다른 이메일을 사용해 주세요.",
    });
  if (response.status === 422) {
    const fields: FieldErrors = {};
    for (const issue of Array.isArray(body?.detail) ? body.detail : []) {
      const field: unknown = issue.loc?.[1];
      if (field === "name" || field === "email" || field === "password")
        fields[field] = "입력값을 확인해 주세요.";
    }
    throw new RegistrationError("입력한 정보를 다시 확인해 주세요.", fields);
  }
  if (!response.ok || !body?.id)
    throw new RegistrationError(
      "가입을 완료하지 못했습니다. 잠시 후 다시 시도해 주세요.",
    );
  return body as RegisteredMember;
}
