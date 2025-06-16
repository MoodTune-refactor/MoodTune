import { useState, FormEvent } from "react";
import { useTranslation } from "react-i18next";
import Button from "../../components/Button/Button";
import { Textarea } from "../../components/Textarea/Textarea";
import GenreFilter from "../../components/GenreFilter/GenreFilter";
import { useNavigate } from "react-router-dom";
import { useLoading } from "../../context/LoadingContext/useLoading"; // Importar el hook del contexto
import { API_URL, reducedGenreGroups } from "../../config";
import "./GetMoodForm.scss";

export const GetMoodForm = () => {
    const { t } = useTranslation();
    const { isLoading, setIsLoading } = useLoading(); // Usar el contexto de loading
    const [moodText, setMoodText] = useState("");
    const [selectedGenres, setSelectedGenres] = useState<string[]>(["all genres"]);
    const navigate = useNavigate();
  
    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      if (moodText.trim() === "") return;
      
      setIsLoading(true); // Activar el loading global
      try {
        let additionalKeywords: string[] = [];
        if (!selectedGenres.includes("all genres")) {
          additionalKeywords = selectedGenres.flatMap(genre => reducedGenreGroups[genre] || []);
        }
    
        const response = await fetch(`${API_URL}/songs/mood`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            moodText: `${moodText} ${additionalKeywords}`
           }),
        });
  
        if (!response.ok) throw new Error("Error al obtener la playlist");
        
        const recommendedSongs = await response.json();
        localStorage.setItem("moodPlaylist", JSON.stringify(recommendedSongs));
        localStorage.setItem("moodText", moodText);
        navigate("/moods");
      } catch (error) {
        console.error("Error al obtener las recomendaciones:", error);
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <div className="mood-form">
        <form className="mood-form__form-body" onSubmit={handleSubmit}>
          <GenreFilter selectedGenres={selectedGenres} setSelectedGenres={setSelectedGenres} />
          <div className="mood-form__form-main">
            <div className="mood-form__form-form">
              <Textarea
                id="moodText"
                value={moodText}
                onChange={(e) => setMoodText(e.target.value)}
                placeholder={t("mood-form.textarea-placeholder")}
                className="mood-form__form-textarea"
              />
              <Button type="submit" variant="primary" text={isLoading ? "Cargando..." : t("mood-form.get-playlist")} disabled={isLoading} />
            </div>
          </div>
        </form>
      </div>
    );
};
