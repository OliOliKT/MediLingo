import { View, Image, Keyboard, ActivityIndicator } from 'react-native';
import React, { useState, useEffect } from 'react';
import * as Speech from 'expo-speech';
import { useAppContext } from '../../components/context';
import { Audio } from 'expo-av';
import { storage, fetchApiKey } from '../../infrastructure/firebase';
import { ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage';
import OpenAI from 'openai';

import { 
    SoundButton, 
    MicButton,
    ActionButtonIcon, 
    TranslateInput, 
    TranslateScreenContainer, 
    ButtonContainer, 
    TopContainer,
    BottomContainer,
    DeleteButton,
} from "./translate.styles";

export const TranslateScreen = () => {
    const [bottomInputText, setBottomInputText] = useState('');
    const [topInputText, setTopInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const [recording, setRecording] = useState();

    const [isRecording, setIsRecording] = useState(false);
    const [openaiClient, setOpenaiClient] = useState(null);
    const [transcriptionLanguage, setTranscriptionLanguage] = useState('');

    const { addConversation, selectedPhrase, getCurrentTimeString, shouldUpdateBottomText, setShouldUpdateBottomText } = useAppContext();


    useEffect(() => {
        fetchApiKey().then(apiKey => {
            if (apiKey) {
                const config = new OpenAI({ apiKey: apiKey.trim() });
                const client = new OpenAI(config);
                setOpenaiClient(client);
            }
        });
    }, []);

    const runDanishPrompt = async (prompt) => {
        if (openaiClient) {
            const response = await openaiClient.chat.completions.create({
                model: "ft:gpt-3.5-turbo-0125:personal:medilingo:94Zh7J6M",
                messages: [
                    { role: "system", content: "You are a medical translator. Your task is to translate the following text from Danish to Ukrainian for use in a radiology department. Ensure the translation is accurate, preserves the original meaning, and maintains a formal and professional tone. If the text is ambiguous, nonsensical, or cannot be reasonably translated, respond with: 'Teksten kan ikke oversættes meningsfuldt.' Do not guess or create information." },
                    { role: "user", content: prompt },
                ],
            });
            return response.choices[0].message.content;
        }
    };

    const runUkrainianPrompt = async (prompt) => {
        if (openaiClient) {
            const response = await openaiClient.chat.completions.create({
                model: "ft:gpt-3.5-turbo-0125:personal:uktodk:9ENr7qy1",
                messages: [
                    { role: "system", content: "You are a medical translator. Your task is to translate the following text from Ukrainian to Danish for use in a radiology department. Ensure the translation is accurate, preserves the original meaning, and maintains a formal and professional tone. If the text is ambiguous, nonsensical, or cannot be reasonably translated, respond with: 'Teksten kan ikke oversættes meningsfuldt.' Do not guess or create information." },
                    { role: "user", content: prompt },
                ],
            });
            return response.choices[0].message.content;
        }
    };

    useEffect(() => {
        if (shouldUpdateBottomText) {
            setBottomInputText(selectedPhrase);
            handleSubmitDoctor(selectedPhrase);
            setShouldUpdateBottomText(false);
        }
    }, [selectedPhrase, shouldUpdateBottomText]);
    
    const deleteText = () => {
        setBottomInputText('');
        setTopInputText('');
        Keyboard.dismiss();
    };

    const handleSubmitDoctor = async (input) => {
        const inputText = input.nativeEvent && input.nativeEvent.text ? input.nativeEvent.text : input;

        if (inputText) {
            addConversation({ patient: false, phrase: inputText, time: getCurrentTimeString() });
            setLoading(true);
            try {
                const translatedText = await runDanishPrompt(inputText);
                setTopInputText(translatedText);
            } catch (error) {
                console.error('Error getting translation:', error);
            } finally {
                setLoading(false);
            }
        } else {
            setTopInputText('');
        }
    };

    const handleSubmitPatient = async (input) => {
        const inputText = input.nativeEvent && input.nativeEvent.text ? input.nativeEvent.text : input;

        if (inputText) {
            addConversation({ patient: true, phrase: inputText, time: getCurrentTimeString() });
            setLoading(true);
            try {
                const translatedText = await runUkrainianPrompt(inputText);
                setBottomInputText(translatedText);
            } catch (error) {
                console.error('Error getting translation:', error);
            } finally {
                setLoading(false);
            }
        } else {
            setBottomInputText('');
        }
    };

    const speakPatientInputText = () => {
        const options = {
            volume: 1.0,
            language: "uk",
        };
        Speech.speak(topInputText, options);
    };

    const speakDoctorInputText = () => {
        const options = {
            volume: 1.0,
        };
        Speech.speak(bottomInputText, options);
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
            console.log('Recording started');
        } catch (err) {
            console.error('Failed to start recording', err);
        }
    }

    const stopRecording = async () => {
        setIsRecording(false);
        setLoading(true);
        await recording.stopAndUnloadAsync();
        const uri = recording.getURI(); 
        console.log('Recording stopped and stored at', uri);
        sendAudioToServer(uri);
    };
    
    const toggleRecording = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const sendAudioToServer = async (uri) => {
        try {
            const response = await fetch(uri);
            const blob = await response.blob();
            const timestamp = new Date().getTime();
            const file_name = `${transcriptionLanguage}/${timestamp}-audio-file.flac`;
            console.log("Transcription language:", transcriptionLanguage);
            console.log('File name:', file_name);
          
            const storageRef = ref(storage, `transcriptions/${file_name}`);
            await uploadBytes(storageRef, blob);

            fetchTranscription(file_name, transcriptionLanguage);
    
        } catch (error) {
            console.error('Error uploading file or fetching transcription:', error);
            setLoading(false);
        }
    };

    const fetchTranscription = async (fileName, transcriptionLanguage) => {
        const txtFileRef = ref(storage, `transcriptions/${transcriptionLanguage}/transcriptions/${fileName}.wav_transcription.txt`);
        console.log("Transcription file reference:", txtFileRef);
        let attemptCount = 0;
        const maxAttempts = 12;

        const loadingInterval = setInterval(() => {
        }, 700);
    
        const checkTranscriptionAvailable = async () => {
            attemptCount++;
            if (attemptCount > maxAttempts) {
                console.log('Maximum attempts reached. Stopping check.');
                clearInterval(checkInterval);
                transcriptionLanguage === 'uk-UA' ? setTopInputText('No transcription available') : setBottomInputText('Transkribering ikke tilgængelig');
                clearInterval(loadingInterval); 
                setLoading(false);
                return;
            }
            try {
                const url = await getDownloadURL(txtFileRef);
                const response = await fetch(url);
                const transcriptionData = await response.json();
                
                if (transcriptionData && transcriptionData.results.length > 0) {
                    const transcript = transcriptionData.results.map(result => result.alternatives[0].transcript).join('\n');
                    console.log('Transcription:', transcript);
                    if (transcriptionLanguage === 'uk-UA') { 
                        setTopInputText(transcript);
                        console.log("Top input text:", transcript);
                        handleSubmitPatient(transcript);
                    }
                    else { 
                        setBottomInputText(transcript);
                        console.log("Bottom input text:", transcript);
                        handleSubmitDoctor(transcript);
                    }
                    clearInterval(checkInterval);
                    deleteTranscriptionFile(txtFileRef);
                    const audioFile = ref(storage, `transcriptions/${fileName}`);
                    deleteTranscriptionFile(audioFile)
                    setLoading(false);

                } else {
                    console.log('Transcription file found but no results.');
                    transcriptionLanguage === 'uk-UA' ? setTopInputText('Транскрипція недоступна') : setBottomInputText('Transkribering ikke tilgængelig');
                    clearInterval(checkInterval);
                    setLoading(false);
                }
                clearInterval(loadingInterval); 
            } catch (error) {
                console.log('Transcription file not ready yet, checking again...');
            }
        };
    
        let checkInterval = setInterval(checkTranscriptionAvailable, 1000);
    };

    const deleteTranscriptionFile = async (fileRef) => {
        deleteObject(fileRef)
            .then(() => {
                console.log('File deleted successfully:', fileRef.fullPath);
            })
            .catch((error) => {
                if (error.code === 'storage/object-not-found') {
                    console.log('File does not exist, nothing to delete:', fileRef.fullPath);
                } else {
                    console.error('Error deleting file:', fileRef.fullPath, error);
                }
            });
    };
      

    return (
        <TranslateScreenContainer>
            {loading && (
                <View style={{ 
                    position: 'absolute', 
                    top: 50, 
                    left: 0, 
                    right: 0, 
                    bottom: 0, 
                    backgroundColor: 'rgba(0, 0, 0, 0.5)', 
                    justifyContent: 'center', 
                    alignItems: 'center',
                    zIndex: 10 
                }}>
                    <ActivityIndicator size="large" color="#ffffff" />
                </View>
            )}
            
            <TopContainer>
                <ButtonContainer>
                    <SoundButton onPress={speakDoctorInputText}>
                        <Image 
                            source={require('../../../assets/dk_sound_icon.png')}
                            resizeMode="cover"
                            style={{ width: '55%', height: '55%', transform: [{ rotate: '180deg' }] }}
                        />
                    </SoundButton>

                    <MicButton onPress={() => {
                        if (!isRecording) {
                            setTranscriptionLanguage('uk-UA');
                            toggleRecording();
                        } else if (transcriptionLanguage === 'uk-UA') {
                            toggleRecording();
                        }
                    }} isRecording={isRecording && transcriptionLanguage === 'uk-UA'}>
                        <ActionButtonIcon name={isRecording && transcriptionLanguage === 'uk-UA' ? "square" : "mic"} reverse={true}/>
                    </MicButton>

                    <SoundButton onPress={speakPatientInputText}>
                        <Image 
                                source={require('../../../assets/ukr_sound_icon.png')}
                                resizeMode="cover"
                                style={{ width: '55%', height: '55%', transform: [{ rotate: '180deg' }] }}
                        />
                    </SoundButton>
                </ButtonContainer>
                <View style={{ marginBottom: 10 }}></View>
                <TranslateInput
                    reverse={true}
                    onChangeText={(text) => setTopInputText(text)}
                    onSubmitEditing={() => handleSubmitPatient(topInputText)}
                    blurOnSubmit={true}
                    multiline={true}
                    value={topInputText}
                    editable={false}
                />
            </TopContainer>

            {(topInputText || bottomInputText) && (
                <DeleteButton onPress={deleteText}>
                    <ActionButtonIcon name={'close'} />
                </DeleteButton>
            )}

                <BottomContainer>
                <TranslateInput
                    onChangeText={(text) => setBottomInputText(text)}
                    onSubmitEditing={() => handleSubmitDoctor(bottomInputText)}
                    multiline={true}
                    blurOnSubmit={true}
                    value={bottomInputText}
                />
                <View style={{ marginBottom: 10 }} />
                <ButtonContainer>
                    <SoundButton onPress={speakPatientInputText}>
                    <Image 
                        source={require('../../../assets/ukr_sound_icon.png')}
                        resizeMode="cover"
                        style={{ width: '55%', height: '55%' }}
                    />
                    </SoundButton>
                    <MicButton onPress={() => {
                        if (!isRecording) {
                            setTranscriptionLanguage('da-DK');
                            toggleRecording();
                        } else if (transcriptionLanguage === 'da-DK') {
                            toggleRecording();
                        }
                    }} isRecording={isRecording && transcriptionLanguage === 'da-DK'}>
                        <ActionButtonIcon name={isRecording && transcriptionLanguage === 'da-DK' ? "square" : "mic"} />
                    </MicButton>

                    <SoundButton onPress={speakDoctorInputText}>
                        <Image 
                            source={require('../../../assets/dk_sound_icon.png')}
                            resizeMode="cover"
                            style={{ width: '55%', height: '55%' }}
                        />
                    </SoundButton>
                </ButtonContainer>
            </BottomContainer>
        </TranslateScreenContainer>
    );
};