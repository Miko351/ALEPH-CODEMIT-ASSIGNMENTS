import type { InputHTMLAttributes, ReactNode } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
  hint?: string;
  action?: ReactNode;
};

export function FormField({ label, error, hint, action, id, ...props }: Props) {
  const description = error || hint;
  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        <span className="required-mark">*</span>
      </label>
      <div className={`input-wrap ${error ? "invalid" : ""}`}>
        <input
          {...props}
          id={id}
          aria-invalid={Boolean(error)}
          aria-describedby={description ? `${id}-description` : undefined}
        />
        {action}
      </div>
      {description && (
        <p
          id={`${id}-description`}
          className={error ? "field-error" : "field-hint"}
        >
          {description}
        </p>
      )}
    </div>
  );
}
