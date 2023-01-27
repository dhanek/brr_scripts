import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# %%
plt.style.use("fivethirtyeight")

# %%
df = pd.read_html("https://www.bicyclerollingresistance.com/road-bike-reviews")[1]
df.rename(
    columns={
        "Unnamed: 1": "brand",
        "Unnamed: 2": "model",
        "Unnamed: 4": "TLR",
        "Unnamed: 9": "weight",
        "Unnamed: 12": "rr",
        "Unnamed: 14": "wet",
        "Unnamed: 15": "puncture",
        "Unnamed: 8": "width",
    },
    inplace=True,
)
df.drop(columns=df.columns[df.columns.str.startswith("Unnamed")], inplace=True)

# df = df[df.TLR == "TLR"]
# %%
df["weight"] = df.weight.str.split("/").str.get(1).astype(int)
df["wet"] = df.wet.str.split("/").str.get(0).str.replace("--", "0").astype(int)
df["puncture"] = (
    df.puncture.str.split("/").str.get(0).str.replace("--", "0").astype(int)
)
df["width"] = df.width.str.split("/").str.get(1).astype(int)

idxs = df[df.TLR == "TT"].index
df.loc[idxs, "weight"] = df.loc[idxs, "weight"] + 40
# %%
df["weight_p"] = (df.weight - df.weight.min()) / df.weight.min() * 100
df["rr_p"] = (df.rr - df.rr.min()) / df.rr.min() * 100
df["wet_p"] = (df.wet.max() - df.wet) / df.wet.max() * 100
df["puncture_p"] = (df.puncture.max() - df.puncture) / df.puncture.max() * 100
df["width_p"] = (df.width.max() - df.width) / df.width.max() * 100

# %%
df["sum_all"] = (
    df.weight_p + df.rr_p * 3 + df.wet_p + df.puncture_p * 5 + df.width_p
) / 11
# %%
df.sort_values(by="sum_all", inplace=True)
df.reset_index(drop=True, inplace=True)
fig, ax = plt.subplots(figsize=(10, 22))
ax.barh(y=df.model, width=df.sum_all)
ax.set_title("avg percentage behind best tire in each category")
ax.invert_yaxis()  # labels read top-to-bottom
plt.tight_layout()

# %%
df.sort_values(by="sum_all").head(10)
# %%
