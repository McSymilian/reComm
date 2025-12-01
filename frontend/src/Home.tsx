
const Home = () => {
    return (
        <div style={styles.container}>
            <h2 style={styles.header}>Czaty</h2>
        </div>
    );
};

// Podstawowe style CSS (inline dla prostoty)
const styles = {
    container: {
        flex: 1,
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

export default Home;