import React from "react";
import { FlatList } from "react-native";

import {
    PhrasesContent,
    ItemSeparator,
    PhraseDetails,
    Phrase,
    SafeArea,
    PatientDoctorIcon,
  } from "./conversationHistory.styles";

const CONVERSATIONS = [
    { phrase: "Chuck Norris", patient: Math.random() < 0.5 },
    { phrase: "Bruce Lee", patient: Math.random() < 0.5 },
    { phrase: "Steven Seagal", patient: Math.random() < 0.5 },
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
            color: "green",
        }
    }
    else {
        return {
            icon: "arrow-forward",
            color: "blue",
        }
    }
};

const PhraseItem = React.memo(({ item }) => {
    
    return (
        <PhrasesContent>
            <PhraseDetails>
                <Phrase>{item.phrase}</Phrase>
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