import { View } from 'react-native';
import React, { useState, useEffect } from 'react';
import { ActionButton, ActionButtonIcon, TranslateInput, TranslateScreenContainer, ButtonContainer } from "./translate.styles";
import * as Speech from 'expo-speech';

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

    useEffect(() => {
        setTopInputText(bottomInputText);
    }, [bottomInputText]);

    const speakTopInputText = () => {
        Speech.speak(topInputText);
    };

    return (
        <TranslateScreenContainer>
            
            <ButtonContainer>
                <ActionButton>
                    <ActionButtonIcon name="volume-high" reverse={true}/>
                </ActionButton>
                <ActionButton>
                    <ActionButtonIcon name="mic" reverse={true}/>
                </ActionButton>
            </ButtonContainer>

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

            <ButtonContainer>
                <ActionButton onPress={speakTopInputText}>
                    <ActionButtonIcon name="volume-high" />
                </ActionButton>
                <ActionButton onPress={speakTopInputText}>
                    <ActionButtonIcon name="mic" />
                </ActionButton>
            </ButtonContainer>

        </TranslateScreenContainer>
    );
};



// import React, { useState, useEffect } from 'react';
// import { View } from 'react-native';
// import { initWhisper, AudioSessionIos } from 'whisper.rn';
// import { ActionButton, ActionButtonIcon, TranslateInput, TranslateScreenContainer } from "./translate.styles";

// export const TranslateScreen = () => {
//     const [bottomInputText, setBottomInputText] = useState('');
//     const [topInputText, setTopInputText] = useState('');
//     const [whisperContext, setWhisperContext] = useState(null);
//     const [isRecording, setIsRecording] = useState(false);
//     const [transcription, setTranscription] = useState('');

//     useEffect(() => {
//         const setupWhisper = async () => {
//             const context = await initWhisper({
//                 filePath: 'file://.../ggml-tiny.en.bin',
//             });
//             setWhisperContext(context);
//         };

//         setupWhisper();
//     }, []);

//     const handleTopInputChange = (text) => {
//         setTopInputText(text);
//     };

//     const handleBottomInputChange = (text) => {
//         setBottomInputText(text);
//     };

//     useEffect(() => {
//         setBottomInputText(topInputText);
//     }, [topInputText]);

//     useEffect(() => {
//         setTopInputText(bottomInputText);
//     }, [bottomInputText]);

//     const handleRecordPress = async () => {
//         if (!whisperContext) return;

//         if (!isRecording) {
//             // Start recording
//             const { stop, subscribe } = await whisperContext.transcribeRealtime({
//                 audioSessionOnStartIos: {
//                     category: AudioSessionIos.Category.PlayAndRecord,
//                     options: [AudioSessionIos.CategoryOption.MixWithOthers],
//                     mode: AudioSessionIos.Mode.Default,
//                 },
//                 audioSessionOnStopIos: 'restore',
//             });

//             subscribe(evt => {
//                 if (!evt.isCapturing) {
//                     console.log('Finished realtime transcribing');
//                     setIsRecording(false);
//                 } else {
//                     // Update transcription text in real-time (optional)
//                     const { data } = evt;
//                     setTranscription(data.result);
//                 }
//             });

//             // Store the stop function to manage recording state
//             setIsRecording({ stop });
//         } else {
//             // Stop recording
//             isRecording.stop();
//             setIsRecording(false);
//         }
//     };

//     useEffect(() => {
//         if (transcription) {
//             // Update the bottom input text with the latest transcription
//             handleBottomInputChange(transcription);
//         }
//     }, [transcription]);

//     return (
//         <TranslateScreenContainer>
//             <ActionButton onPress={() => {}} >
//                 <ActionButtonIcon name="chatbox-ellipses" reverse={true}/>
//             </ActionButton>
//             <View style={{ marginBottom: 10 }}></View>
//             <TranslateInput 
//                 reverse={true} 
//                 value={topInputText} 
//                 onChangeText={handleTopInputChange}
//             />
//             <View style={{ marginBottom: 10 }}></View>
//             <TranslateInput 
//                 onChangeText={handleBottomInputChange} 
//                 value={bottomInputText}
//             />
//             <View style={{ marginBottom: 10 }}></View>
//             <ActionButton onPress={handleRecordPress}>
//                 <ActionButtonIcon name="chatbox-ellipses" /> 
//             </ActionButton>
//         </TranslateScreenContainer>
//     );
// };
