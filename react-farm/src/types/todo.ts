export interface Todo {
    id: string
    title: string
    description: string
    owner_email: string
    done: boolean
}

export interface CreateTodo {
    title: string;
    done?: boolean;
}
