import './App.css';
import React, { useState, useEffect } from "react";
import Form from "./Form";
import LoadingIcons from 'react-loading-icons';
import Speech from "./Speech";
import { getSpotifyTokenOrRefresh } from './token_util';
import styles from './App.css';

let currentFont = 0;
let pfont = 1;
let h1font = 2;
let h3font = 1.17;
let fontcolor = 'black';

function App(props) {
    const [statement, setStatement] = useState('');
    const [token, setToken] = useState(null);
    const [toggleHome, setToggleHome] = useState(true);
    const [toggleMode, setToggleMode] = useState(true);
    const [toggleChat, setToggleChat] = useState(false);
    const [song, setSong] = useState(null);
    const [speaking, setSpeaking] = useState(false);
    


    function makeBigger(){
        if(currentFont <0.6)
        {
            currentFont += 0.2;
            pfont += 0.2;
            h1font += 0.2;
            h3font += 0.2;
            setFont();
        }
    };
     
    function makeSmaller(){
        if(currentFont >=0.2)
        {
            currentFont -= 0.2;
            pfont -= 0.2;
            h1font -=0.2;
            h3font -= 0.2;
            setFont();
        }
    };
     
    function setFont() {
        if (toggleChat && statement ==='')
        {
            document.getElementById('Instructions').style.fontSize = pfont + 'em';
        }
        else if (statement !== '' && song == null)
        {
            document.getElementById('Instructions_err').style.fontSize = pfont + 'em';
            document.getElementById('Statement_err').style.fontSize = pfont+ 'em';
            document.getElementById('Response_err').style.fontSize = pfont + 'em';
        }
        else if (statement !== '' && song != null)
        {

            document.getElementById('Instructions_Fin').style.fontSize = pfont + 'em';
            document.getElementById('Statement_Fin').style.fontSize = pfont + 'em';
            document.getElementById('Response_Fin').style.fontSize = pfont+ 'em';
            document.getElementById('Result_Fin').style.fontSize = pfont + 'em';
            
        }
        else
        {
            document.querySelector('h1').style.fontSize = `${h1font}em`;
            document.querySelector('h3').style.fontSize = `${h3font}em`;
            var list = document.querySelectorAll('p');
            for (var x = 0; x < list.length; x++)
                list[x].style.fontSize = `${pfont}em`;
        }
    }

    function DarkMode(){
        if(toggleMode)
        {
            if (toggleChat && statement ==='')
            {
                document.querySelector('body').style.backgroundColor = '#152028';
            }
            else if (statement !== '' && song == null)
            {
                document.querySelector('body').style.backgroundColor = '#152028';
            }
            else if (statement !== '' && song != null)
            {
                document.querySelector('body').style.backgroundColor = '#152028';
            }
            else 
            {
                
                document.querySelector('h1').style.color = `white`;
                document.querySelector('h3').style.color = `white`;
                var list = document.querySelectorAll('p');
                for (var x = 0; x < list.length; x++)
                    list[x].style.color = `white`;
                document.querySelector('body').style.backgroundColor = '#152028';
            }
            fontcolor = 'white';
            setToggleMode(false);
            
        }
        else
        {
            if (toggleChat && statement ==='')
            {
                document.querySelector('body').style.backgroundColor = 'white';
            }
            else if (statement !== '' && song == null)
            {
                document.querySelector('body').style.backgroundColor = 'white';
            }
            else if (statement !== '' && song != null)
            {
                document.querySelector('body').style.backgroundColor = 'white';
            }
            else 
            {
                document.querySelector('h1').style.color = `black`;
                document.querySelector('h3').style.color = `black`;
                var list = document.querySelectorAll('p');
                for (var x = 0; x < list.length; x++)
                    list[x].style.color = `black`;
                document.querySelector('body').style.backgroundColor = 'white';
            }
            fontcolor = 'black';
            setToggleMode(true);
        }
        

    };
    
    
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
                <button onClick={DarkMode} className="dark" title="Dark Mode">Dark Mode</button>
                <button onClick={makeBigger} className="a1" title="Make font bigger">A</button>
                <button onClick={makeSmaller} className="a2" title="Make font smaller">A</button>
                <button onClick={goToAbout} >About Mood</button>
            </nav>
            <main>
            {toggleHome && !toggleChat && <div>
                <h1 id = 'welcome' style={{fontSize: h1font +"em", color: fontcolor}}>Welcome to</h1>
                <h1 id = 'logo' style={{ margin: "0", fontSize: "75pt" }}><img src={toggleMode ? require('./moodlogo.png') : require('./Moodlogowhite.png')} alt="Mood logo" /></h1>
                <h3 id = 'intro' style={{fontSize: h3font +"em", color: fontcolor}}>Finding the perfect song to suit your Mood.</h3>
                <p id = 'instruct' style={{fontSize: pfont +"em", color: fontcolor}}>Simply chat with Mood about your day!</p>
                <button onClick={goChat}>Let's Chat!</button>
                <br />
            </div>}

            {toggleChat && statement ==='' && <div class="chat">
                <p style={{fontSize: pfont +"em"}} id = "Instructions" class = "instructions">Hi, what's up!</p>  
                
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
                <p style={{fontSize: pfont +"em"}} id = "Instructions_err" class = "instructions">Hi, what's up!</p>
                <p style={{fontSize: pfont +"em"}} id = "Statement_err" class = "statement">{statement}</p>
                <p style={{fontSize: pfont +"em"}} id = "Response_err" class = "response">Finding the perfect song to match your mood...</p>
                <p class="center"><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1} /></p>
                <p class="center"><button onClick={goHome} >Go Back</button></p>
            </div>}
            {
                // above will show while song is loading
                // below will show when song is found (we can replace the embed url with the one we find)
            }
            {statement !== '' && song != null && <div class="chat no-input">
                <p style={{fontSize: pfont +"em"}} id = "Instructions_Fin" class="instructions">Hi, what's up!</p>
                <p style={{fontSize: pfont +"em"}} id = "Statement_Fin" class="statement">{statement}</p>
                <p style={{fontSize: pfont +"em"}} id = "Response_Fin" class="response">Finding the perfect song to match your mood...</p>
                <p style={{fontSize: pfont +"em"}} id = "Result_Fin" class= "response">Here's the perfect song for you:</p>
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
                <h1 style={{fontSize: h1font +"em", color: fontcolor}}>About Mood</h1>
                <h3 style={{fontSize: h3font +"em", color: fontcolor}}>Finding the perfect song to suit your Mood.</h3>
                <p style={{fontSize: pfont +"em", color: fontcolor}}>When you tell Mood how you're feeling, the app analyzes your statement to determine key factors about your emotional context.</p>
                <p style={{fontSize: pfont +"em", color: fontcolor}}>Using Spotify's Developer Toolkit, Mood searches thousands of songs and finds the top match based on those factors.</p>
                <p style={{fontSize: pfont +"em", color: fontcolor}}>Interested in learning more or joining the team? Reach out to tani@u.northwestern.edu.</p>
            </main>}


        </div>
    );
}

export default App;
