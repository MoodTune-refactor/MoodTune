import { useState } from "react";
import { GetMoodForm } from "../../components/GetMoodForm/GetMoodForm";
import { GetRecommendationForm } from "../../components/GetRecommendationForm/GetRecommendationForm";
import { useTranslation } from "react-i18next";
import Button from "../../components/Button/Button";
import "./MainForm.scss";

const MoodForm = () => {
  const { t } = useTranslation();
  const [showMoodForm, setShowMoodForm] = useState(true);

  return (
    <div className="main-form">
      <div className="main-form__title-container">
        <h4 className="main-form__form-title">{t("mood-form.title")}</h4>
        <div className="main-form__toggle">
          <Button 
            type="button" 
            variant={showMoodForm ? "primary" : "secondary"} 
            text={t('mood-form.get-playlist-mood')} 
            onClick={() => setShowMoodForm(true)}
            className={showMoodForm ? "selected" : ""}
          />
          <Button 
            type="button" 
            variant={!showMoodForm ? "primary" : "secondary"} 
            text={t('mood-form.get-playlist-preferences')} 
            onClick={() => setShowMoodForm(false)}
            className={!showMoodForm ? "selected" : ""}
          />
        </div>
      </div>
      {showMoodForm ? <GetMoodForm /> : <GetRecommendationForm />}
    </div>
  );
};

export default MoodForm;