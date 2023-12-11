## Contents

The contents folder includes the code for embedding the Generate Summary button into Course lecture video pages. Due to Chrome security guidelines, content scripts such as this cannot make API calls, therefore the API call to retrieve the summary is made in our background script which sends it back to the content script as a message. The course name and video name are retrieved directly from the page's URL.

## Tabs

The tabs folder contains the code for the secondary popup windows present in our extension. These include the Chatbox popup in which you can ask questions about lecture content, the sign up popup window for creating an account, as well as the popup window that displays summaries for specific files, selectable from the "View Uploaded Files" button in the main extension popup. Plasmo automatically converts the Typescript files into readable HTML.

## Utils

The utils folder contains the helper functions that are used to retrive/upload information from our backend. These are used for signing in/signing up, retrieving answers to user's questions in the Chatbox feature, uploading new files for other courses, and retrieving a summary for a video or power point.

## background.ts

This is our background script. It is only necessary to help our content script with communicating with our backend. It receives a message, telling it what to do, then sends a response back to the message sender.

## fileview.tsx

This file includes the code for displaying uploaded files. It retrieves a list of all transcripts and PDF's and displays them in a list. These items can be clicked to display their summaries in a new pop up window.

## popup.tsx

This is our extension main popup that you see when clicking the extensions icon in Chrome. It includes a login page, as well as the home view, which allows for uploading a new file, viewing already uploaded files, and opening the ChatBot feature.

## uploadfile.tsx

This includes the code for the file uploading menu. It allows you to select and submit a file to be uploaded into our database.












MORE CLEAR INSTRUCTIONS INCLUDED AT BOTTOM

This is a [Plasmo extension](https://docs.plasmo.com/) project bootstrapped with [`plasmo init`](https://www.npmjs.com/package/plasmo).

## Getting Started

First, run the development server:

```bash
pnpm dev
# or
npm run dev
```

Open your browser and load the appropriate development build. For example, if you are developing for the chrome browser, using manifest v3, use: `build/chrome-mv3-dev`.

You can start editing the popup by modifying `popup.tsx`. It should auto-update as you make changes. To add an options page, simply add a `options.tsx` file to the root of the project, with a react component default exported. Likewise to add a content page, add a `content.ts` file to the root of the project, importing some module and do some logic, then reload the extension on your browser.

For further guidance, [visit our Documentation](https://docs.plasmo.com/)

## Making production build

Run the following:

```bash
pnpm build
# or
npm run build
```

This should create a production bundle for your extension, ready to be zipped and published to the stores.

## Submit to the webstores

The easiest way to deploy your Plasmo extension is to use the built-in [bpp](https://bpp.browser.market) GitHub action. Prior to using this action however, make sure to build your extension and upload the first version to the store to establish the basic credentials. Then, simply follow [this setup instruction](https://docs.plasmo.com/framework/workflows/submit) and you should be on your way for automated submission!



For testing: If you want to run the extension on chrome, navigate to:
```
./src/frontend/extension
```
From here, run 
```
npm install plasmo
```
then,

```
npm run dev
```
This will create a build folder insie of this directory which contains
```
chrome-mv3-dev
```
Then, to load the extension, navigate to Chrome's manage extension menu and click Load Unpacked, selecting the 
```
chrome-mv3-dev
```
folder

All these commands should be ran while in the "extension" folder. A 
```
npm install
```
may be necessary in this folder as well.
