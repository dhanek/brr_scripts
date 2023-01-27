import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# %%
plt.style.use("fivethirtyeight")

# %%
df = pd.read_html("https://www.bicyclerollingresistance.com/cx-gravel-reviews")[1]
df.rename(
    columns={
        "Unnamed: 1": "brand",
        "Unnamed: 2": "model",
        "Unnamed: 8": "width",
        "Unnamed: 9": "weight",
        "Unnamed: 14": "knobs",
        "Unnamed: 10": "rr",
        "Unnamed: 15": "wet",
        "Unnamed: 16": "puncture",
    },
    inplace=True,
)
df.drop(columns=df.columns[df.columns.str.startswith("Unnamed")], inplace=True)
# %%
df["weight"] = df.weight.str.split("/").str.get(1).astype(int)
df["width"] = df.width.str.split("/").str.get(1).astype(int)
df["knobs_center"] = df.knobs.str.split("/").str.get(0).astype(float)
df["knobs_edge"] = df.knobs.str.split("/").str.get(1).astype(float)
df["wet"] = df.wet.str.split("/").str.get(0).astype(int)
df["puncture"] = df.puncture.str.split("/").str.get(0).astype(int)
df["knobs_combined"] = (df.knobs_center + df.knobs_edge) / 2
# %%
df["weight_p"] = (df.weight - df.weight.min()) / df.weight.min() * 100
df["rr_p"] = (df.rr - df.rr.min()) / df.rr.min() * 100
df["knobs_center_p"] = (
    (df.knobs_center.max() - df.knobs_center) / df.knobs_center.max() * 100
)
df["knobs_edge_p"] = (df.knobs_edge.max() - df.knobs_edge) / df.knobs_edge.max() * 100
df["width_p"] = (df.width.max() - df.width) / df.width.max() * 100
df["wet_p"] = (df.wet.max() - df.wet) / df.wet.max() * 100
df["puncture_p"] = (df.puncture.max() - df.puncture) / df.puncture.max() * 100
df["knobs_combined_p"] = (
    (df.knobs_combined.max() - df.knobs_combined) / df.knobs_combined.max() * 100
)
# %%
df["sum_all"] = (
    df.weight_p
    + df.rr_p * 3
    + df.knobs_center_p
    + df.knobs_edge_p
    # + df.wet_p
    + df.puncture_p * 3
    # + df.knobs_combined_p
    + df.width_p
) / 10

# %%
df.sort_values(by="sum_all", inplace=True)
df.reset_index(drop=True, inplace=True)
fig, ax = plt.subplots(figsize=(10, 12))
ax.barh(y=df.model, width=df.sum_all)
ax.set_title("avg percentage behind best tire in each category")
ax.invert_yaxis()  # labels read top-to-bottom
plt.tight_layout()

# %%
df.sort_values(by="sum_all").head(10)[
    ["brand", "model", "width", "weight", "rr", "knobs", "wet", "puncture", "sum_all"]
]
# %%
