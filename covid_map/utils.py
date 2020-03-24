from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import pickle
import pandas as pd 
import numpy as np

def process_df(url, st_abbrev):
    """ 
    Read data from url and preprocess it 
    Parameters: 
    url (link): URL of the DF
    st_abbrev(Dictionary): Dictionary mapping states name with their abbreviation
  
    Returns: 
    pd.df: preprocessed dataframe 
  
    """
    # read url
    df = pd.read_csv(url)
    # only keep states, country,lat,long and last day
    df = df.drop(columns=list(df.columns)[4:-2])
    # filter data for US
    df = df[df["Country/Region"] == "US"]
    # rename columns
    df = df.rename(columns={list(df.columns)[-1]: "cases"})
    df = df.rename(columns={"Province/State": "states"})
    # only keep data for each states
    df = df[np.array([len(word.split(',')) for word in df['states'].tolist()]) == 1]
    # choose states which exists in abbreviation directory
    df = df[[x in st_abbrev.keys() for x in df.states]]
    # replace states names with abbreviation
    df["states"].replace(st_abbrev, inplace=True)
    df=df.dropna()
    return df




# read and convert spreadsheet into dataframe
def get_data_from_sheets(SCOPES,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return pd.DataFrame.from_records(values, columns=values[0])
