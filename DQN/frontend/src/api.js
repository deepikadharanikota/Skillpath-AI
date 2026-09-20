/**
 * api.js
 * Centralized API client for SkillPath AI Backend.
 */

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const getToken = () => localStorage.getItem("skillpath_token") || "";
export const setToken = (t) => localStorage.setItem("skillpath_token", t);
export const removeToken = () => localStorage.removeItem("skillpath_token");

async function request(endpoint, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };

  if (token) {
    headers["token"] = token;
  }

  // If body is not FormData, add application/json Content-Type
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${BACKEND_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errMsg = "An error occurred";
    try {
      const errData = await response.json();
      errMsg = errData.detail || errData.message || JSON.stringify(errData);
    } catch {
      errMsg = await response.text();
    }
    const err = new Error(errMsg);
    err.status = response.status;
    throw err;
  }

  return response.json();
}

export const api = {
  // ── Auth ──
  login: (username, password) => request("/auth/local-login", { method: "POST", body: { username, password } }),
  register: (username, email, password, target_role) => request("/auth/register", { method: "POST", body: { username, email, password, target_role } }),
  me: () => request("/auth/me"),
  logout: async () => {
    try {
      await request("/auth/logout", { method: "POST" });
    } finally {
      removeToken();
    }
  },

  // ── Resume ──
  getResume: () => request("/resume"),
  getSkillGap: () => request("/resume/skill-gap"),
  uploadResumeFile: (formData) => request("/resume/upload", { method: "POST", body: formData }),
  updateTargetRole: (target_role) => request("/resume/target-role", { method: "PUT", body: { target_role } }),

  // ── Learning & Videos ──
  getState: () => request("/learning/state"),
  getLearningResume: () => request("/learning/resume"),
  saveLearningPosition: (topic, module, video_id, position_seconds, video_title = "") =>
    request("/learning/position", {
      method: "POST",
      body: { topic, module, video_id, position_seconds, video_title },
    }),
  getVideos: (topic, module, difficulty) => {
    let url = `/learning/videos?topic=${encodeURIComponent(topic)}&module=${encodeURIComponent(module)}`;
    if (difficulty) url += `&difficulty=${encodeURIComponent(difficulty)}`;
    return request(url);
  },
  completeVideo: (topic, module, video_id) => request("/learning/video/complete", { method: "POST", body: { topic, module, video_id } }),
  navigateTopic: (topic, module = "intro") => request("/learning/navigate", { method: "POST", body: { topic, module } }),

  // ── Quiz ──
  generateQuiz: (topic, module, difficulty) => {
    let url = `/quiz/generate?topic=${encodeURIComponent(topic)}&module=${encodeURIComponent(module)}`;
    if (difficulty) url += `&difficulty=${encodeURIComponent(difficulty)}`;
    return request(url);
  },
  submitQuiz: (quiz_id, topic, module, answers) => request("/quiz/submit", { method: "POST", body: { quiz_id, topic, module, answers } }),
  getQuizResults: (quiz_id) => request(`/quiz/${quiz_id}/results`),
  getQuizHistory: () => request("/quiz/history"),

  // ── Dashboard ──
  getDashboardOverview: () => request("/dashboard/overview"),
  getDashboardSkills: () => request("/dashboard/skills"),
  getDashboardTimeline: () => request("/dashboard/activity"),
  getDashboardInsights: () => request("/dashboard/insights"),
  getDashboardRecommendations: () => request("/dashboard/recommendations"),
  getDashboardRoadmap: () => request("/dashboard/roadmap"),
  getQuizAnalysis: () => request("/dashboard/quiz-analysis"),

  // ── Catalog ──
  getRoles: () => request("/roles"),
};
