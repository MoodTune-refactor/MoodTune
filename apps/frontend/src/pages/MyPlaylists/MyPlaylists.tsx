import React from "react";
import UserPlaylists from "../../components/UserPlaylists/UserPlaylists";
import { useTranslation } from "react-i18next";
import "./MyPlaylists.scss";

const MyPlaylists: React.FC = () => {
    const { t } = useTranslation();
    return (
        <section className="my-playlists">
            <h2 className="my-playlists__title">{t("playlists.title")}</h2>
            <UserPlaylists />
        </section>
    );
};

export default MyPlaylists;
