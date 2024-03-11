import styled from "styled-components/native";

export const ArticleItem = styled.View`
  background-color: ${(props) => props.theme.colors.bg.primary};
  padding-vertical: ${(props) => props.theme.space[2]};
`;

export const ArticleDate = styled(Text)`
  font-family: ${(props) => props.theme.fonts.heading};
  font-size: ${(props) => props.theme.fontSizes.caption};
  opacity: 0.5;
`;