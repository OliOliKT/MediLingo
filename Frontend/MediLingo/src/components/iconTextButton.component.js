import React from 'react';
import styled from 'styled-components/native';
import { Dimensions } from 'react-native';
import { Ionicons } from "@expo/vector-icons";

const screenWidth = Dimensions.get('window').width;

export const IconTextButton = ({ onPress, iconName, buttonText }) => {
    return (
        <ButtonContainer onPress={onPress}>
            <ButtonText>{buttonText}</ButtonText>
            <ActionButtonIcon name={iconName} />
        </ButtonContainer>
    );
};

const ButtonContainer = styled.TouchableOpacity`
    flex-direction: row;
    align-items: center;
    align-self: center;
    background-color: ${(props) => props.theme.colors.blues.cyanBlue};
    padding: 10px 20px;
    border-radius: 5px;
    margin: 10px;
`;

const ButtonText = styled.Text`
    color: white;
    margin-right: 10px;
    font-size: ${screenWidth * 0.05}px;
    font-weight: ${(props) => props.theme.fontWeights.bold};
`;

export const ActionButtonIcon = styled(Ionicons)`
    color: white;
    font-size: ${screenWidth * 0.09}px;
`;