import React from "react";
import "./Notifications.scss";

interface NotificationsProps {
    message: string;
    variant: 'error' | 'success';
    onClose: () => void;
}

const Notifications: React.FC<NotificationsProps> = ({ message, variant, onClose }) => {
    if (!message) return null;

    return (
        <div className={`notifications-popup ${variant}-popup`}>
            <div className={`${variant}-popup__content`}>
                <p>{message}</p>
                <button onClick={onClose} className={`${variant}-popup__close`}>
                    <span className="icon icon-cross"></span>
                </button>
            </div>
        </div>
    );
};

export default Notifications;
