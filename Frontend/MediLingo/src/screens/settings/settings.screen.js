import React from "react";
import { SettingsScreenContainer, AboutUsParagraph } from "./settings.styles";
import { useNavigation } from '@react-navigation/native';
import { IconTextButton } from "../../components/iconTextButton.component";


export const SettingsScreen = () => {

    const navigation = useNavigation();

    const handleReturnButtonPress = () => {
        navigation.navigate('Introduction');
    };

    return (
        <SettingsScreenContainer>
            <AboutUsParagraph>
            {"This application is developed by Maja Styrk Andersen, Simon Min Olafsson " +
            "and Oliver Kronholm Thomsen. This is part of a master thesis project at " +
            "the Software Design MSc at the IT University of Copenhagen.\n\n" +
            "This app is an interpreter tool that is to be used in hospitals to help " +
            "in facilitating translation between healthcare professionals and non-native " +
            "speaking patients."}
            </AboutUsParagraph>
            <IconTextButton 
                onPress={handleReturnButtonPress} 
                iconName="arrow-forward" 
                buttonText="Tilbage til menuen" 
            />
        </SettingsScreenContainer>
    );
}