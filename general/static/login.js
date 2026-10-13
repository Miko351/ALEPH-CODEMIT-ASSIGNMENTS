document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  const error = document.getElementById("login-error");
  button.disabled = true;
  error.hidden = true;
  try {
    const response = await fetch("/auth/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: form.username.value, password: form.password.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "로그인에 실패했습니다.");
    window.location.assign(data.redirect);
  } catch (reason) {
    error.textContent = reason.message;
    error.hidden = false;
  } finally { button.disabled = false; }
});
