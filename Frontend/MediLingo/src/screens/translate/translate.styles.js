import styled from "styled-components/native";
import { Ionicons } from "@expo/vector-icons";
import { Dimensions } from "react-native";

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

export const TranslateScreenContainer = styled.View`
  flex: 1;
  align-items: center;
  justify-content: space-between; 
  width: 100%;
`;

export const TopContainer = styled.View`
  align-items: center;
  width: 100%;
  margin-top: 56px;
`;

export const BottomContainer = styled.View`
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
`;

export const ButtonContainer = styled.View`
  flex-direction: row;
  justify-content: center;
`;

export const ActionButton = styled.TouchableOpacity`
  height: ${screenHeight * 0.077}px;
  width: ${screenHeight * 0.077}px;
  border-radius: 50px;
  background-color: ${(props) => props.theme.colors.blues.cyanBlue};
  justify-content: center;
  align-items: center;
  margin-right: 8px;
  margin-left: 8px;
`;

export const ActionButtonIcon = styled(Ionicons)`
  color: white;
  font-size: ${screenWidth * 0.09}px;
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
`;

export const TranslateInput = styled.TextInput`
  height: ${screenHeight * 0.31}px;
  width: 96%;
  padding: 14px;
  border-radius: 4px;
  border-width: 1px;
  border-color: ${(props) => props.theme.colors.whites.chineseSilver};
  background-color: ${(props) => props.theme.colors.whites.silver};
  font-size: ${screenWidth * 0.05}px;
  font-family: ${(props) => props.theme.fonts.body};
  color: ${(props) => props.theme.colors.fontColor};
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
`;