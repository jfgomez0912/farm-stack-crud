import { useEffect, useState } from "react";
import { tasksApi } from "../api/tasks";
import TaskList from "../components/TaskList";

function HomePage() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    tasksApi
      .tasksGetTasks()
      .then((res) => {
        setTasks(res.data.tasks);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return <TaskList tasks={tasks} />;
}

export default HomePage;
