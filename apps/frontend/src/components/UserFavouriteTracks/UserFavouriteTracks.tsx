import React from "react";
import Notifications from "../NotificationsPopup/Notifications";
import { useTranslation } from "react-i18next";
import { TrackResponse } from "../../types/userSpotifyData";
import "./UserFavouriteTracks.scss";

interface UserFavouriteTracksProps {
    favouriteTracks: TrackResponse[];
    loading: boolean;
    error: string | null;
    setError?: (error: string | null) => void;
}

const UserFavouriteTracks: React.FC<UserFavouriteTracksProps> = ({ favouriteTracks, error, setError }) => {
    const { t } = useTranslation();

    return (
        <div className="favourite-tracks">
            {error && setError && (
                <Notifications
                    message={error}
                    variant="error"
                    onClose={() => setError(null)}
                />
            )}

            {favouriteTracks.length === 0 ? (
                <p>{t('my-tracks.empty-tracks')}</p>
            ) : (
                <ul className="favourite-tracks__list">
                    {favouriteTracks.map((trackData) => {
                        const track = trackData.spotify_data;
                        const dataset = trackData.dataset_data;

                        return track && dataset ? (
                            <li key={track.spotify_url || `track-${Math.random()}`} className="favourite-tracks__item">
                                <div className="favourite-tracks__image">
                                    <img
                                        src={track.picture}
                                        alt={track.original_name || "Unknown track"}
                                        className="favourite-tracks__image-image"
                                    />
                                </div>
                                
                                <div className="favourite-tracks__info">
                                    <h4 className="favourite-tracks__name">{track.original_name}</h4>
                                    
                                    <div className="favourite-tracks__data">
                                        <span className="favourite-tracks__artists">{track.artist}</span>
                                        <span> | </span>
                                        <span>{track.album || "Unknown album"}</span>
                                    </div>
                                    
                                    <div className="favourite-tracks__details">
                                        <span className="favourite-tracks__details--time">
                                            <span className="icon icon-clook"></span>
                                            {(track.duration_ms ? track.duration_ms / 60000 : 0).toFixed(2)} min
                                        </span>

                                        <span className="favourite-tracks__details--popularity">
                                            <span className="icon icon-star"></span>
                                            {track.popularity ?? "N/A"}
                                        </span>
                                    </div>

                                    <div className="favourite-tracks__stats">
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.male')}</span>
                                            <progress value={dataset.male} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.danceable')}</span>
                                            <progress value={dataset.danceable} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.tonal')}</span>
                                            <progress value={dataset.tonal} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.timbre_bright')}</span>
                                            <progress value={dataset.timbre_bright} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.instrumental')}</span>
                                            <progress value={dataset.instrumental} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_acoustic')}</span>
                                            <progress value={dataset.mood_acoustic} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_aggresive')}</span>
                                            <progress value={dataset.mood_aggressive} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_electronic')}</span>
                                            <progress value={dataset.mood_electronic} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_happy')}</span>
                                            <progress value={dataset.mood_happy} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_party')}</span>
                                            <progress value={dataset.mood_party} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_relaxed')}</span>
                                            <progress value={dataset.mood_relaxed} max="1"></progress>
                                        </div>
                                        <div className="favourite-tracks__stat">
                                            <span className="favourite-tracks__stat--data">{t('preferences.mood_sad')}</span>
                                            <progress value={dataset.mood_sad} max="1"></progress>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        ) : null;
                    })}
                </ul>
            )}
        </div>
    );
};

export default UserFavouriteTracks;
