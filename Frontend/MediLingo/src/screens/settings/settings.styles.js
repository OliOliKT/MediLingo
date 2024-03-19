import styled from "styled-components/native";
import { Ionicons } from "@expo/vector-icons";
import { Dimensions } from 'react-native';
import { Text } from 'react-native';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

export const SettingsScreenContainer = styled.View`
    flex: 1;
    align-items: center;
    margin-top: ${screenHeight * 0.2}px;
`;

export const AboutUsParagraph = styled(Text)`
    font-size: 18px;
    color: ${(props) => props.theme.colors.blacks.darkGunmetal};
    line-height: 28px;
    margin: 24px;
    text-align: justify; 
    font-family: ${(props) => props.theme.fonts.body};
  `;