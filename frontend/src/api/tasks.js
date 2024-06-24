import { Configuration, TasksApiFactory } from "../client";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
const config = new Configuration({ basePath: BACKEND_URL });
export const tasksApi = TasksApiFactory(config);
