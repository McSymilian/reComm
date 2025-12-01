import React, {type FormEvent, useState} from 'react';
// Używamy useNavigate do przekierowania użytkownika po pomyślnym logowaniu
import { useNavigate } from 'react-router-dom';
import type {AuthSuccessResponse} from './types/api.ts';

const RegisterPage = () => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordCheck, setPasswordCheck] = useState('');

    const [error, setError] = useState<string|null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setError(null);
        if (password !== passwordCheck) {
            setError("Hasła nie pasują do siebie");
            return
        }
        setIsLoading(true);
        //dummy response
        const authSuccessResponse: AuthSuccessResponse = {
            message: "Rejestracja pomyślna",
            token: "tokentokentoken",
            code: 200,
        }

        try {
            //todo server request

        } catch (apiError) {
            setError("Wystąpił błąd podczas komunikacji z serwerem." + apiError.message);
            console.error(apiError);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Zarejestruj się do reComm</h2>

            <form onSubmit={handleSubmit} style={styles.form}>

                <input
                    type="text"
                    placeholder="Nazwa użytkownika"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={isLoading}
                    style={styles.input}
                />

                <input
                    type="password"
                    placeholder="Hasło"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isLoading}
                    style={styles.input}
                />

                <input
                    type="password"
                    placeholder="Potwierdź hasło"
                    value={passwordCheck}
                    onChange={(e) => setPasswordCheck(e.target.value)}
                    required
                    disabled={isLoading}
                    style={styles.input}
                />

                {error && <p style={styles.error}>{error}</p>}

                <button
                    type="submit"
                    disabled={isLoading}
                    style={styles.button}
                >
                    {isLoading ? 'Rejestracja...' : 'Zarejestruj się'}
                </button>
            </form>
        </div>
    );
};

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
        color: '#2C2E33',
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
        backgroundColor: '#4A90E2',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '16px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
    },
    error: {
        color: '#E74C3C',
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

export default RegisterPage;