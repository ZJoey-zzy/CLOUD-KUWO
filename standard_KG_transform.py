import pandas as pd
import os
import shutil

def copy_dirs(src_path,target_path):
    source_path = os.path.abspath(src_path)
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                

def process_data(source_path, target_path):
    copy_dirs(source_path, target_path)
    triples1 = pd.read_csv(os.path.join(target_path, "rel_triples_1"),sep="\t",header=None).values
    triples2 = pd.read_csv(os.path.join(target_path, "rel_triples_2"),sep="\t",header=None).values
    ent_links = pd.read_csv(os.path.join(target_path, "ent_links"),sep="\t",header=None).values
    attr1 = pd.read_csv(os.path.join(target_path, "attr_triples_1"),sep="\t",header=None).values
    attr2 = pd.read_csv(os.path.join(target_path, "attr_triples_2"),sep="\t",header=None).values
    
    triples1_li = []
    for triple in triples1:
        h,r,t = triple
        triples1_li.append([str(h)+ "_1", str(r) + "_1", str(t) + "_1"])
    triples2_li = []
    for triple in triples2:
        h,r,t = triple
        triples2_li.append([str(h)+ "_2", str(r) + "_2", str(t) + "_2"])
    ent_links_li = []
    for link in ent_links:
        i1 , i2 = link
        ent_links_li.append([str(i1) + "_1", str(i2) + "_2"])
    attr1_li = []
    for triple in attr1:
        h,r,t = triple
        attr1_li.append([str(h)+ "_1", str(r), str(t)])
    attr2_li = []
    for triple in attr2:
        h,r,t = triple
        attr2_li.append([str(h)+ "_2", str(r), str(t)])
    pd.DataFrame(triples1_li).to_csv(os.path.join(target_path, "rel_triples_1"), sep = "\t", header=False,index=False)
    pd.DataFrame(triples2_li).to_csv(os.path.join(target_path, "rel_triples_2"), sep = "\t", header=False,index=False)
    pd.DataFrame(ent_links_li).to_csv(os.path.join(target_path, "ent_links"), sep = "\t", header=False,index=False)
    pd.DataFrame(attr1_li).to_csv(os.path.join(target_path, "attr_triples_1"), sep = "\t", header=False,index=False)
    pd.DataFrame(attr2_li).to_csv(os.path.join(target_path, "attr_triples_2"), sep = "\t", header=False,index=False)
    
def single_encoder(triples, ent_id_start=0, rel_id_start=0):
    ent_id = ent_id_start
    rel_id = rel_id_start
    ent_encoder = {}
    rel_encoder = {}
    for triple in triples:
        h,r,t = triple
        if h not in ent_encoder:
            ent_encoder[h] = ent_id
            ent_id += 1
        if t not in ent_encoder:
            ent_encoder[t] = ent_id
            ent_id += 1
        if r not in rel_encoder:
            rel_encoder[r] = rel_id
            rel_id += 1
    return ent_encoder, rel_encoder, ent_id, rel_id

def triples2encoded_df(triples, ent_encoder, rel_encoder):
    li = []
    for triple in triples:
        h,r,t = triple
        li.append([ent_encoder[h], rel_encoder[r], ent_encoder[t]])
    return pd.DataFrame(li)

def ent_link2ill_ent_df(ent_links, ent_encoder1, ent_encoder2):
    li = []
    for ent_link in ent_links:
        ent1, ent2 = ent_link
        li.append([ent_encoder1[ent1], ent_encoder2[ent2]])
    return pd.DataFrame(li)

def dic2df(dic):
    li =  [[v,k] for k,v in dic.items()]
    return pd.DataFrame(sorted(li,key = lambda row:row[0]))

def transform_data(source_path, target_path):
    triples1 = pd.read_csv(os.path.join(source_path, "rel_triples_1"),sep="\t",header=None).values
    triples2 = pd.read_csv(os.path.join(source_path, "rel_triples_2"),sep="\t",header=None).values
    ent_links = pd.read_csv(os.path.join(source_path, "ent_links"),sep="\t",header=None).values
    df_li = []
    df_name_li = []
    
    ent_encoder1, rel_encoder1, max_ent_id_1_plus1, max_rel_id_1_plus1 = single_encoder(triples1)
    ent_encoder2, rel_encoder2, _, _ = single_encoder(triples2, max_ent_id_1_plus1, max_rel_id_1_plus1)
    encoder_li = [ent_encoder1, ent_encoder2, rel_encoder1, rel_encoder2]
    df_li.extend([dic2df(encoder) for encoder in encoder_li] )
    df_name_li.extend(["ent_ids_1", "ent_ids_2", "rel_ids_1", "rel_ids_2"])
    
    encoded_triples_1_df = triples2encoded_df(triples1, ent_encoder1, rel_encoder1)
    encoded_triples_2_df = triples2encoded_df(triples2, ent_encoder2, rel_encoder2)
    encoded_ill_ent_df = ent_link2ill_ent_df(ent_links, ent_encoder1, ent_encoder2)
    df_li.extend([encoded_triples_1_df, encoded_triples_2_df ,encoded_ill_ent_df])
    df_name_li.extend(["triples_1", "triples_2", "ill_ent_ids"])
    
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for i, df in enumerate(df_li):
        file_path = os.path.join(target_path, df_name_li[i])
        df.to_csv(file_path, sep = "\t", header=False,index=False)
        
    # rename the atrribute file
    if not os.path.exists(os.path.join(target_path, "training_atrrs_1")) and not os.path.exists(os.path.join(target_path, "training_atrrs_2")):
        shutil.copy(os.path.join(source_path, "attr_triples_1"), target_path)
        shutil.copy(os.path.join(source_path, "attr_triples_2"), target_path)
        os.rename(os.path.join(target_path, "attr_triples_1"), os.path.join(target_path, "training_atrrs_1"))
        os.rename(os.path.join(target_path, "attr_triples_2"), os.path.join(target_path, "training_atrrs_2"))
    
    
if __name__ == "__main__":
    process_data("./CLOUD-KUWO_org/", "./processed_kg")
    transform_data("./processed_kg", "./CLOUD-KUWO")