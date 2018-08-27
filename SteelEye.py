import pandas as pd
import numpy as np
import json
import boto3

df = pd.read_excel('ISO10383_MIC.xls', header=0,sheet_name="MICs List by CC")

keys = df.columns.tolist()

df.fillna(value="?", inplace=True)
dict_list = []
for x in range(0,len(df)):
    values = df.iloc[x]
    dict_list.append(dict(zip(keys,values)))

with open('MICbyCC.json', 'w') as f:
    json.dump(dict_list, f)

with open('MICbyCC.json') as f:
    string = f.read()

encoded_string = string.encode("utf-8")

def lambda_handler(event, context,filename):
    bucket_name = "s3bucket"
    file_name = "MIC.txt"
    lambda_path = "/tmp/" + file_name
    s3_path = "/test/SteelEye/" + file_name
    s3 = boto3.resource("s3")
    
    try:
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    except Exception as e:
        print(e)
        print("Error writing to bucket. Ensure bucket is created among other things")
        raise e
        
