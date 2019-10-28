import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import collections
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Plot results from different trainings. You should use as input a folder in which multiple dirs store "result.json" and "parameter_attributes.json"')
parser.add_argument('-input_dir', type=str, required=True,
                    help='The direcotry in which the training folders are stored')
parser.add_argument('--out_dir',type=str,default="out/",
                    help='Output dir to which save images')

args = parser.parse_args()


input_dir=args.input_dir
out_dir=os.path.join(input_dir, args.out_dir)

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

def flatten(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


res_dict={}

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(input_dir):
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


for field in tqdm(to_plot):

    for k,v in res_dict.items():
        # gca stands for 'get current axis'

        plt.clf()
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

        if "/" in k:
            key=k.split("/")[-1]
        else:
            key=k
        pt=os.path.join(out_dir,f"{key}_{field}")
        plt.savefig(pt)





