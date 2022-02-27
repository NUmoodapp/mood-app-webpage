from cgi import test
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, KeywordsOptions, ConceptsOptions, RelationsOptions, EntitiesOptions

authenticator = IAMAuthenticator(
    'gp_Dnnao3ThiGRXgkZBkdDZ-mbcTRUQIwUKOnPZwiuDM')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(
    'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/45b5e28d-3891-42fb-a262-655c664accc7')


def SentimentAnalysis(statement):
    try:
        response = natural_language_understanding.analyze(
            text=statement,
            features=Features(
                emotion=EmotionOptions(),
                keywords=KeywordsOptions(),
                concepts=ConceptsOptions(),
                relations=RelationsOptions(),
                entities=EntitiesOptions(),
            )).get_result()
        print(json.dumps(response, indent=2))
        result = json.loads(json.dumps(response, indent=2))
        return result
    except:
        print('Failed to perform analysis')

#example on accessing emotion of the whole statment below
# exampleText = "Ah, Bikini Bottom. Home to the friendliest creatures under the sea. But how do you know if you're really from Bikini Bottom? You know you are from Bikini Bottom when... this is how you drive."
# example = SentimentAnalysis(exampleText)
# print(example['emotion']['document']['emotion'])#
exampleText = "Jane just broke up with me. I really thought she was the one and I dont know what I will do without her. I should have treated her better. I miss when she was my girlfriend. I loved her."
example = SentimentAnalysis(exampleText)
# exampleText = "Who lives in a pineapple under the sea? SpongeBob SquarePants! Absorbent and yellow and porous is he SpongeBob SquarePants! If nautical nonsense be something you wish SpongeBob SquarePants! Then drop on the deck and flop like a fish! SpongeBob SquarePants!"
# example = SentimentAnalysis(exampleText)
#print(example)

def MakeConceptTuples(response):
    conceptList = []
    for concept in response['concepts']:
        conceptList.append((concept['text'], concept['relevance']))
    return conceptList

def MakeKeywordTuples(response):
    keywordList = []
    for keyword in response['keywords']:
        keywordList.append((keyword['text'], keyword['relevance']))
    return keywordList

# testList = MakeConceptTuples(example)
# print(testList)
# testList = MakeKeywordTuples(example)
# print(type(testList[1][1]))
