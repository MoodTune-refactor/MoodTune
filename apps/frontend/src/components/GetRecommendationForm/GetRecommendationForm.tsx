import { useState } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../components/Button/Button";
import GenreFilter from "../../components/GenreFilter/GenreFilter";
import ParametersSettings from "../../components/ParametersSettings/ParametersSettings";
import { useNavigate } from "react-router-dom";
import { useLoading } from "../../context/LoadingContext/useLoading";
import { API_URL, genreGroups } from "../../config";
import VerticalParametersSettings from "../../components/VerticalParametersSettings/VerticalParametersSettings";
import "./GetRecommendationForm.scss";

export const GetRecommendationForm = () => {
    const { t } = useTranslation();
    const { isLoading, setIsLoading } = useLoading();
    const [selectedGenres, setSelectedGenres] = useState<string[]>(["all genres"]);
    const navigate = useNavigate();
  
    const handleGetSimilarSongs = async () => {
      setIsLoading(true);
      try {
        const preferences = JSON.parse(localStorage.getItem("moodtune_preferences") || "{}");
        const importances = JSON.parse(localStorage.getItem("moodtune_settings") || "{}");
  
        if (!Object.keys(preferences).length || !Object.keys(importances).length) {
          throw new Error("No hay preferencias o importancias guardadas.");
        }
  
        let additionalKeywords: string[] = [];
        if (!selectedGenres.includes("all genres")) {
          additionalKeywords = selectedGenres.flatMap(genre => genreGroups[genre] || []);
        }
  
        const response = await fetch(`${API_URL}/songs/recommendations`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ preferences, importances, genres: additionalKeywords }),
        });
  
        if (!response.ok) throw new Error("Error al obtener recomendaciones");
  
        const recommendedSongs = await response.json();
        localStorage.setItem("moodPlaylist", JSON.stringify(recommendedSongs.recommended_tracks));
        localStorage.setItem("moodText", "Canciones Similares");
        navigate("/moods");
      } catch (error) {
        console.error("Error al obtener recomendaciones:", error);
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <div className="recomendation-form">
        <GenreFilter selectedGenres={selectedGenres} setSelectedGenres={setSelectedGenres} />
        <div className="recomendation-form__form-main">
          <ParametersSettings />
          <div className="recomendation-form__block-right">
            <VerticalParametersSettings />
            <Button 
              type="button" 
              variant="secondary" 
              text={isLoading ? "Cargando..." : t("mood-form.get-playlist")} 
              onClick={handleGetSimilarSongs} 
              disabled={isLoading} 
            />
          </div>
        </div>
      </div>
    );
};
