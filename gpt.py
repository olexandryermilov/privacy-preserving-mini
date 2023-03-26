import csv
import logging
import openai
import sys

openai_key = "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"

def get_response(text):
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Replace every named entity in the sentence using named entities of the same type. Do not change other words"},
            #{"role": "user", "content": "Replace: Sasha lives in Germany."},
            #{"role": "assistant", "content": "Answer: Yaroslav lives in Poland."},
            #{"role": "user", "content": "Replace: I will meet Artem tomorrow at the Google office in New York."},
            #{"role": "assistant", "content": "Answer: I will meet Kyrylo tomorrow at the Facebook office in San Francisco."},
            #{"role": "user", "content": "Replace: I asked Lena from Twitter to reply to my email."},
            #{"role": "assistant", "content": "Answer: I asked Yana from Tiktok to reply to my email."},
            {"role": "user", "content": "Replace:" + text},
        ]
    )
    return response

def process_text(text) -> str:
    resp = get_response(text)
    response = resp['choices'][0]['message']['content'].strip()

    return response

# Insert the text you want to get the outputs here
#text = "I will go to Paris, France with Daniel. I met Daniel in Starbucks and talked to him about Harry Potter films and Harry Potter franchise main star, Emma Watson."
#process_text(text)
file_path = sys.argv[1]
with open(file_path, "r") as input_file, open(file_path.split(".")[0]+"_gpt35.txt", "w") as output_file:
    # Loop through each line in the input file
    for line in input_file:
        # Apply the process_line function to the current line
        processed_line = process_text(line)
        # Write the processed line to the output file
        output_file.write(processed_line)
        output_file.write("\n")