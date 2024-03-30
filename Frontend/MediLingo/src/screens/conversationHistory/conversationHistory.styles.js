import { StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native";
import styled from "styled-components/native";
import { Ionicons } from "@expo/vector-icons";

export const SafeArea = styled(SafeAreaView)`
    flex: 1;
`;

export const PhrasesContent = styled.View`
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: ${(props) => props.theme.space[2]};
`;

export const PhraseDetails = styled.View`
    margin: ${(props) => props.theme.space[2]};
`;

export const Phrase = styled(Text)`
    font-family: ${(props) => props.theme.fonts.body};
    font-weight: ${(props) => props.isBold ? props.theme.fontWeights.bold : props.theme.fontWeights.regular};
`;

export const Headline = styled(Text)`
    font-size: ${(props) => props.theme.fontSizes.title};
    font-family: ${(props) => props.theme.fonts.body};
    font-weight: ${(props) => props.theme.fontWeights.bold};
    margin-top: ${(props) => props.theme.space[4]};
    margin-left: ${(props) => props.theme.space[3]};
    margin-bottom: ${(props) => props.theme.space[3]};
`;

export const ItemSeparator = styled.View`
    background-color: ${(props) => props.theme.colors.blacks.eerieBlack};
    height: ${StyleSheet.hairlineWidth}px;
`;

export const PatientDoctorIcon = styled(Ionicons)`
  color: black;
  font-size: 24px;
  align-content: flex-end;
  margin-right: 12px;
  color: ${(props) => props.color};
`;