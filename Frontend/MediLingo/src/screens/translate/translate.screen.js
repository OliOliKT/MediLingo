import { View } from 'react-native';
import React, { useState, useEffect } from 'react';
import { ActionButton, ActionButtonIcon, TranslateInput, TranslateScreenContainer } from "./translate.styles";

export const TranslateScreen = () => {
    const [bottomInputText, setBottomInputText] = useState('');
    const [topInputText, setTopInputText] = useState('');

    const handleTopInputChange = (text) => {
        setTopInputText(text);
    };

    const handleBottomInputChange = (text) => {
        setBottomInputText(text);
    };

    useEffect(() => {
        setBottomInputText(topInputText);
    }, [topInputText]);

    React.useEffect(() => {
        setTopInputText(bottomInputText);
    }, [bottomInputText]);

    return (
        <TranslateScreenContainer>
            <ActionButton>
                <ActionButtonIcon name="chatbox-ellipses" reverse={true}/>
            </ActionButton>
            <View style={{ marginBottom: 10 }}></View>
            <TranslateInput 
                reverse={true} 
                value={topInputText} 
                onChangeText={handleTopInputChange}
            />
            <View style={{ marginBottom: 10 }}></View>
            <TranslateInput 
                onChangeText={handleBottomInputChange} 
                value={bottomInputText}
            />
            <View style={{ marginBottom: 10 }}></View>
            <ActionButton>
                <ActionButtonIcon name="chatbox-ellipses" />
            </ActionButton>
        </TranslateScreenContainer>
    );
};