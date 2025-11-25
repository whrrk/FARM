// src/components/todo/TodoList.tsx
import { useEffect, useState } from "react";
import type { Todo } from "../../types/todo";
import { TodoApi,AuthApi } from "../../api/api";
import { TodoListView } from "./TodoListView";

interface TodoListProps {
  onLogout: () => void;
}

export function TodoList({ onLogout }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    TodoApi
      .getList()
      .then(setTodos)
      .catch((err) => {
        console.error(err);
        setError("タスクの取得に失敗しました。");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleAdd = async () => {
    if (!input.trim()) return;
    try {
      const csrf = await AuthApi.getCsrfToken();
      const newTodo = await TodoApi.create({ title: input.trim() }, csrf);
      setTodos((prev) => [...prev, newTodo]);
      setInput("");
    } catch (err) {
      console.error(err);
      setError("タスクの追加に失敗しました。");
    }
  };

  const handleToggleDone = async (id: string, currentDone: boolean) => {
    try {
      const csrf = await AuthApi.getCsrfToken();
      const updated = await TodoApi.update(id, { done: !currentDone }, csrf);
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      console.error(err);
      setError("タスクの更新に失敗しました。");
    }
  };

  const handleEditTitle = async (id: string, currentTitle: string) => {
    const nextTitle = window.prompt("新しいタイトルを入力してください", currentTitle);
    if (!nextTitle || nextTitle.trim() === currentTitle) return;

    try {
      const csrf = await AuthApi.getCsrfToken();
      const updated = await TodoApi.update(id, { title: nextTitle.trim() }, csrf);
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      console.error(err);
      setError("タスクのタイトル更新に失敗しました。");
    }
  };

  // 삭제
  const handleRemove = async (id: string) => {
    if (!window.confirm("本当に削除しますか？")) return;
    try {
      const csrf = await AuthApi.getCsrfToken();
      await TodoApi.remove(id, csrf);
      setTodos((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      console.error(err);
      setError("タスクの削除に失敗しました。");
    }
  };

  return (
    <TodoListView
      todos={todos}
      input={input}
      loading={loading}
      error={error}
      onInputChange={setInput}
      onAdd={handleAdd}
      onToggleDone={handleToggleDone}
      onEditTitle={handleEditTitle}
      onRemove={handleRemove}
      onLogout={onLogout}
    />
  );
}
