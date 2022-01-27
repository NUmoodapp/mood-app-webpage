import './App.css';
import React, { useState } from "react";
import Form from "./Form";
import LoadingIcons from 'react-loading-icons';
import Speech from "./Speech";


function App(props) {
    const [statement, setStatement] = useState('');
    const [toggleHome, setToggleHome] = useState(true);
    const [song, setSong] = useState(null);

    function addStatement(newStatement) {
        setStatement(newStatement);
    }

    function goToAbout(e) {
        setToggleHome(false);
        e.preventDefault();
    }

    function goHome(e) {
        setToggleHome(true);
        setStatement('');
        e.preventDefault();
    }


    return (
        <div>
            <nav>
                <button onClick={goHome} className="logo"><img src={require('./moodapplogo.png').default} alt="Mood app logo"/></button>
                <button onClick={goToAbout} >About Mood</button>
            </nav>
            {toggleHome && <main>
                <h1 >Welcome to</h1>
                <h1 style={{ margin: "0", fontSize: "75pt" }}><img src={require('./moodlogo.png').default} alt="Mood logo" /></h1>
                <h3>Finding the perfect song to suit your Mood.</h3>

                {statement === '' && <div>
                    <p>To get started, click to type or press the button to speak how you're feeling.</p>

                    <Form addStatement={addStatement} />
                    <br />
                    <Speech addStatement={addStatement} />
                    {// Speech.js handles all the speech to text!
                    }
                </div>}

                {statement !== '' && <div>
                    <br />
                    <h3>Mood got... </h3>
                    <p>"{statement}"</p>
                </div>
                }

                {statement !== '' && song == null && <div>
                    <p>Finding the perfect song to match your mood...</p>
                    <p><LoadingIcons.BallTriangle stroke="#555" strokeOpacity={1} /></p>
                    <button onClick={goHome} >Go Back</button>
                </div>}
                {
                    // above will show while song is loading
                    // below will show when song is found (we can replace the embed url with the one we find)
                }
                {statement !== '' && song != null && <div>
                    <p>Here's the perfect song for you:</p>
                    <iframe title="Spotify Link" src="https://open.spotify.com/embed/track/3n69hLUdIsSa1WlRmjMZlW?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                </div>}
            </main>}

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