import {Routes, Route, BrowserRouter, Link} from 'react-router-dom';
import './App.css'
import LoginPage from "./LoginPage.tsx";
import Home from "./Home.tsx";
import RegisterPage from "./RegisterPage.tsx";

function App() {
    return (
        <BrowserRouter>
            {/* Navigation */}
            {/*<nav>*/}
            {/*    <Link to="/">Home</Link> |{" "}*/}
            {/*    <Link to="/about">About</Link> |{" "}*/}
            {/*    <Link to="/contact">Contact</Link>*/}
            {/*</nav>*/}

            {/* Routes */}
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/rejestracja" element={<RegisterPage />} />
                <Route path="/czaty" element={<Home />} />
                <Route path="/czat" element={<Home />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App
