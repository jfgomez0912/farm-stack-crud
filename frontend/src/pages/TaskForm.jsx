import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { tasksApi } from "../api/tasks";

function TaskForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const params = useParams();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (!params.id) {
        await tasksApi.tasksCreateTask({ title, description });
      } else {
        await tasksApi.tasksUpdateTask(params.id, { title, description });
      }
      navigate("/");
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (params.id) {
      tasksApi
        .tasksGetTask(params.id)
        .then((res) => {
          setTitle(res.data.title);
          setDescription(res.data.description);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, []);

  return (
    <div className="flex items-center justify-center h-[calc(100vh-10rem)]">
      <div>
        <form className="bg-zinc-950 p-10" onSubmit={handleSubmit}>
          <h1 className="text-3xl my-4">
            {params.id ? "Update Task" : "Create Task"}
          </h1>
          <input
            className="block py-2 px-3 mb-4 w-full text-black"
            type="text"
            placeholder="title"
            onChange={(e) => setTitle(e.target.value)}
            value={title}
            autoFocus
          />
          <textarea
            className="block py-2 px-3 mb-4 w-full text-black"
            placeholder="description"
            rows="3"
            onChange={(e) => setDescription(e.target.value)}
            value={description}
          ></textarea>
          <button className="bg-white hover:bg-slate-800 hover:text-white text-slate-800 py-2 px-4 rounded">
            {params.id ? "Update Task" : "Create Task"}
          </button>
          {params.id && (
            <button
              className="bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 rounded ml-5"
              onClick={async () => {
                try {
                  await tasksApi.tasksDeleteTask(params.id);
                  navigate("/");
                } catch (error) {
                  console.log(error);
                }
              }}
            >
              Delete
            </button>
          )}
        </form>
      </div>
    </div>
  );
}

export default TaskForm;
