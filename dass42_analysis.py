import pandas as pd
import json

data_file_path = ".\data\emotouchdb-70b2a-export.json"
#dass42_answers = pd.DataFrame(columns=[for i in range(42)])
dass42_answers = []

with open(data_file_path) as f:
    json_data = json.load(f)
    for user in json_data:
        #print(user)
        try:
            user_answer = [user]
            if len(json_data[user]["dass42"]) != 42:
                print ("{}: number of answers not correct ({})".format(user, len(json_data[user]["dass42"])))
            else:
                user_answer.extend(json_data[user]["dass42"])
                dass42_answers.append(user_answer)
        except KeyError:
            print("{}: dass42 not present".format(user))

dass42 = pd.DataFrame(dass42_answers)
print(dass42.shape)
dass42.to_csv(".\data\export\dass42.csv", index=False)
