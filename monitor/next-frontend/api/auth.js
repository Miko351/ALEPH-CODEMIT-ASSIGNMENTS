import { request } from "./client";
export const currentUser = () => request("/auth/me");
export const login = async (username, password) => {
  await currentUser();
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
};
export const logout = () => request("/auth/logout", { method: "POST" });
