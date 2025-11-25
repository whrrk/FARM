// src/components/todo/TodoListView.tsx
import type { Todo } from "../../types/todo";
import "./TodoList.css";

interface TodoListViewProps {
  todos: Todo[];
  input: string;
  loading: boolean;
  error: string | null;
  onInputChange: (value: string) => void;
  onAdd: () => void;
  onToggleDone: (id: string, done: boolean) => void;
  onEditTitle: (id: string, currentTitle: string) => void;
  onRemove: (id: string) => void;
  onLogout: () => void;
}

export function TodoListView({
  todos,
  input,
  loading,
  error,
  onInputChange,
  onAdd,
  onToggleDone,
  onEditTitle,
  onRemove,
  onLogout,
}: TodoListViewProps) {
  return (
    <div className="todo-wrapper">
      <div className="todo-card">
        <header className="todo-header">
          <div>
            <h1 className="todo-title">My Tasks</h1>
            <p className="todo-subtitle"></p>
          </div>
          <button className="todo-logout" onClick={onLogout}>
            ログアウト
          </button>
        </header>

        <section className="todo-input-row">
          <input
            className="todo-input"
            placeholder="タスクを入力して Enter または追加ボタン"
            value={input}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") onAdd();
            }}
          />
          <button className="todo-add-btn" onClick={onAdd}>
            追加
          </button>
        </section>

        {error && <div className="todo-error">{error}</div>}

        {loading ? (
          <p className="todo-loading">読み込み中…</p>
        ) : todos.length === 0 ? (
          <p className="todo-empty">まだタスクがありません。</p>
        ) : (
          <ul className="todo-list">
            {todos.map((t) => (
              <li key={t.id} className="todo-item">
                <label className={`todo-item-main ${t.done ? "todo-done" : ""}`}>
                  <input
                    type="checkbox"
                    checked={t.done}
                    onChange={() => onToggleDone(t.id, t.done)}
                  />
                  <span>{t.title}</span>
                </label>
                <div className="todo-item-actions">
                  <button
                    className="todo-edit-btn"
                    onClick={() => onEditTitle(t.id, t.title)}
                  >
                    編集
                  </button>
                  <button
                    className="todo-delete-btn"
                    onClick={() => onRemove(t.id)}
                  >
                    削除
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
