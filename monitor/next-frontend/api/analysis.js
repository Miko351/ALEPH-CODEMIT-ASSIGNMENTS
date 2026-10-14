import { request } from "./client";

export const startObservation = () =>
  request("/analysis/start", { method: "POST", body: "{}" });
export const getAnalysis = ({ threshold, afterId, referenceTime }) => {
  const query = new URLSearchParams({
    threshold: String(threshold),
    after_id: String(afterId),
  });
  if (referenceTime) query.set("reference_time", referenceTime);
  return request("/analysis?" + query.toString());
};
