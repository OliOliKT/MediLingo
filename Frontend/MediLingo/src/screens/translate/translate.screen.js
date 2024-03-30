import { View, Image } from 'react-native';
import React, { useState, useEffect } from 'react';
import * as Speech from 'expo-speech';
import { useAppContext } from '../../components/context';
import { Audio } from 'expo-av';

import { 
    ActionButton, 
    ActionButtonIcon, 
    TranslateInput, 
    TranslateScreenContainer, 
    ButtonContainer, 
    TopContainer,
    BottomContainer
} from "./translate.styles";


export const TranslateScreen = () => {
    const [bottomInputText, setBottomInputText] = useState('');
    const [topInputText, setTopInputText] = useState('');
    const [recording, setRecording] = React.useState();
    const [isRecording, setIsRecording] = React.useState(false);
    const { addConversation, selectedPhrase, getCurrentTimeString } = useAppContext();

    useEffect(() => {
        setBottomInputText(selectedPhrase);
    }, [selectedPhrase]);

    const handleTopInputChange = (text) => {
        setTopInputText(text);
    };
    useEffect(() => {
        setTopInputText(bottomInputText);
    }, [bottomInputText]);

    const handleBottomInputChange = (text) => {
        setBottomInputText(text);
    };
    useEffect(() => {
        setBottomInputText(topInputText);
    }, [topInputText]);

    const handleSubmitDoctor = (event) => {
        const inputText = event.nativeEvent.text;
        if (inputText) {
            addConversation({ patient: false, phrase: inputText, time: getCurrentTimeString()});
        }
    }

    const handleSubmitPatient = (event) => {
        const inputText = event.nativeEvent.text;
        if (inputText) {
            addConversation({ patient: true, phrase: inputText, time: getCurrentTimeString()});
        }
    }

    const speakPatientInputText = () => {
        Speech.speak(topInputText);
    };

    const speakDoctorInputText = () => {
        Speech.speak(bottomInputText);
    };

    const startRecording = async () => {
        try {
            await Audio.requestPermissionsAsync();
            await Audio.setAudioModeAsync({
                allowsRecordingIOS: true,
                playsInSilentModeIOS: true,
            }); 
            const { recording } = await Audio.Recording.createAsync(
                Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
            );
            setRecording(recording);
            setIsRecording(true);
        } catch (err) {
            console.error('Failed to start recording', err);
        }
    }

    const stopRecording = async () => {
        setIsRecording(false);
        await recording.stopAndUnloadAsync();
        const uri = recording.getURI(); 
        sendAudioToServer(uri);
    };
    
    const toggleRecording = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const sendAudioToServer = async (audioUri) => {
        const formData = new FormData();
        formData.append('audio', {
            uri: audioUri,
            type: 'audio/m4a',
            name: 'voice-recording.m4a',
        });
    
        try {
            const response = await fetch('http://your-backend-url/transcribe', {
                method: 'POST',
                body: formData,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            const data = await response.json();
            setBottomInputText(data.text); // Assuming the server responds with JSON containing {text: "transcribed text"}
        } catch (error) {
            console.error('Error sending audio file:', error);
        }
    };

    return (
        <TranslateScreenContainer>
            <TopContainer>
                <ButtonContainer>
                    <ActionButton onPress={speakDoctorInputText}>
                        <Image 
                            source={require('../../../assets/dk_sound_icon.png')}
                            resizeMode="cover"
                            style={{ width: '55%', height: '55%', transform: [{ rotate: '180deg' }] }}
                        />
                    </ActionButton>
                    <ActionButton>
                        <ActionButtonIcon name="mic" reverse={true}/>
                    </ActionButton>
                    <ActionButton onPress={speakPatientInputText}>
                        <Image 
                                source={require('../../../assets/ukr_sound_icon.png')}
                                resizeMode="cover"
                                style={{ width: '55%', height: '55%', transform: [{ rotate: '180deg' }] }}
                        />
                    </ActionButton>
                </ButtonContainer>
                <View style={{ marginBottom: 10 }}></View>
                <TranslateInput 
                    reverse={true} 
                    value={topInputText} 
                    onChangeText={handleTopInputChange}
                    onSubmitEditing={handleSubmitPatient}
                />
            </TopContainer>
            <BottomContainer>
                <TranslateInput 
                    onChangeText={handleBottomInputChange} 
                    onSubmitEditing={handleSubmitDoctor}
                    value={bottomInputText}
                />
                <View style={{ marginBottom: 10 }}></View>
                <ButtonContainer>
                    <ActionButton onPress={speakPatientInputText}>
                    <Image 
                        source={require('../../../assets/ukr_sound_icon.png')}
                        resizeMode="cover"
                        style={{ width: '55%', height: '55%' }}
                    />
                    </ActionButton>
                    <ActionButton>
                        <ActionButtonIcon onPress={toggleRecording} name="mic" />
                    </ActionButton>
                    <ActionButton onPress={speakDoctorInputText}>
                        <Image 
                            source={require('../../../assets/dk_sound_icon.png')}
                            resizeMode="cover"
                            style={{ width: '55%', height: '55%' }}
                        />
                    </ActionButton>
                </ButtonContainer>
            </BottomContainer>
        </TranslateScreenContainer>

    );
};