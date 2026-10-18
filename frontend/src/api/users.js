import api from "./axios";

export async function uploadAvatar(file) {
    const form = new FormData();
    form.append("file", file);
    const response = await api.post("/users/me/avatar", form);
    return response.data;
}

export async function updateProfile(data) {
    const response = await api.put("/users/me", data);
    return response.data;
}
