import './App.css';
import React, { useState } from "react";
import Form from "./Form";
import LoadingIcons from 'react-loading-icons'

function App(props) {
    const [statement, setStatement] = useState('');
    const [toggleHome, setToggleHome] = useState(true);
    const [toggleVoice, setToggleVoice] = useState(false); 
    const [song, setSong] = useState(null);

    function addStatement(newStatement) {
        setStatement(newStatement);
    }

    function goToAbout(e) {
        setToggleHome(false);
        setToggleVoice(false);
        e.preventDefault();
    }

    function goHome(e) {
        setToggleHome(true);
        setToggleVoice(false);
        setStatement('');
        e.preventDefault();
    }

    function goVoice(e) {
        setToggleVoice(true);
        setToggleHome(false);
        e.preventDefault();
        // is there where i would implement the listening function?
        // currently just working to understand everything before trying
        // to implement anything
        
        {// Voice state option
        }
    }

    return (
        <div>
            <nav>
                <a onClick={goHome} href='' className="logo"><img src={require('./moodapplogo.png')} alt="Mood app logo"/></a>
                <a onClick={goToAbout} href=''>About Mood</a>
            </nav>

            {toggleHome && statement == '' && <main>
                <h1 >Welcome to</h1>
                <h1 style={{margin:"0", fontSize:"75pt"}}><img src={require('./moodlogo.png')} alt="Mood logo" /></h1>
                <h3>Finding the perfect song to suit your Mood.</h3>
                
                <p>To get started, click to type or press the button to speak how you're feeling.</p>

                <Form addStatement={addStatement} />

                <p><button onClick={goVoice} href=''>Use Voice</button></p>
                {// Click to access the voice option
                }
            </main>}
            
            {toggleVoice && !toggleHome && <main>
                <h3>Mood is listening...</h3>
                <p><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1}/></p>
                <a onClick={goHome} href=''>Go back</a> 
                {//transition to Mood Got
                }
            </main>}

            {toggleHome && statement !== '' && song == null && <main>
                <h3>Mood got... </h3>
                <p>"{statement}"</p>
                <p>Finding the perfect song to match your mood...</p>
                <p><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1}/></p>
                <a onClick={goHome} href=''>Go back</a>
            </main>}
            {
                // above will show while song is loading
                // below will show when song is found (we can replace the embed url with the one we find)
            }
            {toggleHome && statement !== '' && song != null && <main>
                <h3>Mood got... </h3>
                <p>"{statement}"</p>
                <p>Here's the perfect song for you:</p>
                <iframe src="https://open.spotify.com/embed/track/3n69hLUdIsSa1WlRmjMZlW?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            </main>}

            {
                // about page
            }
            {!toggleHome && !toggleVoice && <main>
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