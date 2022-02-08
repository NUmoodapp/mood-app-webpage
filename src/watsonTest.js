const NaturalLanguageUnderstandingV1 = require('ibm-watson/natural-language-understanding/v1');
const { IamAuthenticator } = require('ibm-watson/auth');
const naturalLanguageUnderstanding = new NaturalLanguageUnderstandingV1({
    version: '2021-03-25',
    authenticator: new IamAuthenticator({
        apikey: 'gp_Dnnao3ThiGRXgkZBkdDZ-mbcTRUQIwUKOnPZwiuDM',
    }),
    serviceUrl: 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/45b5e28d-3891-42fb-a262-655c664accc7',
});
const text2Analyze = 'To be, or not to be, that is the question: Whether tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles And by opposing end them. To die—to sleep, No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to: tis a consummation Devoutly to be wished. To die, to sleep; To sleep, perchance to dream—ay, theres the rub:';
const analyzeParams = {
    'text': text2Analyze,
    'features': {
        'emotion': {
        },
        'entities': {
            'emotion': true,
            'sentiment': true,
            'limit': 10,
        },
        'keywords': {
            'emotion': true,
            'sentiment': true,
            'limit': 10,
        },
    },
};
naturalLanguageUnderstanding.analyze(analyzeParams)
    .then(analysisResults => {
        console.log(JSON.stringify(analysisResults, null, 2));
    })
    .catch(err => {
        console.log('error:', err);
    });
