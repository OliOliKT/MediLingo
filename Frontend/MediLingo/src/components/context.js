import React, { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const useAppContext = () => useContext(AppContext);

export const AppProvider = ({ children }) => {
    const [conversations, setConversations] = useState([]);
    const [selectedDepartment, setSelectedDepartment] = useState("xRayImaging");
    const [selectedPhrase, setSelectedPhrase] = useState("");
    const [shouldUpdateBottomText, setShouldUpdateBottomText] = useState(false);


    const addConversation = (item) => {
        setConversations((prevConversations) => [...prevConversations, item]);
    };

    const setDepartment = (department) => {
        setSelectedDepartment(department);
    };

    const updateSelectedPhrase = (phrase, shouldUpdate = false) => {
        setSelectedPhrase(phrase);
        setShouldUpdateBottomText(shouldUpdate);
    };

    const getCurrentTimeString = () => {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    };

    return (
        <AppContext.Provider value={{
            conversations, 
            addConversation, 
            selectedDepartment, 
            setDepartment, 
            selectedPhrase,
            updateSelectedPhrase,
            getCurrentTimeString,
            shouldUpdateBottomText,
            setShouldUpdateBottomText,
        }}>
            {children}
        </AppContext.Provider>
    );
};
