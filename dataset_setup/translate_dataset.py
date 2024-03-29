import requests
import os
import sys


def main():
    root_dir = "../cckres/translated"  # directory to save results
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
        os.mkdir(f"{root_dir}/en")
        os.mkdir(f"{root_dir}/sl")

    if str(sys.argv[1]) == "ensl":
        # If we're translating English to Slovene, the English files are inputs
        listdir = f"{root_dir}/en"
    if str(sys.argv[1]) == "slen":
        # If we're translating Slovene to English, the preprocessed (original) files are inputs
        listdir = "../cckres/preprocessed"

    all_files = os.listdir(listdir)
    for idx, filename in enumerate(all_files):
        f = os.path.join(listdir, filename)
        if str(sys.argv[1]) == "ensl":
            outfile = os.path.join(f"{root_dir}/sl", filename)
        if str(sys.argv[1]) == "slen":
            outfile = os.path.join(f"{root_dir}/en", filename)

        outcontent = []
        batch_num = 1
        print(f"Translating {filename} - {idx+1} / {len(all_files)} ...")

        # We may already have the translation, so skip
        if os.path.isfile(outfile):
            print()
            continue

        # checking if it is a file
        if os.path.isfile(f):
            with open(f, encoding='utf-8') as f:
                contents = f.read()
                lines = contents.split('\n')[:-1]  # get all sentences from the file; last element is an empty line
                i = 0
                while i < len(lines):
                    # Split lines in batches not exceeding ~4500 characters, due to Slovene_NMT constraint
                    chars = 0
                    tokens = []
                    c = 0
                    while chars < 4500 and i+c < len(lines):
                        chars += len(lines[i+c])
                        tokens.append(lines[i+c])
                        c += 1
                    i += c
                    print(f"\tBatch number {batch_num} ... ", end="", flush=True)

                    # Translate with Slovene_NMT running on localhost
                    if str(sys.argv[1]) == "ensl":
                        r = requests.post("http://localhost:4001/api/translate", json={ "src_language": "en",
                                                                                        "tgt_language": "sl",
                                                                                        "text": tokens })
                    if str(sys.argv[1]) == "slen":
                        r = requests.post("http://localhost:4002/api/translate", json={ "src_language": "sl",
                                                                                        "tgt_language": "en",
                                                                                        "text": tokens })
                    batch_num += 1
                    print(r)
                    if r.status_code == 200:
                        temp = r.json()["result"]
                        for t in temp:
                            outcontent.append(t)
                    else:
                        print(f"\t\tStatus code {r.status_code}, {r.text}, text limit was probably exceeded.")
                        # exit(-1)

        if len(outcontent) != 0:
            with open(outfile, 'w', encoding='utf-8') as f:
                for t in outcontent:
                    f.write(t+"\n")
            print(f"Translation of {filename} saved in {outfile}\n")


if __name__ == "__main__":
    if not (str(sys.argv[1]) == "slen" or str(sys.argv[1]) == "ensl"):
        print("Please run the script with argument \"slen\", if you want to translate preprocessed files " + 
              "from ccKres corpus to English, or \"ensl\", if you want to translate the translated English " +
              "files back to Slovene.")
        exit(-1)

    main()
