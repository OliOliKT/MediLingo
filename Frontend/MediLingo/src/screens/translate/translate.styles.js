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
  align-items: center;
`;

export const DeleteButton = styled.TouchableOpacity`
  position: absolute;
  right: ${screenWidth * 0.43}px;
  bottom: ${screenHeight * 0.395}px;
  height: ${screenHeight * 0.066}px;
  width: ${screenHeight * 0.066}px;
  border-radius: 50px;
  background-color: ${(props) => props.theme.colors.blues.cyanBlue};
  justify-content: center;
  align-items: center;
  shadow-color: #000;
  shadow-opacity: 0.15;
  shadow-radius: 3.84px;
  elevation: 5;
  zIndex: 20;
`;

export const SoundButton = styled.TouchableOpacity`
  height: ${screenHeight * 0.076}px;
  width: ${screenHeight * 0.076}px;
  border-radius: 50px;
  background-color: ${(props) => props.theme.colors.blues.cyanBlue};
  justify-content: center;
  align-items: center;
  margin-right: 10px;
  margin-left: 10px;
  shadow-color: #000;
  shadow-opacity: 0.15;
  shadow-radius: 3.84px;
  elevation: 5;
`;

export const MicButton = styled.TouchableOpacity`
  height: ${screenHeight * 0.085}px;
  width: ${screenHeight * 0.085}px;
  border-radius: 50px;
  background-color: ${props => props.isRecording ? props.theme.colors.recordingColor : props.theme.colors.blues.greyCyanBlue};
  justify-content: center;
  align-items: center;
  margin-right: 8px;
  margin-left: 8px;
  shadow-color: #000;
  shadow-opacity: 0.25;
  shadow-radius: 3.84px;
  elevation: 5;
`;

export const ActionButtonIcon = styled(Ionicons)`
  color: white;
  font-size: ${screenWidth * 0.105}px;
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
`;

export const TranslateInput = styled.TextInput`
  height: ${screenHeight * 0.305}px;
  width: 96%;
  padding: 16px;
  border-radius: 10px;
  border: 0.45px solid ${(props) => props.theme.colors.whites.chineseSilver}; 
  background-color: ${(props) => props.theme.colors.whites.silver};
  font-size: ${screenWidth * 0.06}px;
  font-weight: ${(props) => props.theme.fontWeights.medium};
  font-family: ${(props) => props.theme.fonts.body};
  color: ${(props) => props.theme.colors.fontColor};
  transform: ${(props) => props.reverse ? 'rotate(180deg)' : ''};
  textAlignVertical: top;
  shadow-color: #000;
  shadow-opacity: 0.1;
  shadow-radius: 4px;
  elevation: 5;
`;
