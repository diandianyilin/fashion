# tfashion - A model to identify fashion-related words
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

![Screenshot 2024-09-02 at 15 04 43](https://github.com/user-attachments/assets/eccae477-14db-4121-a828-01372b9a18cc)
![Screenshot 2024-09-02 at 15 05 20](https://github.com/user-attachments/assets/3beac766-70cb-499d-8f89-19049e5da7cb)

## Step 5. Apply the model
- prepare post data
  - input: poster_test_fashion_nlpclean.csv
  - Combine 'post_title' and 'post_content' into 'post_text'
  - Clean and Tokenize 'post_text'
- Filter Non-Fashion Words Using the Model
- output: post_filtered.csv

### Text before filtering:  
1. <span style="font-size:9px">球衣穿搭 ｜ 曼联在新疆喀什 . #球衣穿搭 #blokecore #曼联 #喀什 #喀什古城</p>
2. <p style="font-size:9px">国民初恋裴秀智牛仔裤配衬衫，韩系松弛感绝 裴姐不愧是南韩国民初恋，气质超绝！美得毫不费力，穿着简简单单的衬衫和牛仔裤真的好像在拍韩剧，最后再搭上披肩增加层次感，水洗蓝小香风设计感牛仔裤➕质感好的衬衫跟着裴秀智穿这种松弛感，同事说我上班穿得像去拍韩剧#裴秀智#韩系穿搭 #衬衫 #披肩 #韩女 #missa  #女明星穿搭 #女明星私服 #不费力气的穿搭 #简约穿搭 #小香风牛仔裤 #ins博主穿搭 #松弛感 #跟着明星学穿搭 #牛仔裤 #复古牛仔裤 #初恋#气质穿搭</p>
3.  听劝，力量训练才能打造出紧致线条 自从我摆脱白幼瘦后，真的有点开挂#健身女孩 #健身穿搭 #撸铁女孩 #力量训练 #臀腿训练 #好看好穿健身裤 #臀部塑形 #Ootd

### Text after filtering:  
1.  古城
2.  说
3.  NA
