import { useEffect, useState } from "react";
import type { Todo } from "../../types/todo";
import { TodoApi,AuthApi } from "../../api/api";
import { TodoListView } from "./TodoListView";

export function TodoList({ onLogout }: { onLogout: () => void }) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    TodoApi.getList().then(setTodos).catch(console.error);
  }, []);

  const addTodo = async () => {
    const csrf = await AuthApi.getCsrfToken();
    const newTodo = await TodoApi.create({ title: input }, csrf);
    setTodos((prev) => [...prev, newTodo]);
    setInput("");
  };

  const handleLogout = async () => {
    await AuthApi.logout();
    onLogout();
  };

  return (
    <TodoListView
      todos={todos}
      input={input}
      onInputChange={setInput}
      onAdd={addTodo}
      onLogout={handleLogout}
    />
  );
}
