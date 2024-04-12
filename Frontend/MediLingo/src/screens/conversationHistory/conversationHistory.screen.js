import React from "react";
import { FlatList, View } from "react-native";
import { theme } from "../../infrastructure/theme/index";
import { useAppContext } from '../../components/context';
import { IconTextButton } from "../../components/iconTextButton.component";
import { Share } from 'react-native';

import {
    PhrasesContent,   
    ItemSeparator,
    PhraseDetails,
    Phrase,
    SafeArea,
    PatientDoctorIcon,
    Headline
  } from "./conversationHistory.styles";

const patientDoctor = (patient) => {

    if (patient) {
        return {
            icon: "arrow-back",
            color: theme.colors.greens.mint,
            string: "Patient",
        }
    }
    else {
        return {
            icon: "arrow-forward",
            color: theme.colors.blues.cyanBlue,
            string: "Læge",
        }
    }
};

const truncateText = (text, maxLength = 44) => {
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
                <Phrase isBold={true}>{`${patientDoctor(item.patient).string} (${item.time}):`}</Phrase>
                <Phrase>"{truncatedPhrase}"</Phrase>
            </PhraseDetails>
            <PatientDoctorIcon 
                name={patientDoctor(item.patient).icon}
                color={patientDoctor(item.patient).color}>
            </PatientDoctorIcon>
        </PhrasesContent>
    );
    });
        
    export const ConversationHistoryScreen = () => {
        const { conversations } = useAppContext();
        const renderItem = ({ item }) => <PhraseItem item={item} />;

        const handlePress = () => {
        const formattedConversations = conversations.map(conv => {
            const speaker = conv.patient ? "Patient" : "Læge";
            return `${speaker} (${conv.time}):\n"${conv.phrase}"`;
        }).join('\n\n');

        Share.share({
            message: "Samtalehistorik: \n\n" + formattedConversations,
            title: 'Del samtale',
        }).then((result) => {
            console.log('Share was successful:', result);
        }).catch((error) => {
            console.log('Share failed:', error.message);
        });
        };
    
    return (
        <SafeArea>
            <Headline>Samtalehistorik:</Headline>
            <ItemSeparator />
            <FlatList
                data={conversations}
                keyExtractor={(_, i) => String(i)}
                renderItem={renderItem}
                ItemSeparatorComponent={ItemSeparator}
            />
            <IconTextButton 
                onPress={handlePress} 
                iconName="arrow-forward"
                buttonText="Eksporter samtalehistorik"
            />
            <View style={{ marginBottom: 24 }} />
        </SafeArea>
    );
};