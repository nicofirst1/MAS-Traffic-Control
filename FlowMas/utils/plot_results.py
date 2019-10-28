import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import collections

def flatten(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

res_dir="/Users/giulia/Desktop/results"

res_dict={}

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(res_dir):
    if "result.json" in files:
        pt=os.path.join(root,"result.json")
        with open(pt,"r+") as f:
            d=f.readlines()

        d=[json.loads(elem) for elem in d]

        d=[flatten(elem) for elem in d]
        d=pd.DataFrame(d)

        pt = os.path.join(root, "parameter_attributes.json")
        with open(pt,"r+") as f:
            pa=json.load(f)

        k=f"{pa['training_alg']}_coop{pa['coop_rl_vehicle_num']}_self{pa['selfish_rl_vehicle_num']}_human{pa['human_vehicle_num']}"

        res_dict[k]=dict(
            results=d,
            params=pa,

        )


to_plot=[
    'Actions',
    'Delays',
    'Jerks',
    "Rewards"
]


for field in to_plot:

    for k,v in res_dict.items():
        # gca stands for 'get current axis'
        ax = plt.gca()

        df=v["results"]
        if f"custom_metrics/{field}/RL_coop_mean" in df.keys() :

            df.reset_index().plot(kind='line', y=f"custom_metrics/{field}/RL_coop_mean",x="index", ax=ax)
        if f"custom_metrics/{field}/all_mean" in df.keys() :
            df.reset_index().plot(kind='line', y=f"custom_metrics/{field}/all_mean",x="index", ax=ax)
        if f"custom_metrics/{field}/RL_selfish_mean" in df.keys() :

            df.reset_index().plot(kind='line', y=f"custom_metrics/{field}/RL_selfish_mean", x="index", ax=ax)

        ax.set_title(k)
        ax.set_xlabel("generation")
        ax.set_ylabel(field)
        plt.show()





