import React from "react";
import { Navigation } from "./src/infrastructure/navigation";
import { ThemeProvider } from "styled-components/native";
import { theme } from "./src/infrastructure/theme";
import { AppProvider } from './src/components/context';


export default function App() {
  return (
    <>
      <AppProvider>
        <ThemeProvider theme={theme}>
          <Navigation />
        </ThemeProvider>
      </AppProvider>
    </>
  );
}