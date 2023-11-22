from setup import *

!wget -c https://www.dropbox.com/sh/9aozrd1fv0bg1xd/AACCM0Y4J9fFTSv9YSjrKO1ya?dl=0 -O eqtl_data.zip
!unzip -o eqtl_data.zip -d eqtl_data
os.unlink("eqtl_data.zip")
eqtl_data = {}
for fname in os.listdir("eqtl_data"):
    with open(os.path.join("eqtl_data", fname), "r") as R:
        eqtl_data[fname] = R.read().encode('utf-8')

# Processes *Data.txt files
"""
Example inp:
    Patient Trait1 Trait2 Trait3
    A 0.1 0.2 0.3
    B 0.4 0.5 0.6
    C 0.7 0.8 0.9

process_file(inp, "patient")
    [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]

process_file(inp, "trait")
    {"Trait1": [0.1, 0.4, 0.7], "Trait2": [0.2, 0.5, 0.8], "Trait3": [0.3, 0.6, 0.9]}
"""
def process_file(inp, mode):
    rows = inp.decode("utf-8").split("\n")
    if mode == "patient":
        return [[float(val) for val in row.split()[1:]] for row in rows[1:] if row]
    elif mode == "trait":
        res = pd.DataFrame([row.split()[1:] for row in rows if row])
        res.columns = res.iloc[0]
        return {k: [float(val) for val in v.values()] for k, v in res[1:].to_dict().items()}

#process_file(eqtl_data["SnpData.txt"], "patient")
#process_file(eqtl_data["SnpData.txt"], "trait")
#process_file(eqtl_data["ExpData.txt"], "patient")
#process_file(eqtl_data["ExpData.txt"], "trait")