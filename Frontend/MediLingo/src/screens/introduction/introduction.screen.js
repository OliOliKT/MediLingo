import React, { useState } from "react";
import { IntroductionContainer, StyledPickerContainer, StyledImage } from "./introduction.styles";
import { IconTextButton } from "../../components/iconTextButton.component";
import { useNavigation } from '@react-navigation/native';
import { Picker } from '@react-native-picker/picker';
import { View } from 'react-native';
import { useAppContext } from '../../components/context';

export const DepartmentDropdown = () => {
    const { selectedDepartment, setDepartment } = useAppContext();
    const placeholderItem = { label: "Vælg afdeling:", value: undefined, color: '#9e9e9e' };

    return (
        <StyledPickerContainer>
            <Picker
                selectedValue={selectedDepartment}
                onValueChange={(itemValue, itemIndex) => itemIndex !== 0 && setDepartment(itemValue)}
                style={{ width: '100%', height: '100%' }}
            >
                <Picker.Item {...placeholderItem} />
                <Picker.Item label="CT-scanning" value="ctScanning" />
                <Picker.Item label="MR-scanning" value="mriScanning" />
                <Picker.Item label="Ultralyd" value="ultrasound" />
            </Picker>
        </StyledPickerContainer>
    );
};

export const LanguageDropdown = () => {
    const [selectedValue, setSelectedValue] = useState();
    const placeholderItem = { label: "Vælg patientens sprog:", value: undefined, color: '#9e9e9e' };

    return (
        <StyledPickerContainer>
            <Picker
                selectedValue={selectedValue}
                onValueChange={(itemValue, itemIndex) => itemIndex !== 0 && setSelectedValue(itemValue)}
                style={{ width: '100%', height: '100%' }}
            >
                <Picker.Item {...placeholderItem} />
                <Picker.Item label="Ukrainsk" value="ukrainan" />
                <Picker.Item label="Engelsk" value="english" />
                <Picker.Item label="Tysk" value="german" />
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
            <View style={{ marginBottom: 10 }} />
            <LanguageDropdown />
            <View style={{ marginBottom: 130 }} />
            <DepartmentDropdown />
            <View style={{ marginBottom: 160 }} />
            <IconTextButton 
                onPress={handlePress} 
                iconName="arrow-forward" 
                buttonText="Begynd nu" 
            />
        </IntroductionContainer>
    );
};