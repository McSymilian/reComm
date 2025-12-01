import React, { useState } from 'react';
// Używamy useNavigate do przekierowania użytkownika po pomyślnym logowaniu
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);


    };

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Zaloguj się do reComm</h2>

            <form onSubmit={handleSubmit} style={styles.form}>

                {/* Pole Nazwa użytkownika */}
                <input
                    type="text"
                    placeholder="Nazwa użytkownika"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={isLoading}
                    style={styles.input}
                />

                {/* Pole Hasło */}
                <input
                    type="password"
                    placeholder="Hasło"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isLoading}
                    style={styles.input}
                />

                {/* Komunikat o błędzie */}
                {error && <p style={styles.error}>{error}</p>}

                {/* Przycisk Logowania */}
                <button
                    type="submit"
                    disabled={isLoading}
                    style={styles.button}
                >
                    {isLoading ? 'Logowanie...' : 'Zaloguj się'}
                </button>
            </form>

            <p style={styles.registerText}>
                Nie masz konta? <span
                onClick={() => navigate('/rejestracja')}
                style={styles.link}
            >Zarejestruj się</span>
            </p>
        </div>
    );
};

// Podstawowe style CSS (inline dla prostoty)
const styles = {
    container: {
        maxWidth: '400px',
        margin: '50px auto',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        backgroundColor: '#fff',
    },
    header: {
        marginBottom: '20px',
        color: '#2C2E33', // Kolor tekstu z Twojej palety
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    input: {
        padding: '10px',
        marginBottom: '15px',
        borderRadius: '4px',
        border: '1px solid #DEE2E6',
        fontSize: '16px',
    },
    button: {
        padding: '12px',
        backgroundColor: '#4A90E2', // Akcent z Twojej palety
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '16px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
    },
    error: {
        color: '#E74C3C', // Czerwony dla błędu
        marginBottom: '15px',
    },
    registerText: {
        marginTop: '20px',
        color: '#6C757D',
        fontSize: '14px',
    },
    link: {
        color: '#4A90E2',
        cursor: 'pointer',
        textDecoration: 'underline',
    }
};

export default LoginPage;