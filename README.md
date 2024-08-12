# Multimodal_MKT

## text clustering
### Dictionary 1 - General
##### Input: topics0611.csv, poster_test_fashion_nlpclean.csv
##### Output: word_suffixes.csv, keyword_freq_dict1.csv, keyword_freq_by_month_dict1.csv
##### Steps: 
1. Extract common suffixes from the topics0611.csv file.
2. Use those suffixes to search for complete words in the poster_test_fashion_nlpclean.csv file.
3. Do textual data cleaning again.
4. Count overall frequency and by-month frequency.
 
### Dictionary 2 - Specific 
##### Inputs: topics0611.csv, poster_test_fashion_nlpclean.csv
##### Outputs: keyword_freq_dict2.csv, keyword_freq_by_month_dict2.csv
##### Steps:
1. Use topics0611.csv to do exact match with poster_test_fashion_nlpclean.csv.
2. Count overall frequency and by-month frequency.






## Aug 5, 2024
### cloth-segment issues
- need to remove non cloth-focused images (e.g., posts of makeup/accessory/shoes)

### clustering -- find out the optimal number of cluster by silhouette method
![image](https://github.com/user-attachments/assets/caa34e4a-d857-438e-907d-3bf02f3cfddf)
![image](https://github.com/user-attachments/assets/0fd23eb4-f2fa-4b3d-8511-843c56038c94)


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

