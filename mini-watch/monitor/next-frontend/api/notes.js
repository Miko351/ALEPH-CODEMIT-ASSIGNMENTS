import { request } from "./client";
export const listNotes = () => request("/notes");
export const findNote = (id) => request(`/notes/${id}`);
export const createNote = (values) =>
  request("/notes", { method: "POST", body: JSON.stringify(values) });
export const updateNote = (id, values) =>
  request(`/notes/${id}`, { method: "PUT", body: JSON.stringify(values) });
export const deleteNote = (id) => request(`/notes/${id}`, { method: "DELETE" });
