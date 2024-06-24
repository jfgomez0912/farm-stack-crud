import { Configuration, TasksApiFactory } from "../client";

const config = new Configuration({ basePath: "http://localhost:8000" });
export const tasksApi = TasksApiFactory(config);
