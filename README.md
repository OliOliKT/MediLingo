**GitHub repository**

We have a **main** repository. This is where the final app is placed. You should not touch this repository or merge any changes to it. Then we have a **development** repository. This is the branch you create a new branch from. When you have pushed your changes to your own branch you then merge your branch with this one.

 - **Create new branch:** Go to GitHub repository > Click on branch name > Click "View all branches" > Click "New branch".
 - **Create local Git repository:** Create folder on computer > Navigate to folder in repository > Type "git init"
 - **Clone from specific branch:** In your newly initialized folder you can add folders for each branch. Create a folder with your branch name, navigate to it in the terminal, and use the following command to clone the repository inside this folder: *git clone -b <your_branch_name> https://github.com/OliOliKT/MediLingo.git*
 - Now you can open the new cloned repository branch in Visual Studio Code and make your code changes.
 - When you are done you can use the following commands: *git commit -m "message"* and *git push* to add it to the remote repository. However, it would be preferred if you used the integrated Git interface in Visual Studio Code, where you can click *"Commit"* and then *"Sync changes"*.
 - When the changes are pushed to your remote repository, GitHub will prompt you to make a pull request. You should do this, and set it so you merge your branch with the development branch - NOT the main branch.

**Useful Git commands**
 - **git branch -vv:** See which remote branches your local branches are connected to.
 - **git remote -v:** Show remote repositories.
 - **git branch --set-upstream-to=origin/remote_branch_name local_branch_name:** Change your remote branch (the GitHub branch you push to)


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

*Create new React Native app:*
 - Open folder in Visual Studio Code > Open a terminal
 - Install node.js: install node // node -v
 - Install Node Packet Manager: install npm // npm -v
 - Install Expo: npm install -g expo-cli
 - Create Expo app called "hello-world": expo init hello-world
 - Choose template, blank or tabs
 - Move into "hello-world" app folder: cd hello-world
 - From here, you can begin using commands as seen below.
 - In order to set up testing properly, create a .watchmanconfig file in the root folder of the app project, that contains the following:
   <img width="211" alt="image" src="https://github.com/OliOliKT/MediLingo/assets/61165499/d4a146ed-382c-4595-bd4c-e9264ee9144e">


