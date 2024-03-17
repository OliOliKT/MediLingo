import React from "react";
import { Ionicons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { theme } from "../theme";

import { IntroductionScreen } from "../../screens/introduction/introduction.screen";
import { TranslateScreen } from "../../screens/translate/translate.screen";
import { PromptsScreen } from "../../screens/prompts/prompts.screen";
import { SettingsScreen } from "../../screens/settings/settings.screen";
import { ConversationHistoryScreen } from "../../screens/conversationHistory/conversationHistory.screen";

const Tab = createBottomTabNavigator();

const TAB_ICON = {
  Translate: "chatbox",
  Introduction: "people",
  Prompts: "albums",
  Settings: "settings",
  "History": "time",
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
    tabBarActiveTintColor: theme.colors.greens.cyanBlue,
    tabBarInactiveTintColor: "gray",
  };
};

export const AppNavigator = () => (
  <Tab.Navigator screenOptions={createScreenOptions}>
    <Tab.Screen name="Introduction" component={IntroductionScreen} />
    <Tab.Screen name="Prompts" component={PromptsScreen} />
    <Tab.Screen name="Translate" component={TranslateScreen} />
    <Tab.Screen name="History" component={ConversationHistoryScreen} />
    <Tab.Screen name="Settings" component={SettingsScreen} />
  </Tab.Navigator>
);
