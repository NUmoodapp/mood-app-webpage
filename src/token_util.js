import axios from 'axios';
import Cookie from 'universal-cookie';

export async function getTokenOrRefresh() {
    const cookie = new Cookie();
    const speechToken = cookie.get('speech-token');

    if (speechToken === undefined) {
        try {
            const res = await axios.get('http://localhost:3001/api/get-speech-token');
            const token = res.data.token;
            const region = res.data.region;
            cookie.set('speech-token', region + ':' + token, {maxAge: 540, path: '/'});

            console.log('Token fetched from back-end: ' + token);
            return { authToken: token, region: region };
        } catch (err) {
            console.log(err.response.data);
            return { authToken: null, error: err.response.data };
        }
    } else {
        console.log('Token fetched from cookie: ' + speechToken);
        const idx = speechToken.indexOf(':');
        return { authToken: speechToken.slice(idx + 1), region: speechToken.slice(0, idx) };
    }
}

export async function getSpotifyTokenOrRefresh() {
    const spot_cookie = new Cookie();
    const spotifyToken = spot_cookie.get('spotify-token');

    if (spotifyToken === undefined) {
        try {
            const spot_res = await axios.get('http://localhost:3001/api/get-spotify-token');
            const spot_token = spot_res.data.token.access_token;
            spot_cookie.set('spotify-token', spot_token, {maxAge: 540, path: '/'});

            console.log('Spotify token fetched from back-end: ' + spot_token);
            return { authToken: spot_token };
        } catch (spot_err) {
            console.log("error in getSpotifyTokenOrRefresh: ",spot_err.response.data);
            return { authToken: null, error: spot_err.response.data };
        }
    } else {
        console.log('Spotify token fetched from cookie: ' + spotifyToken);
        return { authToken: spotifyToken };
    }
}
