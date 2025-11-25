import type { Todo } from "../../types/todo";

interface Props {
  todos: Todo[];
  input: string;
  onInputChange: (value: string) => void;
  onAdd: () => void;
  onLogout: () => void;
}

export function TodoListView({
  todos,
  input,
  onInputChange,
  onAdd,
  onLogout,
}: Props) {
  return (
    <div style={{ padding: "20px" }}>
      <button onClick={onLogout} className="logout-btn">
        Logout
      </button>

      <h2>Todo List</h2>

      <input
        value={input}
        onChange={(e) => onInputChange(e.target.value)}
      />
      <button onClick={onAdd}>Add</button>

      <ul>
        {todos.map((t) => (
          <li key={t.id}>{t.title}</li>
        ))}
      </ul>
    </div>
  );
}
