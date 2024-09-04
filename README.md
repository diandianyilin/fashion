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

![Screenshot 2024-09-03 at 20 07 21](https://github.com/user-attachments/assets/8bd1be1f-91f7-4fc1-9c20-b69efc0015bc)
![Screenshot 2024-09-03 at 20 07 42](https://github.com/user-attachments/assets/fe9eca3b-1579-4144-a626-06086c0be387)
#### Possible Conclusions:
##### Overfitting:  
The increase in validation loss while the training loss continues to decrease is a common sign of overfitting. This means that the model is starting to memorize the training data rather than generalizing to unseen data.
##### Early Stopping:  
The model might have achieved its best performance after Epoch 1 or 2. Continuing to train beyond this point could lead to overfitting.
#### Metrics Breakdown:
##### Accuracy: 0.9449  
High Accuracy: The model is correctly predicting a large proportion of the total instances. However, accuracy can be misleading, especially in imbalanced datasets.
##### Precision: 0.6518  
Moderate Precision: When the model predicts a positive class (e.g., fashion-related content), it is correct 65.18% of the time. This is a reasonable precision, but there's room for improvement.
##### Recall: 0.0978  
Low Recall: The model is identifying only 9.78% of the actual positive instances. This suggests that the model is missing many true positives, meaning it has a high number of false negatives.
##### F1 Score: 0.1700  
Low F1 Score: The F1 score, which balances precision and recall, is quite low. This indicates that the model is not performing well in identifying the positive class.

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
