import os
import nltk
import re
from tqdm import tqdm


def clean_up(contents: str):
    """
    Clean up file contents a bit.
    """
    for brace in ["{", "["]:
        contents = contents.replace(brace, "(")

    for brace in ["}", "]"]:
        contents = contents.replace(brace, ")")

    for quote in ["«", "»", "`", "´", "ʼ", "‘", "’", "‛", "‹", "›", "“", "”", "„", "″"]:
        contents = contents.replace(quote, "\"")

    for dash in ["‑", "‒", "–", "—", "―", "−", "─"]:
        contents = contents.replace(dash, "-")

    contents = contents.replace("•", " ")
    contents = contents.replace("…", "...")
    contents = contents.strip()

    return contents


def main():
    nltk.download('punkt')

    source_dir = "../cckres/text"  # directory with raw, original text
    preprocessed_dir = "../cckres/preprocessed"  # directory to store the preprocessed files
    if not os.path.exists(preprocessed_dir):
        os.mkdir(preprocessed_dir)

    for filename in tqdm(os.listdir(source_dir)):
        f = os.path.join(source_dir, filename)
        outfile = os.path.join(preprocessed_dir, filename)
        outcontent = []

        # checking if it is a file
        if not os.path.isfile(f):
            continue

        with open(f, encoding='utf-8') as f:
            contents = f.read()
            contents = clean_up(contents)
            tokens = nltk.sent_tokenize(contents, language='slovene')  # split into sentences

            for t in tokens:
                # Replace any non-ASCII character except čćšžđČĆŠŽĐ with whitespace
                t = re.sub(r"[^\x00-\x7FčćšžđČĆŠŽĐ]", ' ', t)  
                t = re.sub('\n', ' ', t)
                t = re.sub('[ ]+', ' ', t)
                t = t.strip()

                # Remove too short or too long sentences
                words = t.split(" ")
                if len(words) < 4 or len(words) > 50:
                    continue

                # Ignore sentences that contain non ASCII characters, excluding č, ć, š and ž
                # temp = t.lower().replace("č", "c").replace("ć", "c").replace("ž", "z").replace("š", "s")
                # if not temp.isascii():
                #     continue

                # Make sure the sentence starts and ends properly
                if t[0].isupper() and (t[len(t)-1] == '.' or t[len(t)-1] == '?' or t[len(t)-1] == '!'):
                    outcontent.append(t)
        
        if len(outcontent) == 0:
            continue

        with open(outfile, 'w', encoding='utf-8') as f:
            for t in outcontent:
                f.write(t+"\n")


if __name__ == "__main__":
    main()
