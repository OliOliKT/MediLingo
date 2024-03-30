import React from "react";
import { Ionicons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { theme } from "../theme";

import { IntroductionScreen } from "../../screens/introduction/introduction.screen";
import { TranslateScreen } from "../../screens/translate/translate.screen";
import { PromptsScreen } from "../../screens/prompts/prompts.screen";
import { SettingsScreen } from "../../screens/settings/settings.screen";
import { ConversationHistoryScreen } from "../../screens/conversationHistory/conversationHistory.screen";

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const TAB_ICON = {
  Oversæt: "language",
  Spørgsmål: "albums",
  Indstillinger: "settings",
  Historik: "time",
};

const tabBarIcon =
  (iconName) =>
  ({ size, color }) =>
    <Ionicons name={iconName} size={size} color={color} />;

const createScreenOptions = ({ route }) => {
  const iconName = TAB_ICON[route.name];
  return {
    headerShown: false,
    tabBarIcon: tabBarIcon(iconName),
    tabBarActiveTintColor: theme.colors.blues.cyanBlue,
    tabBarInactiveTintColor: "gray",
  };
};

function NavigationTabs() {
  return (
    <Tab.Navigator screenOptions={createScreenOptions}>
      <Tab.Screen name="Oversæt" component={TranslateScreen} />
      <Tab.Screen name="Spørgsmål" component={PromptsScreen} />
      <Tab.Screen name="Historik" component={ConversationHistoryScreen} />
      <Tab.Screen name="Indstillinger" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export const AppNavigator = () => (
    <Stack.Navigator>
      <Stack.Screen name="Introduction" component={IntroductionScreen} options={{headerShown: false}} />
      <Stack.Screen name="Main" component={NavigationTabs} options={{headerShown: false}} />
    </Stack.Navigator>
);

