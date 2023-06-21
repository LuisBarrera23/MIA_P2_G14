import React, { useState } from "react";
import "../css/styles.css";
import "bootstrap/dist/css/bootstrap.min.css";
const apiUrl = process.env.REACT_APP_VM_IP;

function Login({ onLogin }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");


    const handleLogin = (e) => {
        e.preventDefault();
        if (username.toString().trim() && password.toString().trim()) {
            const newUser = { user: username, password: password };
            const urlVM = `${apiUrl}:8080/login`
            fetch(urlVM, {
                method: 'POST',
                body: JSON.stringify(newUser),
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            })
                .then((res) => res.json())
                .catch((err) => {
                    console.log('Error al hacer signIn:', err);
                })
                .then((response) => {
                    console.log(response)
                    if (response.acceso === "autorizado") {
                        alert(`Bienvenido: ${username}`)
                        onLogin();
                    } else {
                        alert("El usuario o contraseña es incorrecta.")
                    }
                    setUsername("")
                    setPassword("")
                });
        } else {
            alert("Por favor llenar todos los campos")
        }
    };

    return (
        <div className="App">
            <div className="login-form">
                <h1 style={{ color: "black" }}>Sign In</h1>
                <div className="form">
                    <form onSubmit={handleLogin}>
                        <div className="input-container">
                            <h3>Username</h3>
                            <div className="input-group mb-3">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Username"
                                    aria-label="Username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>
                        <div className="input-container">
                            <h3>Password</h3>
                            <div className="input-group mb-3">
                                <input
                                    type="password"
                                    className="form-control"
                                    placeholder="Password"
                                    aria-label="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>
                        <button
                            type="submit"
                            className="btn btn-outline-info"
                            style={{ marginTop: "5%", width: 'auto' }}
                        // onClick={handleLogin}
                        >
                            Sign in
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
export default Login;