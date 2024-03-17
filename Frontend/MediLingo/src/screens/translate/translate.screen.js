import React from "react";
import { View } from 'react-native';
import { ActionButton, ActionButtonIcon, TranslateInput, TranslateScreenContainer } from "./translate.styles";

export const TranslateScreen = () => {
    return (
        <View>
            <TranslateScreenContainer>
                <ActionButton>
                    <ActionButtonIcon name="chatbox-ellipses" reverse={true}/>
                </ActionButton>
                <View style={{ marginBottom: 10 }}></View>
                <TranslateInput reverse={true}></TranslateInput>
                <View style={{ marginBottom: 10 }}></View>
                <TranslateInput></TranslateInput>
                <View style={{ marginBottom: 10 }}></View>
                <ActionButton>
                    <ActionButtonIcon name="chatbox-ellipses" />
                </ActionButton>
            </TranslateScreenContainer>
        </View>
    );
}