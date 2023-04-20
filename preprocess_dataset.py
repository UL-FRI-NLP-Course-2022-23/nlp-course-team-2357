import os
import urllib.request as req
import nltk
import re


def main():
    nltk.download('punkt')

    data_dir = "cckres"
    if not os.path.exists(data_dir+"/preprocessed"):
        os.mkdir("cckres/preprocessed")

    i = 0
    for filename in os.listdir("cckres/text"):
        f = os.path.join("cckres/text", filename)
        outfile = os.path.join("cckres/preprocessed", filename)
        outcontent = []
        # checking if it is a file
        if os.path.isfile(f):
            with open(f) as f:
                contents = f.read()
                contents = re.sub('[\n]+', '\n', contents)
                contents = contents.strip()
                tokens = nltk.sent_tokenize(contents)
                for t in tokens:
                    if t[0].isupper() and (t[len(t)-1] == '.' or t[len(t)-1] == '?' or t[len(t)-1] == '!'):
                        outcontent.append(re.sub('\n', ' ', t))
        
        if len(outcontent) != 0:
            with open(outfile, 'a') as f:
                for t in outcontent:
                    f.write(t+"\n")
        
        i += 1
        if i == 10:
            break


if __name__ == "__main__":
    main()
