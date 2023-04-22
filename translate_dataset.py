@@ -0,0 +1,61 @@
import requests
import os
import sys
import nltk

def main():
    data_dir = "cckres"
    if not os.path.exists(data_dir+"/translated"):
        os.mkdir("cckres/translated")
        os.mkdir("cckres/translated/en")
        os.mkdir("cckres/translated/sl")

    if str(sys.argv[1]) == "ensl":
        listdir = "cckres/translated/sl"
    if str(sys.argv[1]) == "slen":
        listdir = "cckres/preprocessed"

    for filename in os.listdir(listdir):
        f = os.path.join("cckres/preprocessed", filename)
        if str(sys.argv[1]) == "ensl":
            outfile = os.path.join("cckres/translated/sl", filename)
        if str(sys.argv[1]) == "slen":
            outfile = os.path.join("cckres/translated/en", filename)
        r = []
        outcontent = []
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, encoding='utf-8') as f:
                contents = f.read()
                lines = nltk.sent_tokenize(contents)
                i = 0
                while i < len(lines):
                    chars = 0
                    tokens = []
                    c = 0
                    while chars < 4000 and i+c < len(lines):
                        chars += len(lines[i+c])
                        tokens.append(lines[i+c])
                        c += 1
                    i += c
                    if str(sys.argv[1]) == "ensl":
                        r = requests.post("http://localhost:4001/api/translate", json={ "src_language": "en",
                                                                                        "tgt_language": "sl",
                                                                                        "text": tokens })
                    if str(sys.argv[1]) == "slen":
                        r = requests.post("http://localhost:4002/api/translate", json={ "src_language": "sl",
                                                                                        "tgt_language": "en",
                                                                                        "text": tokens })
                    print(r)
                    if r.status_code == 200:
                        temp = r.json()["result"]
                        for t in temp:
                            outcontent.append(t)
        if len(outcontent) != 0:
            with open(outfile, 'a', encoding='utf-8') as f:
                for t in outcontent:
                    f.write(t+"\n")


if __name__ == "__main__":
    main()
