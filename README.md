**GitHub repository**

We have a **main** repository. This is where the final app is placed. Then we have a **development** repository. This is the branch you create a new branch from and push to when you are done.

 - **Create new branch:** Go to GitHub repository > Click on branch name > Click "View all branches" > Click "New branch".
 - **Create local Git repository:** Create folder on computer > Navigate to folder in repository > Type "git init"
 - **Clone from specific branch:** In your newly initialized folder you can add folders for each branch. Create a folder with your branch name, navigate to it in the terminal, and use the following command to clone the repository inside this folder: *git clone -b <your_branch_name> https://github.com/OliOliKT/MediLingo.git*
 - Now you can open the new branch in Visual Studio Code and make your changes in the code. When you are done you can use the following commands: *git commit -m "message"* and *git push* to add it to the remote repository

**Backend**

Backend consists of 4 folders:
 - **Maja:** In this folder Maja will push files
 - **Oliver:** In this folder Oliver will push files
 - **Simon:** In this folder Simon will push files
 - **Common:** In this folder we will agree on which files are to be used for the final product

**Frontend**

Frontend has a folder with the app name: MediLingo. Move into "MediLingo" app folder with **cd Frontend/MediLingo**. Then you should execute the command **npm install** before you can run the app. Then you can execute app-specific commands in the terminal. The most useful being **npm start** which starts the app:
 - **react-native doctor:** Check and diagnose issues in your React Native development setup.
 - **npx react-native run-android:**	Build and run your app on an Android emulator or device.
 - **npx react-native run-ios:**	Build and run your app on an iOS simulator or device.
 - **npm start:**	Start the Metro Bundler for packaging and serving your code.
 - **npm test:**	Run tests for your React Native project using Jest.
 - **react-native log-android:**	Display Android app logs for troubleshooting.
 - **react-native log-ios:**	Display iOS app logs for troubleshooting.
 - **npm run android-clean:**	Clean build artifacts for the Android app.
 - **npm run ios-clean:**	Clean build artifacts for the iOS app.
 - **npm run start -- --reset-cache:**	Reset the Metro Bundler's cache.
 - **npx react-native info:**	Display information about your React Native environment.
 - **ctrl + c:**	Stop server from runnning
