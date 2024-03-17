import React from "react";
import { Navigation } from "./src/infrastructure/navigation";
import { ThemeProvider } from "styled-components/native";
import { theme } from "./src/infrastructure/theme";


export default function App() {
  return (
    <>
      <ThemeProvider theme={theme}>
        <Navigation />
      </ThemeProvider>
    </>
  );
}