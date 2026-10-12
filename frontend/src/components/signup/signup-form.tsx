"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { FormField } from "@/components/ui/form-field";
import { Icon } from "@/components/ui/icon";
import {
  registerMember,
  RegistrationError,
  type RegisteredMember,
} from "@/lib/api";
import {
  validateSignup,
  type FieldErrors,
  type SignupValues,
} from "@/lib/validation";

const emptyValues: SignupValues = {
  name: "",
  email: "",
  password: "",
  confirmation: "",
};

export function SignupForm() {
  const [values, setValues] = useState(emptyValues);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);
  const [visible, setVisible] = useState(false);
  const [member, setMember] = useState<RegisteredMember | null>(null);
  const formRef = useRef<HTMLFormElement>(null);
  const submitting = useRef(false);
  const focusTarget = useRef<string | null>(null);

  useEffect(() => {
    if (!pending && focusTarget.current) {
      formRef.current
        ?.querySelector<HTMLInputElement>(`#${focusTarget.current}`)
        ?.focus();
      focusTarget.current = null;
    }
  }, [pending, errors]);

  function update(field: keyof SignupValues, value: string) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: undefined }));
    setMessage("");
  }

  function focusError(fields: FieldErrors) {
    // Wait until React re-enables the fieldset after an API error.
    focusTarget.current = Object.keys(fields)[0] ?? null;
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (submitting.current) return;
    const validation = validateSignup(values);
    setErrors(validation);
    setMessage("");
    if (Object.keys(validation).length) {
      focusError(validation);
      return;
    }
    submitting.current = true;
    setPending(true);
    try {
      const registered = await registerMember(values);
      setValues(emptyValues);
      setVisible(false);
      setMember(registered);
    } catch (error) {
      const failure =
        error instanceof RegistrationError
          ? error
          : new RegistrationError("다시 시도해 주세요.");
      setMessage(failure.message);
      setErrors(failure.fields);
      focusError(failure.fields);
    } finally {
      submitting.current = false;
      setPending(false);
    }
  }

  if (member)
    return (
      <div className="success-card" role="status" aria-live="polite">
        <div className="success-icon">
          <Icon name="check" />
        </div>
        <h3>{member.name}님, 환영합니다!</h3>
        <p>
          회원가입이 완료되었습니다.
          <br />
          새로운 이야기를 시작할 준비가 되었어요.
        </p>
        <span className="success-label">계정 생성 완료</span>
        <button className="secondary-button" onClick={() => setMember(null)}>
          다른 계정 가입하기 <Icon name="arrow" />
        </button>
      </div>
    );

  return (
    <form onSubmit={submit} noValidate ref={formRef} aria-busy={pending}>
      <fieldset disabled={pending}>
        <FormField
          id="name"
          label="이름"
          placeholder="이름을 입력해 주세요"
          autoComplete="name"
          required
          value={values.name}
          error={errors.name}
          onChange={(event) => update("name", event.target.value)}
        />
        <FormField
          id="email"
          label="이메일"
          type="email"
          placeholder="you@example.com"
          autoComplete="email"
          required
          value={values.email}
          error={errors.email}
          onChange={(event) => update("email", event.target.value)}
        />
        <FormField
          id="password"
          label="비밀번호"
          type={visible ? "text" : "password"}
          placeholder="10자 이상 입력해 주세요"
          autoComplete="new-password"
          required
          value={values.password}
          error={errors.password}
          hint="10~128자로 입력해 주세요."
          onChange={(event) => update("password", event.target.value)}
          action={
            <button
              type="button"
              className="visibility-button"
              aria-label={visible ? "비밀번호 숨기기" : "비밀번호 보기"}
              aria-pressed={visible}
              onClick={() => setVisible(!visible)}
            >
              <Icon name={visible ? "eye-off" : "eye"} />
            </button>
          }
        />
        <FormField
          id="confirmation"
          label="비밀번호 확인"
          type={visible ? "text" : "password"}
          placeholder="비밀번호를 한 번 더 입력해 주세요"
          autoComplete="new-password"
          required
          value={values.confirmation}
          error={errors.confirmation}
          onChange={(event) => update("confirmation", event.target.value)}
        />
        {message && (
          <p className="form-alert" role="alert">
            {message}
          </p>
        )}
        <button type="submit" className="submit-button">
          {pending ? (
            <>
              <span className="spinner" /> 가입하는 중…
            </>
          ) : (
            <>
              회원가입 <Icon name="arrow" />
            </>
          )}
        </button>
      </fieldset>
      <p className="privacy-note">
        <Icon name="lock" />
        <span>입력하신 개인정보는 안전하게 보호됩니다.</span>
      </p>
    </form>
  );
}
