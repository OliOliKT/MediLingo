import React from "react";
import { Ionicons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import { IntroductionScreen } from "../../screens/introduction/introduction.screen";
import { TranslateScreen } from "../../screens/translate/translate.screen";
import { PromptsScreen } from "../../screens/prompts/prompts.screen";

const Tab = createBottomTabNavigator();

const TAB_ICON = {
  Translate: "newspaper",
  Introduction: "people",
  Prompts: "albums",
};

const tabBarIcon =
  (iconName) =>
  ({ size, color }) =>
    <Ionicons name={iconName} size={size} color={color} />;

const createScreenOptions = ({ route }) => {
  const iconName = TAB_ICON[route.name];
  return {
    headerShown: true,
    tabBarIcon: tabBarIcon(iconName),
    tabBarActiveTintColor: "#2182BD",
    tabBarInactiveTintColor: "gray",
  };
};

export const AppNavigator = () => (
  <Tab.Navigator screenOptions={createScreenOptions}>
    <Tab.Screen name="Introduction" component={IntroductionScreen} />
    <Tab.Screen name="Translate" component={TranslateScreen} />
    <Tab.Screen name="Prompts" component={PromptsScreen} />
  </Tab.Navigator>
);
