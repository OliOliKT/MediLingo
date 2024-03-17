import styled from "styled-components/native";
import { Ionicons } from "@expo/vector-icons";

export const TranslateScreenContainer = styled.View`
  flex: 1;
  align-items: center;
  margin-top: 50px;
`;
export const ActionButton = styled.TouchableOpacity`
  height: 70px;
  width: 70px;
  border-radius: 50px;
  background-color: ${(props) => props.theme.colors.blues.greyCyanBlue};
  justify-content: center;
  align-items: center;
`;

export const ActionButtonIcon = styled(Ionicons)`
  color: white;
  font-size: 34px;
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
`;


export const TranslateInput = styled.TextInput`
  height: 266px;
  width: 96%;
  padding: 14px;
  border-radius: 4px;
  border-width: 1px;
  border-color: ${(props) => props.theme.colors.whites.chineseSilver};
  background-color: ${(props) => props.theme.colors.whites.silver};
  font-size: 22px;
  font-family: Arial;
  color: ${(props) => props.theme.colors.fontColor};
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
`;