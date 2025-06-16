import React, { useState, useEffect } from "react";
import { useUserPlaylists } from "./useUserPlaylists";
import { Playlist, Track } from "../../types/userSpotifyData";
import { useTranslation } from "react-i18next";
import Notifications from "../NotificationsPopup/Notifications";
import { useLoading } from "../../context/LoadingContext/useLoading";
import "./UserPlaylists.scss";

const UserPlaylists: React.FC = () => {
  const { t } = useTranslation();
  const { playlists, moodTuneTracks, expandedPlaylist, togglePlaylist, loading, error, setError } = useUserPlaylists();
  const { setIsLoading } = useLoading();
  const [iframeErrors, setIframeErrors] = useState<{ [key: string]: boolean }>({});
  const [iframeLoadedCount, setIframeLoadedCount] = useState(0);
  const [totalIframes, setTotalIframes] = useState(0);

  // Calcula el total de iframes a cargar según playlists y su estado (expandida o no)
  useEffect(() => {
    if (!loading && playlists.length > 0) {
      let total = 0;
      playlists.forEach((playlist) => {
        const tracks = moodTuneTracks[playlist.id] || [];
        total += expandedPlaylist === playlist.id ? tracks.length : Math.min(2, tracks.length);
      });
      setTotalIframes(total);
      setIframeLoadedCount(0);
      setIsLoading(true);
    }
  }, [loading, playlists, moodTuneTracks, expandedPlaylist, setIsLoading]);

  // Cuando se hayan cargado (o fallado) todos los iframes, desactiva el loading global
  useEffect(() => {
    if (totalIframes > 0 && iframeLoadedCount === totalIframes) {
      setIsLoading(false);
    }
  }, [iframeLoadedCount, totalIframes, setIsLoading]);

  return (
    <div className="user-playlists">
      {error && (
        <Notifications 
          message={error} 
          variant="error" 
          onClose={() => setError(null)} 
        />
      )}

      {playlists.length === 0 ? (
        <p>{t("empty-data.playlists")}</p>
      ) : (
        <ul className="user-playlists__list">
          {playlists.map((playlist: Playlist) => {
            const isExpanded = expandedPlaylist === playlist.id;
            const tracks = moodTuneTracks[playlist.id] || [];
            const previewTracks = tracks.slice(0, 2);

            return (
              <li key={playlist.id} className={`user-playlists__item ${isExpanded ? "expanded" : ""}`}>
                <div className="user-playlists__playlist">
                  <div className="user-playlists__image">
                    <img 
                      src={playlist.images?.[0]?.url || "/default-playlist.png"} 
                      alt={`Cover of ${playlist.name}`} 
                      className="user-playlists__image-image"
                    />
                  </div>
                  <div className="user-playlists__details">
                    <h4 className="user-playlists__title">{playlist.name}</h4>
                    <ul className="user-playlists__tracklist">
                      {(isExpanded ? tracks : previewTracks).map((track: Track) => {
                        const spotifyTrackId = track.external_urls?.spotify?.split("/track/")[1]?.split("?")[0];
                        return (
                          <li key={track.id} className="user-playlists__track">
                            {spotifyTrackId && !iframeErrors[track.id] && (
                              <div className="spotify-player-container">
                                <iframe
                                  src={`https://open.spotify.com/embed/track/${spotifyTrackId}?theme=0`}
                                  width="100%"
                                  height="80"
                                  frameBorder="0"
                                  sandbox="allow-same-origin allow-scripts allow-popups allow-presentation"
                                  allow="encrypted-media"
                                  className="spotify-player"
                                  onLoad={() => setIframeLoadedCount(prev => prev + 1)}
                                  onError={() => {
                                    setIframeErrors(prev => ({ ...prev, [track.id]: true }));
                                    setIframeLoadedCount(prev => prev + 1);
                                  }}
                                ></iframe>
                              </div>
                            )}
                          </li>
                        );
                      })}
                    </ul>

                    {tracks.length > 2 && (
                      <div className="user-playlists__btn-container">
                        <button className="user-playlists__toggle-btn" onClick={() => togglePlaylist(playlist.id)}>
                          {isExpanded ? (
                            <>
                              {t('common.view-less')}
                              <span className="icon icon-arrow-turn-up"></span>
                            </>
                          ) : (
                            <>
                              {t('common.view-more')}
                              <span className="icon icon-arrow-turn-down"></span>
                            </>
                          )}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default UserPlaylists;
