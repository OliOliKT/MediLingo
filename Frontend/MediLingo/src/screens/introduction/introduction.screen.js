import React, { useState } from "react";
import { IntroductionContainer, StyledPickerContainer, StyledImage } from "./introduction.styles";
import { IconTextButton } from "../../components/iconTextButton.component";
import { useNavigation } from '@react-navigation/native';
import { Picker } from '@react-native-picker/picker';
import { View } from 'react-native';

export const DepartmentDropdown = () => {
    const [selectedValue, setSelectedValue] = useState("java");
    return (
        <StyledPickerContainer>
            <Picker
                selectedValue={selectedValue}
                onValueChange={(itemValue) => setSelectedValue(itemValue)}
                style={{ width: '100%', height: '100%' }}
            >
            <Picker.Item label="X-ray imaging" value="xRayImaging" />
            <Picker.Item label="CT scanning" value="ctScanning" />
            <Picker.Item label="MRI scanning" value="mriScanning" />
            <Picker.Item label="Ultrasound" value="ultrasound" />
            </Picker>
        </StyledPickerContainer>
    );
};

export const LanguageDropdown = () => {
    const [selectedValue, setSelectedValue] = useState("java");
    return (
        <StyledPickerContainer>
            <Picker
                selectedValue={selectedValue}
                onValueChange={(itemValue) => setSelectedValue(itemValue)}
                style={{ width: '100%', height: '100%' }}
            >
            <Picker.Item label="Ukrainian" value="ukrainan" />
            <Picker.Item label="English" value="english" />
            <Picker.Item label="German" value="german" />
            <Picker.Item label="French" value="french" />
            </Picker>
        </StyledPickerContainer>
    );
};

export const IntroductionScreen = () => {
    const navigation = useNavigation();

    const handlePress = () => {
        navigation.navigate('Main');
    };

    return (
        <IntroductionContainer>
            <View style={{ marginBottom: 80 }} />
            <StyledImage source={require('../../../assets/logo.png')} />
            <View style={{ marginBottom: 0 }} />
            <LanguageDropdown />
            <View style={{ marginBottom: 130 }} />
            <DepartmentDropdown />
            <View style={{ marginBottom: 190 }} />
            <IconTextButton 
                onPress={handlePress} 
                iconName="arrow-forward" 
                buttonText="Begin now" 
            />
        </IntroductionContainer>
    );
};