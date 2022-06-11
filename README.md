# Original data

The data was collected from Cloud Music Website (https://music.163.com/) and Kuwo Music Website (http://www.kuwo.cn/)



The original data is in `data set construstion/org_data` which is in `.csv` form



# Data set construction

make the working directory be `data set construstion`

```bash
cd ./data set construstion
```

Run in order

`data_preprocessing.ipynb`

`identity_links.ipynb`

`build_links.ipynb`



# Transform the kg for training

original kg in `CLOUD-KUWO_org` consists of 5 files: `attr_triples_1`, `attr_triples_2`, `rel_triples_1`, `rel_triples_2`, `ent_links`

It is suitable to read for human but not good for training



It should encode transform the kg format to a form that suitable for training

run `standard_KG_transform.py` 

to transform  `CLOUD-KUWO_org`  to  `CLOUD-KUWO` 



# Training command

make the working directory to `training`

```bash
cd ./training
```



run mtranse in CLOUD-KUWO

```bash
python run.py --log mtranse \
--data_dir "data/CLOUD-KUWO" \
--rate 0.3 \
--epoch 1000 \
--check 10 \
--update 10 \
--train_batch_size 5000 \
--encoder "" \
--hiddens "100" \
--decoder "TransE,MTransE_Align" \
--sampling ".,." \
--k "0,0" \
--margin "0,0" \
--alpha "1,50" \
--feat_drop 0.0 \
--lr 0.01 \
--train_dist "euclidean" \
--test_dist "euclidean"
```



run gcnalign in CLOUD-KUWO

```bash
python run.py --log gcnalign \
--data_dir "data/CLOUD-KUWO" \
--rate 0.3 \
--epoch 1000 \
--check 10 \
--update 10 \
--train_batch_size -1 \
--encoder "GCN-Align" \
--hiddens "100,100,100" \
--decoder "Align" \
--sampling "N" \
--k "25" \
--margin "1" \
--alpha "1" \
--feat_drop 0.0 \
--lr 0.005 \
--train_dist "euclidean" \
--test_dist "euclidean"
```



# Results

make the working directory be `training`

```bash
cd ./training
```



use `tensorboard` to see the training  results

```bash
tensorboard --logdir "_runs" 
```

