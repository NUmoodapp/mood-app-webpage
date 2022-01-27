import React, { Component } from 'react';
import { getTokenOrRefresh } from './token_util';
import LoadingIcons from 'react-loading-icons';
import './custom.css'
import { ResultReason } from 'microsoft-cognitiveservices-speech-sdk';

const speechsdk = require('microsoft-cognitiveservices-speech-sdk')

// Credit to AzureSpeechReactSimple on github for this

export default class Speech extends Component {
    constructor(props) {
        super(props);

        this.state = {
            displayText: '',
            gotStatement: false,
            clicked: false,
        }
    }
    
    async componentDidMount() {
        // check for valid speech key/region
        const tokenRes = await getTokenOrRefresh();
        if (tokenRes.authToken === null) {
            this.setState({
                displayText: 'FATAL_ERROR: ' + tokenRes.error
            });
        }
    }

    async sttFromMic() {
        const tokenObj = await getTokenOrRefresh();
        const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(tokenObj.authToken, tokenObj.region);
        speechConfig.speechRecognitionLanguage = 'en-US';
        
        const audioConfig = speechsdk.AudioConfig.fromDefaultMicrophoneInput();
        const recognizer = new speechsdk.SpeechRecognizer(speechConfig, audioConfig);

        this.setState({
            displayText: 'Mood is listening...',
            clicked: true,
        });

        recognizer.recognizeOnceAsync(result => {
            let displayText;
            if (result.reason === ResultReason.RecognizedSpeech) {
                displayText = `Mood got: ${result.text}`
                this.setState({
                    gotStatement: true
                });
                this.props.addStatement(result.text);
            } else {
                displayText = 'ERROR: Speech was cancelled or could not be recognized. Ensure your microphone is working properly.';
            }

            this.setState({
                displayText: displayText
            });
        });
    }

    render() {
        return (
            <div className="app-container">

                {!this.state.clicked && <h1><i className="fas fa-microphone fa-lg mr-2" onClick={() => this.sttFromMic()}></i></h1>}
                
                {!this.state.gotStatement && this.state.clicked &&
                    <p><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1} /></p>}

                <div >
                    <p>{this.state.displayText}</p>
                </div>
            </div>
        );
    }
}