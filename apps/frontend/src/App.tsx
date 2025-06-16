import { BrowserRouter as Router, Route, Routes, useLocation } from "react-router-dom";
import TopMenu from "./components/TopMenu/TopMenu";
import Login from "./pages/Login/Login";
import Callback from "./pages/Login/Callback";
import PrivacyPolicy from "./pages/PrivacyPolicy/PrivacyPolicy";
import MoodForm from "./pages/MainForm/MainForm";
import Moods from "./pages/Moods/Moods";
import ProtectedRoute from "./hooks/protectedRoute";
import MyPlaylists from "./pages/MyPlaylists/MyPlaylists";
import MyTracks from "./pages/MyTracks/MyTracks";
import WelcomeScreen from "./pages/WelcomeScreen/WelcomeScreen";

import { LoadingProvider } from "./context/LoadingContext/LoadingProvider";
import { FilteredTracksProvider } from "./context/FilteredTracksContext/FilteredTracksProvider";
import { useLoading } from "./context/LoadingContext/useLoading";
import LoadingSpinner from "./components/LoadingSpinner/LoadingSpinner";

import "./assets/icons/style.scss";
import "./styles/_global.scss"

const Layout = ({ children }: { children: React.ReactNode }) => {
    const { isLoading } = useLoading();
    const location = useLocation();
    const hideTopMenu = location.pathname === "/welcome" || location.pathname === "/login";

    return (
        <>
            {isLoading && <LoadingSpinner />}
            {!hideTopMenu && <TopMenu />}
            {children}
        </>
    );
};

const AppContent = () => {
    return (
        <Routes>
            <Route path="/" element={<ProtectedRoute element={
                <MoodForm />
            } />} />
            <Route path="/login" element={<Login />} />
            <Route path="/callback" element={<Callback />} />
            <Route path="/my-playlists" element={<MyPlaylists />} />
            <Route path="/my-tracks" element={<MyTracks />} />
            <Route path="/welcome" element={<ProtectedRoute element={<WelcomeScreen />} />} /> {/* ✅ Nueva ruta */}
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="/moods" element={<ProtectedRoute element={<Moods />} />} />

        </Routes>
    );
};

const App = () => {
    return (
        <Router>
            <LoadingProvider>
                <FilteredTracksProvider>
                    <Layout>
                        <AppContent />
                    </Layout>
                </FilteredTracksProvider>
            </LoadingProvider>
        </Router>
    );
};

export default App;
