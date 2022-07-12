import sys

filename = r"C:\Users\Shamik Bose\Downloads\Royal_Society_Corpus_v2.0.2_final\Royal_Society_Corpus_v2.0.2_final.vrt"
limit = 10
with open(filename, "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        print(line)
        count += 1
        if count > limit:
            break
