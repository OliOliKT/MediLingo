import { View, Image, Keyboard } from 'react-native';
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

    const [recording, setRecording] = useState();
    const [isRecording, setIsRecording] = useState(false);

    const [transcript, setTranscript] = useState('');

    const [transcriptionLanguage, setTranscriptionLanguage] = useState('');

    const [openaiClient, setOpenaiClient] = useState(null);

    const { addConversation, selectedPhrase, getCurrentTimeString, shouldUpdateBottomText, setShouldUpdateBottomText } = useAppContext();

    useEffect(() => {
        fetchApiKey().then(apiKey => {
        if (apiKey) {
            const config = new OpenAI({
            apiKey: apiKey.trim(),
            });

            const client = new OpenAI(config);
            setOpenaiClient(client);
        }
        });
    }, []);

    const runDanishPrompt = async (prompt) => { 
        if (openaiClient) {
            const response = await openaiClient.chat.completions.create({
                model: "ft:gpt-3.5-turbo-0125:personal:medilingo:94WHfDoL",
                messages: [
                    { role: "system", content: "Translate from Danish to Ukrainian for medical purposes ONLY!" },
                    { role: "user", content: prompt },
                ],
            });
        
            console.log('Response:', response);
            const completionText = response.choices[0].message.content;
            return completionText;
        }
    };

    const runUkranianPrompt = async (prompt) => { 
        if (openaiClient) {
            const response = await openaiClient.chat.completions.create({
                model: "ft:gpt-3.5-turbo-0125:personal:medilingo:94WHfDoL",
                messages: [
                    { role: "system", content: "Translate from Ukrainian to Danish for medical purposes ONLY!" },
                    { role: "user", content: prompt },
                ],
            });
        
            console.log('Response:', response);
            const completionText = response.choices[0].message.content;
            return completionText;
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
        setBottomInputText("");
        setTopInputText("");
        Keyboard.dismiss();
    };

    const handleSubmitDoctor = async (input) => {
        const inputText = input.nativeEvent && input.nativeEvent.text ? input.nativeEvent.text : input;

        if (inputText) {
            addConversation({ patient: false, phrase: inputText, time: getCurrentTimeString()});
            console.log('Bottom input text:', inputText);
            try {
                const translatedText = await runDanishPrompt(inputText);
                console.log("Translated text:", translatedText);
                setTopInputText(translatedText);
            } catch (error) {
                console.error("Error getting translation:", error);
            }
        }
        else {
            setTopInputText("");
        }
    }

    const handleSubmitPatient = async (input) => {
        const inputText = input.nativeEvent && input.nativeEvent.text ? input.nativeEvent.text : input;
        if (inputText) {
            addConversation({ patient: true, phrase: inputText, time: getCurrentTimeString()});
            console.log('Top input text:', inputText);
            try {
                const translatedText = await runUkranianPrompt(inputText);
                console.log("Translated text:", translatedText);
                setBottomInputText(translatedText);
            } catch (error) {
                console.error("Error getting translation:", error);
            }
        }
        else {
            setBottomInputText("");
        }
    }

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
        console.log('Recording stopped');
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

    // const sendAudioToServer = async (uri) => {
    //     try {
    //       const response = await fetch(uri);
    //       const blob = await response.blob();
    //       const file_name = 'audio-file.flac';
          
    //       const storageRef = ref(storage, `uploads/${file_name}`);
    //       console.log('Uploading audio to', storageRef.fullPath);
      
    //       await uploadBytes(storageRef, blob);
    //       console.log('Upload complete, attempting to fetch transcription');
    //       fetchTranscription(file_name);
    //     } catch (error) {
    //       console.error('Error uploading file:', error);
    //     }
    // };

    const sendAudioToServer = async (uri) => {
        try {
            const response = await fetch(uri);
            const blob = await response.blob();
            const timestamp = new Date().getTime();
            const file_name = `${transcriptionLanguage}/${timestamp}-audio-file.flac`;
          
            const storageRef = ref(storage, `transcriptions/${file_name}`);
            await uploadBytes(storageRef, blob);

            fetchTranscription(file_name, transcriptionLanguage);
            // fetchTranscription2(file_name, transcriptionLanguage);
    
            // const functionUrl = `https://us-central1-medilingo-418907.cloudfunctions.net/transcribeAudio?filePath=transcriptions/${file_name}&languageCode=${transcriptionLanguage}`;
            // console.log('Fetching transcription from', functionUrl);
            // const transcriptionResponse = await fetch(functionUrl);
            // if (!transcriptionResponse.ok) {
            //     throw new Error('Failed to fetch transcription');
            // }
            // console.log('Transcription response:', transcriptionResponse);
            // const transcriptionData = await transcriptionResponse.json();
            // console.log(transcriptionData);
    
            // setTranscript(transcriptionData.transcription);
    
        } catch (error) {
            console.error('Error uploading file or fetching transcription:', error);
        }
    };

    const fetchTranscription2 = async (fileName, transcriptionLanguage) => { 
        const functionUrl = `https://us-central1-medilingo-418907.cloudfunctions.net/transcribeAudio?filePath=transcriptions/${fileName}&languageCode=${transcriptionLanguage}`;
        console.log('Fetching transcription from', functionUrl);
        const transcriptionResponse = await fetch(functionUrl);
        if (!transcriptionResponse.ok) {
            throw new Error('Failed to fetch transcription');
        }
        const transcriptionData = await transcriptionResponse.json();
        console.log(transcriptionData);
        setBottomInputText(transcriptionData.transcription);
    };


    const fetchTranscription = async (fileName, transcriptionLanguage) => {
        const txtFileRef = ref(storage, `transcriptions/${transcriptionLanguage}/transcriptions/${fileName}.wav_transcription.txt`);
        console.log(txtFileRef);
        let attemptCount = 0;
        const maxAttempts = 12;

        let loadingDots = '.';
        setTopInputText(loadingDots);
        setBottomInputText(loadingDots);

        const loadingInterval = setInterval(() => {
            loadingDots = loadingDots.length < 3 ? loadingDots + '.' : '.';
            setTopInputText(loadingDots)
            setBottomInputText(loadingDots);
        }, 700);
    
        const checkTranscriptionAvailable = async () => {
            attemptCount++;
            if (attemptCount > maxAttempts) {
                console.log('Maximum attempts reached. Stopping check.');
                clearInterval(checkInterval);
                transcriptionLanguage === 'uk-UA' ? setTopInputText('No transcription available') : setBottomInputText('Transkribering ikke tilgængelig');
                clearInterval(loadingInterval); 
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
                        handleSubmitPatient(transcript);
                    }
                    else { 
                        setBottomInputText(transcript);
                        handleSubmitDoctor(transcript);
                    }
                    clearInterval(checkInterval);
                    deleteTranscriptionFile(txtFileRef);
                    const audioFile = ref(storage, `transcriptions/${fileName}`);
                    deleteTranscriptionFile(audioFile)

                } else {
                    console.log('Transcription file found but no results.');
                    transcriptionLanguage === 'uk-UA' ? setTopInputText('No transcription available') : setBottomInputText('Transkribering ikke tilgængelig');
                    clearInterval(checkInterval);
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
                    // editable={false} 
                />
            </TopContainer>

            {(topInputText || bottomInputText) && (
                <DeleteButton onPress={deleteText}>
                    <ActionButtonIcon name={"close"} />
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
                <View style={{ marginBottom: 10 }}></View>
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