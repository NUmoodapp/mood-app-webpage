import './App.css';
import React, { useState, useEffect } from "react";
import Form from "./Form";
import LoadingIcons from 'react-loading-icons';
import Speech from "./Speech";
import { getSpotifyTokenOrRefresh } from './token_util';
import styles from './App.css';

function App(props) {
    const [statement, setStatement] = useState('');
    const [token, setToken] = useState(null);
    const [toggleHome, setToggleHome] = useState(true);
    const [toggleChat, setToggleChat] = useState(false);
    const [song, setSong] = useState(null);
    const [speaking, setSpeaking] = useState(false);
    let currentFont = 0;

    function makeBigger(){
        if(currentFont <0.6)
            currentFont += 0.2;
            setFont();
    };
     
    function makeSmaller(){
        if(currentFont >0.2)
            currentFont -= 0.2;
            setFont();
    };
     
    function setFont() {
        document.querySelector('h1').style.fontSize = `${2+currentFont}em`;
        document.querySelector('h3').style.fontSize = `${1.17+currentFont}em`;
        var list = document.querySelectorAll('p');
        for (var x = 0; x < list.length; x++)
            list[x].style.fontSize = `${1+currentFont}em`;
    }
    
    
    function addStatement(newStatement) {
        setStatement(newStatement);
        {
            // When we get a statement, call api.py with the statement and set the returned with setSong
        }
        console.log(JSON.stringify({ 'statement': newStatement , 'token': token}));
        fetch('/song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'statement': newStatement , 'token': token})
        })
            .then(res => res.json())
            .then(data => {
                setSong(data.song);
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function findSong() {
        console.log(statement)
        
    }

    function nowSpeaking(x){
        setSpeaking(x);
    }

    function goToAbout(e) {
        setToggleHome(false);
        e.preventDefault();
        setToggleChat(false);
    }

    function goHome(e) {
        setToggleHome(true);
        setStatement('');
        setSpeaking(false);
        setSong(null);
        e.preventDefault();
        setToggleChat(false);
    }

    function goChat(e) {
        setToggleChat(true);

        getSpotifyTokenOrRefresh()
            .then((response) => {
                setToken(response.authToken)
            })
            .catch(error => {
                console.log("error: no spotify token found: ",error);
            });
    }


    return (
        <div>
            <nav>
                {/* <select id="theme" onChange={this.change} value={this.state.value}>
                    <option value = 'defaultTheme'>Default</option>
                    <option value = 'desertTheme'>Desert</option>
                    <option value = 'oceanTheme'>Ocean</option>
                    <option value = 'highContrastTheme'>High Contrast</option>
                </select> */}
                <button onClick={goHome} className="logo"><img src={require('./moodapplogo.png')} alt="Mood app logo"/></button>
                <button onClick={makeBigger} className="a1" title="Make font bigger">A</button>
                <button onClick={makeSmaller} className="a2" title="Make font smaller">A</button>
                <button onClick={goToAbout} >About Mood</button>
            </nav>
            <main>
            {toggleHome && !toggleChat && <div>
                <h1 >Welcome to</h1>
                <h1 style={{ margin: "0", fontSize: "75pt" }}><img src={require('./moodlogo.png')} alt="Mood logo" /></h1>
                <h3>Finding the perfect song to suit your Mood.</h3>
                <p>Simply chat with Mood about your day!</p>
                <button onClick={goChat}>Let's Chat!</button>
                <br />
            </div>}

            {toggleChat && statement ==='' && <div class="chat">
                <p class = "instructions">Hi, what's up!</p>  
            </div>}

            {toggleChat && statement === '' && <div class="chat chat-input">
                <Speech addStatement={addStatement} nowSpeaking={nowSpeaking} />
                {// Speech.js handles all the speech to text!
                }
                {!speaking && 
                    <Form class="input-large" addStatement={addStatement} />
                }
                <br />      
            </div>}

            {statement !== '' && song == null && <div class="chat no-input">
                <p class = "instructions">Hi, what's up!</p>
                <p class = "statement">{statement}</p>
                <p class = "response">Finding the perfect song to match your mood...</p>
                <p class="center"><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1} /></p>
                <p class="center"><button onClick={goHome} >Go Back</button></p>
            </div>}
            {
                // above will show while song is loading
                // below will show when song is found (we can replace the embed url with the one we find)
            }
            {statement !== '' && song != null && <div class="chat no-input">
                <p class="instructions">Hi, what's up!</p>
                <p class="statement">{statement}</p>
                <p class="response">Finding the perfect song to match your mood...</p>
                <p class= "response">Here's the perfect song for you:</p>
                <div class="response">
                    <iframe title="Youtube Link" src={song[1]} frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                </div>
                <p class="center"><button onClick={goHome} >Go Back</button></p>
                </div>}
            </main>

            {
                // about page
            }
            {!toggleHome && <main class="about">
                <h1>About Mood</h1>
                <h3>Finding the perfect song to suit your Mood.</h3>
                <p>When you tell Mood how you're feeling, the app analyzes your statement to determine key factors about your emotional context.</p>
                <p>Using Spotify's Developer Toolkit, Mood searches thousands of songs and finds the top match based on those factors.</p>
                <p>Interested in learning more or joining the team? Reach out to tani@u.northwestern.edu.</p>
            </main>}


        </div>
    );
}

export default App;
