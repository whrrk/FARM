export interface Todo {
    id: string
    title: string
    description: string
    owner_email: string
}

export interface CreateTodo {
    title: string;
    done?: boolean;
}
