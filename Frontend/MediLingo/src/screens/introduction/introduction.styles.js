import styled from 'styled-components/native';
import { Dimensions } from 'react-native';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

export const StyledPickerContainer = styled.View`
  height: 50px;
  width: 300px;
  justify-content: center;
`;

export const IntroductionContainer = styled.View`
    flex: 1;
    align-items: center;
`;

export const StyledImage = styled.Image`
  width: 200px;
  height: 160px;
`;