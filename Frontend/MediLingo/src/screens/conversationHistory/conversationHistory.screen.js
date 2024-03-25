import React from "react";
import { FlatList } from "react-native";
import { theme } from "../../infrastructure/theme/index";

import {
    PhrasesContent,
    ItemSeparator,
    PhraseDetails,
    Phrase,
    SafeArea,
    PatientDoctorIcon,
  } from "./conversationHistory.styles";

const CONVERSATIONS = [
    { phrase: "Chuck Norris is an actor who acts in a lot of movies", patient: Math.random() < 0.5 },
    { phrase: "Bruce Lee is the name of another actor", patient: Math.random() < 0.5 },
    { phrase: "Steven Seagal is someone i dont know who is but i recognize the name", patient: Math.random() < 0.5 },
    { phrase: "Tony Jaa", patient: Math.random() < 0.5 },
    { phrase: "Jet Li", patient: Math.random() < 0.5 },
    { phrase: "Jean Claude Van Damme", patient: Math.random() < 0.5 },
    { phrase: "Sonny Chiba", patient: Math.random() < 0.5 },
    { phrase: "Jackie Chan", patient: Math.random() < 0.5 },
    { phrase: "Iko Uwais", patient: Math.random() < 0.5 },
    { phrase: "Donnie Yen", patient: Math.random() < 0.5 },
    { phrase: "Gordon Liu", patient: Math.random() < 0.5 },
    { phrase: "Chow Yun-Fat", patient: Math.random() < 0.5 },
    { phrase: "Sammo Hung", patient: Math.random() < 0.5 },
    { phrase: "Toshiro Mifune", patient: Math.random() < 0.5 },
    { phrase: "Phillip Rhee", patient: Math.random() < 0.5 },
    { phrase: "Cheng Pei-Pei", patient: Math.random() < 0.5 },
    { phrase: "Bolo Yeung", patient: Math.random() < 0.5 },
    { phrase: "Jeff Speakman", patient: Math.random() < 0.5 },
    { phrase: "Bill Superfoot Wallace", patient: Math.random() < 0.5 },
    { phrase: "Dragon Lee", patient: Math.random() < 0.5 },
];

const patientDoctorIcon = (patient) => {

    if (patient) {
        return {
            icon: "arrow-back",
            color: theme.colors.greens.mint,
            string: "Patient: ",
        }
    }
    else {
        return {
            icon: "arrow-forward",
            color: theme.colors.blues.cyanBlue,
            string: "Doctor: ",
        }
    }
};

const truncateText = (text, maxLength = 46) => {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + "...";
    }
    return text;
};

const PhraseItem = React.memo(({ item }) => {

    const truncatedPhrase = truncateText(item.phrase);
    
    return (
        <PhrasesContent>
            <PhraseDetails>
                <Phrase isBold={true}>{patientDoctorIcon(item.patient).string} </Phrase>
                <Phrase>{truncatedPhrase}</Phrase>
            </PhraseDetails>
            <PatientDoctorIcon 
                name={patientDoctorIcon(item.patient).icon} 
                color={patientDoctorIcon(item.patient).color}>
            </PatientDoctorIcon>
        </PhrasesContent>
    );
    });
    
export const ConversationHistoryScreen = () => {
    const renderItem = ({ item }) => <PhraseItem item={item} />;
    
    return (
        <SafeArea>
        <FlatList
            data={CONVERSATIONS}
            keyExtractor={(_, i) => String(i)}
            renderItem={renderItem}
            ItemSeparatorComponent={ItemSeparator}
        />
        </SafeArea>
    );
};