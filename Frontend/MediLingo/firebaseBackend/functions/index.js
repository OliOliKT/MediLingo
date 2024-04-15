const functions = require('firebase-functions');
const admin = require('firebase-admin');
const speech = require('@google-cloud/speech');
const { Storage } = require('@google-cloud/storage');

admin.initializeApp();
const storage = new Storage();
const client = new speech.SpeechClient();

exports.transcribeAudio = functions.https.onRequest(async (req, res) => {
  const filePath = req.query.filePath;
  const languageCode = req.query.languageCode;

  if (!filePath || !languageCode) {
    return res.status(400).send('Missing filePath or languageCode');
  }
  console.log(`Transcribing audio file: ${filePath}`);
  console.log(`Language code: ${languageCode}`);

  try {
    const audio = {
      uri: `gs://medilingo-418907.appspot.com/${filePath}`,
    };
    const config = {
      encoding: 'FLAC',
      sampleRateHertz: 48000,
      languageCode: languageCode,
    };
    const request = {
      audio: audio,
      config: config,
    };

    // Asynchronously performs speech recognition
    const [operation] = await client.longRunningRecognize(request);
    const [response] = await operation.promise();
    console.log('Transcription complete:', response);
    const transcription = response.results
      .map(result => result.alternatives[0].transcript)
      .join('\n');

    res.send({ transcription: transcription });
  } catch (error) {
    console.error('Error transcribing file:', error);
    res.status(500).send(error.toString());
  }
});
