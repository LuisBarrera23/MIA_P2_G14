import React, { useState, Fragment } from 'react';
import Editor from './Components/Editor'
import Login from './Components/Login'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    // Aquí puedes realizar la lógica de autenticación
    // Si la autenticación es exitosa, establece isLoggedIn en true
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    // Aquí puedes realizar cualquier otra lógica de cierre de sesión que necesites

    // Establece isLoggedIn en false para volver al componente Login
    setIsLoggedIn(false);
  };

  return (
    <Fragment>
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} />
      ) : (
        <Editor onLogout={handleLogout} />
      )}
    </Fragment>
  );
}

export default App;
