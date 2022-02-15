import React, { Component } from 'react';
import { getSpotifyTokenOrRefresh } from './token_util';

// Credit to AzureSpeechReactSimple on github for this


export async function getSpotifyToken() {
    // check for valid speech key/region
    const tokenRes = await getSpotifyTokenOrRefresh();
    if (tokenRes.authToken === null) {
        this.setState({
            displayText: 'FATAL_ERROR: ' + tokenRes.error
        });
    }else{
        return tokenRes.authToken;
    }
}

