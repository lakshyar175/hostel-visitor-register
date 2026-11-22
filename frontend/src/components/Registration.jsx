import { useState, useEffect } from 'react';
const API_URL = "http://127.0.0.1:8001";

export default function Registration() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        console.log("Registration page loaded");
    }, []);

    function register() {
        fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.detail) {
                setMessage("Error: " + data.detail);
            } else {
                setMessage("Staff registered successfully!");
                setUsername("");
                setEmail("");
                setPassword("");
            }
        })
        .catch((error) => {
            setMessage("Unable to connect to server");
            console.log(error);
        });
    }
    return (
        <>
            <h1>Staff Registration</h1>
            <p>Username</p>
            <input
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <p>Email</p>
            <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <p>Password</p>
            <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br /><br />
            <button onClick={register}>Register</button>

            <p>{message}</p>
        </>
    );
}