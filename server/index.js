require('dotenv').config();
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const pino = require('express-pino-logger')();
const qs = require('qs');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(pino);

const cors = require('cors');
const corsOptions = {
    origin: 'http://localhost:3000',
    credentials: true,            //access-control-allow-credentials:true
    optionSuccessStatus: 200
}
app.use(cors(corsOptions));

app.get('/api/get-speech-token', async (req, res, next) => {
    res.setHeader('Content-Type', 'application/json');
    const speechKey = process.env.SPEECH_KEY;
    const speechRegion = process.env.SPEECH_REGION;

    if (speechKey === 'paste-your-speech-key-here' || speechRegion === 'paste-your-speech-region-here') {
        res.status(400).send('You forgot to add your speech key or region to the .env file.');
    } else {
        const headers = { 
            headers: {
                'Ocp-Apim-Subscription-Key': speechKey,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        };

        try {
            const tokenResponse = await axios.post(`https://${speechRegion}.api.cognitive.microsoft.com/sts/v1.0/issueToken`, null, headers);
            res.send({ token: tokenResponse.data, region: speechRegion });
        } catch (err) {
            res.status(401).send('There was an error authorizing your speech key.');
        }
    }
});

app.get('/api/get-spotify-token', async (req, res, next) => {
    const client_id = process.env.CLIENT_ID;
    const client_secret = process.env.CLIENT_SECRET;

    const headers = {
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        auth: {
            username:  client_id,
            password: client_secret
        },
    };
    const data = {
        grant_type: 'client_credentials'
    };

    try {
        const tokenResponse = await axios.post('https://accounts.spotify.com/api/token',qs.stringify(data),headers);
        res.send({token: tokenResponse.data});
    } catch(err) {
        res.status(401).send('Unable to authorize Spotify token');
    }
});

app.listen(3001, () =>
    console.log('Express server is running on localhost:3001')
);
