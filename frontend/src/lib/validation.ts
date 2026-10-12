export type SignupValues = {
  name: string;
  email: string;
  password: string;
  confirmation: string;
};
export type FieldErrors = Partial<Record<keyof SignupValues, string>>;

export function validateSignup(values: SignupValues): FieldErrors {
  const errors: FieldErrors = {};
  const nameLength = Array.from(values.name.trim()).length;
  if (nameLength < 2 || nameLength > 80)
    errors.name = "이름은 2~80자로 입력해 주세요.";
  const email = values.email.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254)
    errors.email = "올바른 이메일 주소를 입력해 주세요.";
  const passwordLength = Array.from(values.password).length;
  if (passwordLength < 10 || passwordLength > 128 || !values.password.trim())
    errors.password =
      "비밀번호는 공백만 사용하지 않고 10~128자로 입력해 주세요.";
  if (!values.confirmation || values.password !== values.confirmation)
    errors.confirmation = "비밀번호가 일치하지 않습니다.";
  return errors;
}
