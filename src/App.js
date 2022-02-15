import './App.css';
import React, { useState, useEffect } from "react";
import Form from "./Form";
import LoadingIcons from 'react-loading-icons';
import Speech from "./Speech";


function App(props) {
    const [statement, setStatement] = useState('');
    const [toggleHome, setToggleHome] = useState(true);
    const [toggleChat, setToggleChat] = useState(false);
    const [song, setSong] = useState(null);
    const [speaking, setSpeaking] = useState(false);

    function addStatement(newStatement) {
        setStatement(newStatement);
        {
            // When we get a statement, call api.py with the statement and set the returned with setSong
        }
        console.log(JSON.stringify({ 'statement': newStatement }));
        fetch('/song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'statement': newStatement })
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
    }


    return (
        <div>
            <nav>
                <button onClick={goHome} className="logo"><img src={require('./moodapplogo.png')} alt="Mood app logo"/></button>
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

            {toggleChat && <div>
                
                <p class = "instructions">Hi, what's up!</p>
                <br />      
            </div>}

            {statement === '' && toggleChat && <div>
                <Speech addStatement={addStatement} nowSpeaking={nowSpeaking} />
                {// Speech.js handles all the speech to text!
                }
                {!speaking && 
                    <Form addStatement={addStatement} />
                }
                <br />      
            </div>}

            {statement !== '' && <div>
                    <br />
                    <p class = "statement">"{statement}"</p>
            </div>
            }

            {statement !== '' && song == null && <div>
                <p class = "response">Finding the perfect song to match your mood...</p>
                <p><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1} /></p>
                <button onClick={goHome} >Go Back</button>
            </div>}
                {
                    // above will show while song is loading
                    // below will show when song is found (we can replace the embed url with the one we find)
                }
                {statement !== '' && song != null && <div>
                    <p>Here's the perfect song for you:</p>
                    <p>{song[0]} </p>
                    <iframe title="Youtube Link" src={song[1]} width="100%" height="380" frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                    <button onClick={goHome} >Go Back</button>
                </div>}
            </main>

            {
                // about page
            }
            {!toggleHome && <main>
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
