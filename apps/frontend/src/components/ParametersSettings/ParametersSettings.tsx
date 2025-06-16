import { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import Tooltip from "../Tooltip/Tooltip";
import { useFilteredTracks } from "../../context/FilteredTracksContext/useFilteredTracks";
import "./ParametersSettings.scss";

const SETTINGS = [
  "male",
  "danceable",
  "tonal",
  "timbre_bright",
  "instrumental",
  "mood_acoustic",
  "mood_aggressive",
  "mood_electronic",
  "mood_happy",
  "mood_party",
  "mood_relaxed",
  "mood_sad",
];

const ParametersSettings = () => {
  const { t } = useTranslation();
  const { favouriteTracks, requestsCompleted } = useFilteredTracks();
  const [preferences, setPreferences] = useState<{ [key: string]: number }>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [showMore, setShowMore] = useState<boolean>(false);

  const getImportances = useCallback(() => {
    const storedSettings = localStorage.getItem("moodtune_settings");
    return storedSettings ? JSON.parse(storedSettings) : {};
  }, []);

  const fetchCentralSong = useCallback(async () => {
    if (favouriteTracks.length === 0) {
      console.warn("No hay canciones favoritas para procesar.");
      return;
    }

    try {
      setLoading(true);
      const importances = getImportances();

      const response = await fetch("http://127.0.0.1:5000/songs/rank-central-songs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          references: favouriteTracks,
          importances,
        }),
      });

      if (!response.ok) {
        throw new Error("Error obteniendo la canción central");
      }

      const data = await response.json();
      const centralSong = data.ordered_tracks[0]?.dataset_data;

      if (centralSong) {
        const newPreferences = SETTINGS.reduce((acc, setting) => {
          acc[setting] = Math.round(centralSong[setting] * 100);
          return acc;
        }, {} as { [key: string]: number });

        setPreferences(newPreferences);
        localStorage.setItem("moodtune_preferences", JSON.stringify(newPreferences));
      }
    } catch (error) {
      console.error("Error al obtener la canción central:", error);
    } finally {
      setLoading(false);
    }
  }, [favouriteTracks, getImportances]);

  useEffect(() => {
    const savedPreferences = localStorage.getItem("moodtune_preferences");
    if (savedPreferences) {
      setPreferences(JSON.parse(savedPreferences));
    } else {
      const defaultPreferences = SETTINGS.reduce((acc, setting) => {
        acc[setting] = 50;
        return acc;
      }, {} as { [key: string]: number });
      setPreferences(defaultPreferences);
    }
  }, []);

  useEffect(() => {
    if (requestsCompleted) {
      fetchCentralSong();
    }
  }, [requestsCompleted, fetchCentralSong]);

  useEffect(() => {
    if (Object.keys(preferences).length > 0) {
      localStorage.setItem("moodtune_preferences", JSON.stringify(preferences));
    }
  }, [preferences]);

  const handleChange = (setting: string, value: number) => {
    setPreferences((prev) => ({
      ...prev,
      [setting]: value,
    }));
  };

  const visibleSettings = showMore ? SETTINGS : SETTINGS.slice(0, 6);

  return (
    <div className="parameters-settings">
      <h2 className="parameters-settings__title">
        {t("mood-form.preferences")}
        <Tooltip
          text={t("mood-form.preferences-info")}
          link={{ href: "/preferences-info", text: t("mood-form.preferences-learn") }}
        >
          <span className="icon icon-question" />
        </Tooltip>
      </h2>
      <div className="parameters-settings__settings">
        {loading ? (
          <p>{t("loading.loading")}</p>
        ) : (
          <>
            {visibleSettings.map((setting) => (
              <div key={setting} className="parameters-settings__item">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={preferences[setting] || 50}
                  onChange={(e) => handleChange(setting, Number(e.target.value))}
                  style={{
                    background: `linear-gradient(90deg, 
                      rgba(130,43,190,1) 0%, 
                      rgba(251,111,172,1) ${preferences[setting] * 0.39}%, 
                      rgba(227,158,61,1) ${preferences[setting] * 0.67}%, 
                      rgba(253,229,81,1) ${preferences[setting] * 0.83}%, 
                      rgba(205,245,103,1) 100%)`,
                  }}
                  className="parameters-settings__input"
                />
                <label className="parameters-settings__label">
                  {t(`settings.${setting}`)} {preferences[setting]}%
                </label>
              </div>
            ))}
            {SETTINGS.length > 6 && (
              <button
                type="button"
                className="parameters-settings__toggle"
                onClick={() => setShowMore((prev) => !prev)}
              >
                {showMore ? t("common.view-less") : t("common.view-more")}
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ParametersSettings;
