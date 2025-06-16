import React, { useContext } from "react";
import { FilteredTracksContext } from "../../context/FilteredTracksContext/FilteredTracksContext";
import UserFavouriteTracks from "../../components/UserFavouriteTracks/UserFavouriteTracks";
import { useTranslation } from "react-i18next";
import "./MyTracks.scss";

const MyTracks: React.FC = () => {
    const { t } = useTranslation();
    const context = useContext(FilteredTracksContext);

    if (!context) {
        return <p>Error: Not found context.</p>;
    }

    const { topTracks, favouriteTracks, loading, error } = context;

    return (
        <div className="my-tracks">
            <h4 className="my-tracks__title">{t('my-tracks.fav-tracks')}</h4>
            <p className="my-tracks__description">{t('my-tracks.description')}</p>
            <section>
                <UserFavouriteTracks
                    favouriteTracks={favouriteTracks}
                    loading={loading}
                    error={error}
                />
            </section>
            <section>
                <UserFavouriteTracks
                        favouriteTracks={topTracks}
                        loading={loading}
                        error={error}
                    />
            </section>
        </div>
    );
};

export default MyTracks;
