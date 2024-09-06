# tfashion1.5 - A model to filter fashion-related words
## Softer Matching - a matching strategy based on cosine similarity using BERT embeddings
- input: topics_filtered.csv (expanded), post_cleaned.csv
- output: post_filtered.csv

### Explanation
- BERT-based Embeddings: We get the word embeddings for each word using BERT.
- Cosine Similarity: For each word in the fashion_keywords column, we calculate the cosine similarity to every word in the fashion lexicon.
- Soft Threshold: If the cosine similarity exceeds the threshold (set to 0.6), we consider the word "fashion-related" and include it in the final list.
- Softer Match: Instead of a hard match (exact word match), this approach allows words that are close in meaning to be considered fashion-related.

### Resuls from soft threshold 0.8
- examples of original post text:
  1. 做自己的黑粉 少女感🥰 蝴蝶结元素好少女、缎面雪纺裙嘎嘎好穿#粉黑配色 #超短裙 #少女感穿搭  #泡泡袖 #粉色少女心 #粉色 #蝴蝶结 #黑粉配色 #半身裙,
  2. 可爱遛狗穿搭～ #大学生 #穿搭 #夏季短袖 #春季穿搭 #气质穿搭 #小个子穿搭 #日常穿搭 #ootd每日穿搭 #每日穿搭,
  3. 国民初恋裴秀智牛仔裤配衬衫，韩系松弛感绝 裴姐不愧是南韩国民初恋，气质超绝！美得毫不费力，穿着简简单单的衬衫和牛仔裤真的好像在拍韩剧，最后再搭上披肩增加层次感，水洗蓝小香风设计感牛仔裤➕质感好的衬衫跟着裴秀智穿这种松弛感，同事说我上班穿得像去拍韩剧#裴秀智#韩系穿搭 #衬衫 #披肩 #韩女 #missa  #女明星穿搭 #女明星私服 #不费力气的穿搭 #简约穿搭 #小香风牛仔裤 #ins博主穿搭 #松弛感 #跟着明星学穿搭 #牛仔裤 #复古牛仔裤 #初恋#气质穿搭

- examples of filtered post text:
  1. 做自己的黑粉 少女感smilingfacewithhearts 蝴蝶结元素好少女缎面雪纺裙嘎嘎好穿 粉黑配色 超短裙 少女感穿搭 泡泡袖 粉色少女心 粉色 蝴蝶结 黑粉配色 半身裙']
  2. 可爱遛狗穿搭 大学生 穿搭 夏季短袖 春季穿搭 气质穿搭 小个子穿搭 日常穿搭 ootd每日穿搭 每日穿搭 
  3. []
-------------------------------------------------------------------------------------------------------------------------------------------------

# tfashion1.0 - A model to filter fashion-related words
see [tfashion.ipynb](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/tfashion.ipynb)
## Step 1. Get a non-fashion Chinese corpus
- Chinese Wikipedia Dump
- Use WikiExtractor to convert the XML dump into plain text
- Get extracted_texts
- Filter Non-Fashion Content from the Extracted Texts, using fashion keywords

## Step 2. Prepare Data for Model Training
- Tokenize the Non-Fashion Texts
- Combine with Fashion-Related Tokens

## Step 3. Train the Model
- Split the Data into Training and Validation Sets
- Fine-Tune BERT

## (Optional) Check data before training
- Check Data Shapes
- Check for Any 'NaN' Values
- Check Data Distribution
- Inspect a Few Examples
- Check Label Value Range
- Verify Dataset Splitting
- Check for Duplicates

## Step 4. Evaluate the Model
 - evaluation resutls:
   
![Screenshot 2024-08-31 at 19 56 45](https://github.com/user-attachments/assets/fb94593b-943a-45f4-b535-7e56b91a3a40)

![Screenshot 2024-08-31 at 19 56 59](https://github.com/user-attachments/assets/debace4e-2335-4118-99c6-5f59dac7947b)

## Step 5. Apply the model
- prepare post data
  - input: [poster_test_fashion_nlpclean.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/poster_test_fashion_nlpclean.csv)
  - Combine 'post_title' and 'post_content' into 'post_text'
  - Clean and Tokenize 'post_text'
- Filter Non-Fashion Words Using the Model
- output: [post_filtered.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/post_filtered.csv)

### Results:
- empty values in column fashion_text because the model works in the whole phrase not the individual words.
-------------------------------------------------------------------------------------------------------------------------------------------------

# Clustering based on text

## Use dictionary
see [nlp_dict.ipynb](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/nlp_dict.ipynb)
### Dictionary 1 - General
##### Input: [topics0611.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics0611.csv), [poster_test_fashion_nlpclean.csv]()
##### Output: [word_suffixes.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/word_suffixes.csv), keyword_freq_dict1.csv, keyword_freq_by_month_dict1.csv
##### Steps: 
1. Extract common suffixes from the topics0611.csv file.
2. Use those suffixes to search for complete words in the poster_test_fashion_nlpclean.csv file.
3. Do textual data cleaning again.
4. Count overall frequency and by-month frequency.
5. Match images and visualize the popularity by images.

#### Text visualization
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/14ac29e2-dbe5-4c53-953e-50a6bd1051a2" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/284c782c-b9fc-4c50-921a-28322007ed63" alt="Image 2" width="45%"/>
</div>

#### Image visualization

- Overall Frequency Visualization
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/4da53b0d-3ab0-4eda-b69e-f2655674237f" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/9dbf8ab9-2d9d-450f-8d87-70aad0a2244a" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/9562d664-52de-4d3b-8fb0-b47b4b8f0f9e" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/d6ec9d5e-9d17-49f4-af20-d0a60ac5b288" alt="Image 2" width="45%"/>
</div>

- By-Month Frequency Visualization

</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/dcbbe8a9-416e-456c-a9c4-4c3b4c221c9f" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/93da4ca5-a3e0-4b3f-8302-49bde22c4e35" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/021d88bd-edc3-43a2-baff-559db2a71cc7" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/34bff7d0-2413-4e6e-8d68-a0f404180ac3" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/e93fb66e-a033-45c0-8ecc-3cd3364db5b1" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/4065706b-ce34-46c9-9f03-231ce1b0e9e2" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/c43c038c-184b-4d02-b694-8694213a35ca" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/00f49691-201a-4aae-b44d-451bcd720596" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/d434472e-cd24-446a-8735-b3be249e348c" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/9b32dbc2-762d-4850-8c58-6c9aa7a13a0e" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/8099ef99-041b-49d9-a2ee-af2066decd64" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/c6b0ac01-e113-42b5-88d3-c1550941d52b" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/0130a4b9-3f89-4a8c-b942-4e682154907f" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/06fe12c3-edc5-4be0-bdf4-8bde79a8d4e8" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/4e31eaf3-94d4-40bf-9688-91fded50e291" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/891c8aaf-4590-446a-8a2a-2fedc592220c" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/a0f57811-3dc4-42fd-a90b-4452a3df7513" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/b5545b85-abb1-4292-896b-8706853f10c9" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/40235c82-356b-4d96-912e-48e071ca3d26" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/9c274feb-8b17-400d-a0b6-86072e0229c8" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/7b1184a6-413d-4a4c-b25c-0c35f0bf4374" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/f9ad1c08-497d-43a5-9b90-bb1cf55a7292" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/3a50b8c5-2f6f-45d9-b620-3a0846b850b4" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/2066ef33-d687-4a91-ae97-ee5e680e37f1" alt="Image 2" width="45%"/>
</div>

### Dictionary 2 - Specific 
##### Inputs: [topics0611.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics0611.csv), [poster_test_fashion_nlpclean.csv]()
##### Outputs: keyword_freq_dict2.csv, keyword_freq_by_month_dict2.csv
##### Steps:
1. Use topics0611.csv to do exact match with poster_test_fashion_nlpclean.csv.
2. Count overall frequency and by-month frequency.
3. Match images and visualize the popularity by images.

#### Text visualization
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/dc946c0d-09f3-45f3-91db-e238a193b6df" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/81483025-0f69-4d64-b23a-a211ff5f8969" alt="Image 2" width="45%"/>
</div>

#### Image visualization

- Overall Frequency Visualization
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/3ee70019-a4d0-485b-9440-bdba111994da" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/7da914b6-4bd3-451d-b1c3-ef1ce46adaf8" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/ace39e68-f010-45e6-98b0-f56a9ee8e20e" alt="Image 1" width="33%"/>
  <img src="https://github.com/user-attachments/assets/7a989d3f-be9b-4c4c-837e-4f0068c1dcd3" alt="Image 2" width="33%"/>
  <img src="https://github.com/user-attachments/assets/8e419642-fb95-456b-a84c-eba465021593" alt="Image 2" width="33%"/>
</div>

- By-Month Frequency Visualization
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/8ba4c1c6-e9e8-4d22-a9f6-4dd28aac06b3" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/d969cbb0-de30-40e5-b089-583b24b3a631" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/38cbc41f-d621-480e-a0b2-de76d8d9785b" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/c111c75e-95d4-43e9-9a8b-5b9ddc297e3d" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/e8523f35-811b-4348-b19e-50eb35a24b6a" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/20ddb204-221b-47c6-b445-20e07971dfc7" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/d9f0282e-6b59-44db-8e7b-16ad5d0a5599" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/f5b5b9d5-981d-4ef7-b85c-09797b7d38ab" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/8d624106-c8c3-4ebc-b433-919712738b73" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/16d3d0c1-96ac-43b2-a313-4352d12ce3c9" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/790b5e8b-3bed-4ec8-b06a-e518372fb2a2" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/aa2597a8-f574-440e-9e13-87d2cfcea65b" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/ef276976-1195-4aa3-be48-6d6a6d653704" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/13365890-3aef-4923-86db-4078ac849aa2" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/373fe8b8-f0ef-47f0-a6e4-da1a91905b5b" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/339e08d3-f3aa-483d-ba6e-e474be3108cc" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/a0b1f529-da87-4d8d-b984-38cd61534573" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/90552ff2-909b-41f7-b9db-db1211490e84" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/505b4d4a-bd23-4a56-96ca-f7dca1da1c50" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/6f061100-4e6c-4505-b62e-e53f00511bc3" alt="Image 2" width="45%"/>
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/c05b6389-35da-4b8e-ae52-affc69f88534" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/f178d7ed-3e26-4434-88c2-6d8aaf61a235" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/de2e855d-da16-4842-9196-c02dbf0b6646" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/8e6c0d2a-4166-43c4-a8a9-a9fb3a632d44" alt="Image 2" width="45%"/>
</div>

## No dictionary
see [nlp_nodict.ipynb](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/nlp_nodict.ipynb)
##### Inputs: poster_test_fashion_nlpclean.csv
##### Outputs: poster_test_fashion_clustered.csv
##### Steps:
1. Double cleaning on textual data
2. RAKE keyword extraction
3. Use text2vec-large-chinese to generate embedding
4. Use Silhouette Method to find the optimal number of clusters
5. Do KMeans clustering
6. Visualize results

- The best number of clusters based on silhouette score is: 51
- Visualize the popularity of each cluster
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/e8bf159a-b64c-4d5a-981a-d485ccbaeea9" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/e94f66b3-4c45-4a03-973f-f4f2908d1d31" alt="Image 2" width="45%"/>
</div>

- Visualize the images for top 10 most popular clusters

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/9deb25e3-d516-4248-ac55-2eb26fdb41bf" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/1b93b66e-fabc-40de-9fa7-f7b233e0cb68" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/1e5b6baa-3d09-4397-8346-24d947a634f6" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/10063b98-bc03-47c9-aa41-7b27f617ffc2" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/692219dd-cf95-4210-9139-2f44aa37049a" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/9002fec1-9862-4014-b41c-64842e70ac10" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/03d88901-8970-46bb-957b-fc7a0b18322c" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/56f143b8-e3fa-4db0-98db-dd5b3d421bb3" alt="Image 2" width="45%"/>
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/1f95ed72-81d1-4316-a9a2-1f2e0ca3c9cd" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/03f9157d-0648-4997-90c1-6096cc6916db" alt="Image 2" width="45%"/>
</div>

## No dictionary + Dimensionality reduction
##### Steps:
1. Text Preprocessing
   - Clean and prepare the text data
   - RAKE Keyword Extraction
2. Incorporate S-Bert and UMAP
   - Generate embedding useing SBERT - text2vec-large-chinese
   - Reduce dimensionality using UMAP
   - Find the optimal #clusters using Silhouette Method for
   - Do KMeans clustering
7. Visualize results

##### Findings
- Nice Silhouette score (A reasonable structure is found)
- The best number of clusters based on silhouette score is: 84

<div style="display: flex; justify-content: space-around;">
  <img src="https://github.com/user-attachments/assets/0c2038c8-ef40-48bf-9fed-e38f59b8dcc7" alt="Image 1" width="45%"/>
  <img src="https://github.com/user-attachments/assets/7dec6291-6aa5-4e18-b231-05aeba0ec84b" alt="Image 2" width="45%"/>
</div>


----------------------------------------------------------------------------------------------------------------------------
## Aug 5, 2024
### cloth-segment issues
- need to remove non cloth-focused images (e.g., posts of makeup/accessory/shoes)

### clustering -- find out the optimal number of cluster by silhouette method
![image](https://github.com/user-attachments/assets/caa34e4a-d857-438e-907d-3bf02f3cfddf)
![image](https://github.com/user-attachments/assets/0fd23eb4-f2fa-4b3d-8511-843c56038c94)
![image](https://github.com/user-attachments/assets/d21f3b39-532a-4c5e-896f-a7f5a4b52030)
![image](https://github.com/user-attachments/assets/663344d0-83ea-41a9-8f1e-f83ee1bb09b0)
![image](https://github.com/user-attachments/assets/14dd9560-6947-41eb-9f36-79324ff7eb81)



## July 30, 2024:
####  - added data_prep.ipynb
1. select 200 posters from 50w level posters
2. keep fashion-related posts only

#### - updated data.ipynb
1. visualize special cases of segmentation
2. sentiment analysis on post_comment_content
3. visualize sentiment results
4. add poster's numerical metrics

#### - updated label.ipynb
- visualize proportion and trend

#### - run classification.ipynb and regression.ipynb
- use sample of 300 posters

## Discussion:
1. model architecture: test embedding, vision embedding, numerical embedding --> add audio embedding?
2. heatmap
3. sales data?
4. Bass model
5. Survey? (BrandImageNet mode, LiuLiu 2020)
   
----------------------------------------------
### Video -> Images
1. Extract frames at 1/4, 2/4, and 3/4 of the video's duration
2. Save the extracted frames as images

![Screenshot 2024-07-25 at 13 23 04](https://github.com/user-attachments/assets/78f3144e-1710-4018-a3fc-05a33d8ee2bc)

### Image Segmentation
Original image + the mask -> processed image

![Screenshot 2024-07-25 at 13 23 45](https://github.com/user-attachments/assets/95a27c7e-d74c-43cd-a7f3-25db395a1669)

### Image Segmentation -- special cases
1. mask area too small

<img src="https://github.com/user-attachments/assets/4d276964-1aa6-4be3-a7a7-2c5b9bf5620e" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/d54785c1-f8c7-4974-8e31-2e0e78d152ad" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/a845abda-f0aa-421a-8c86-f127fd8fa929" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/634bcf5b-39d2-44a7-b5da-77d8153c6565" width="450" height="300" />

2. mask area too large

<img src="https://github.com/user-attachments/assets/491c96cb-1920-4490-986f-7537e70d8e76" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/81a9671a-9bdf-4810-9948-7f9fe6a58784" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/a818f392-8e06-4fa4-bd65-4dc1e97630e0" width="450" height="300" />
<img src="https://github.com/user-attachments/assets/abb80344-8286-4206-bb7f-4ef3995ade3f" width="450" height="300" />

### Image Clustering 
- K = 100
- Maybe better to perform image clustering specifically to segment the clothing, rather than focusing on the style or the entire human figure?
- cluster based on pose or style

![Screenshot 2024-07-25 at 13 27 21](https://github.com/user-attachments/assets/854b4f4b-50b3-4d89-b571-20d7aab92bfd)

### Text Preprocessing
1. Removing Stop Words 
2. Tokenization
3. Stemming and Lemmatization
4. Handling Special Characters
5. Translating Emojis
6. replace('1千', '1000').replace('1万', '10000’) 
7. Sentiment analysis on comments

### Sentiment analysis resutls of first 10 comments

<img src="https://github.com/user-attachments/assets/2f2045f4-e15e-45bc-8747-edf9e29ff3fb" width="450" height="300" />

##### Positive: score > 0.6
##### Negative: score < 0.4
##### Neutral: else

<img src="https://github.com/user-attachments/assets/0e12abbd-9e3a-446c-934a-57b2dfb4ff43" width="300" height="300" />

### Numerical metrics from posters
'粉丝数': 'fans_count',
'关注数': 'following_count',
'赞藏总量': 'total_likes',
'笔记数': 'posts_count'

### Metrics of Popularity

![Screenshot 2024-07-25 at 13 34 15](https://github.com/user-attachments/assets/5064e175-fc7a-4535-8920-fcc059bd65e1)

<img src="https://github.com/user-attachments/assets/cbddfa1a-ef96-4866-b29b-29bfa1d7ac97" width="450" height="300" />

![Screenshot 2024-07-25 at 13 33 59](https://github.com/user-attachments/assets/c4935660-b13f-428b-be33-f883e79c151a)

<img src="https://github.com/user-attachments/assets/d49948a4-16c8-4601-9468-31bd0687514d" width="450" height="300" />


### classification results
Test Accuracy: 60.00%

### regression results
Evaluation Loss: 0.00013176486892131254

