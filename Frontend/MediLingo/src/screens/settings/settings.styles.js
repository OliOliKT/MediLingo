import styled from "styled-components/native";

export const ReturnButton = styled.TouchableOpacity`
    height: 70px;
    width: 70px;
    border-radius: 50px;
    background-color: ${(props) => props.theme.colors.blues.greyCyanBlue};
    justify-content: center;
    align-items: center;
    margin: 100px;
    `;