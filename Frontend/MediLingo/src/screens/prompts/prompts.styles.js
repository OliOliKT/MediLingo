import { StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native";
import styled from "styled-components/native";

export const SafeArea = styled(SafeAreaView)`
    flex: 1;
`;

export const Headline = styled(Text)`
    font-size: ${(props) => props.theme.fontSizes.title};
    font-family: ${(props) => props.theme.fonts.body};
    font-weight: ${(props) => props.theme.fontWeights.bold};
    margin-top: ${(props) => props.theme.space[4]};
    margin-left: ${(props) => props.theme.space[3]};
    margin-bottom: ${(props) => props.theme.space[3]};
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
    font-weight: ${(props) => props.theme.fontWeights.medium};
`;

export const ItemSeparator = styled.View`
    background-color: ${(props) => props.theme.colors.blacks.eerieBlack};
    height: ${StyleSheet.hairlineWidth}px;
`;

export const SectionHeader = styled(Text)`
    font-size: ${(props) => props.theme.fontSizes.body};
    font-family: ${(props) => props.theme.fonts.body};
    font-weight: ${(props) => props.theme.fontWeights.bold};
    padding-left: ${(props) => props.theme.space[3]};
    padding-bottom: ${(props) => props.theme.space[2]};
    padding-top: ${(props) => props.theme.space[3]};
    background-color: ${(props) => props.theme.colors.whites.backgroundWhite};
`;