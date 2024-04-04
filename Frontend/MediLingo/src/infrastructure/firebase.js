import { initializeApp } from 'firebase/app';
import { getStorage, ref, getDownloadURL } from 'firebase/storage';

let apiKey = null;

const firebaseConfig = {
  apiKey: "AIzaSyDFReeWUmGdaM2knL_Y59zHiS-k4kv3J9g",
  authDomain: "medilingo-418907.firebaseapp.com",
  projectId: "medilingo-418907",
  storageBucket: "medilingo-418907.appspot.com",
  messagingSenderId: "78184223325",
  appId: "1:78184223325:web:442c8d460acb94c46573b4"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

async function fetchApiKey() {
  try {
    const fileRef = ref(storage, 'api_key.txt');
    const url = await getDownloadURL(fileRef);
    const response = await fetch(url);
    const key = await response.text();
    
    return key;
  } catch (error) {
    console.error('Failed to fetch API key:', error);
    throw new Error('Failed to fetch API key');
  }
}

export { app, storage, fetchApiKey };