# tfashion: A Fashion-Related Text Classification Model

[tfashion5.ipynb](https://github.com/diandianyilin/fashion/blob/October/tfashion5.ipynb)  
The `tfashion` model is a **binary text classifier** designed to identify **fashion-related words** in Chinese social media posts. It leverages a **pre-trained SentenceTransformer model** (`text2vec-large-chinese`) to generate word embeddings and a **ResNet-based binary classifier** for classification.

## Overview

Fashion trends and keywords play a crucial role in influencing consumer behavior, especially in social media contexts. The `tfashion` model was developed to address the need for identifying **fashion-related terms** within unstructured text. By combining a **SentenceTransformer** for embedding generation and a **ResNet-based classifier** for word-level predictions, this model can effectively filter out non-fashion-related content, leaving only relevant keywords.

## Key Features
- **Pre-trained SentenceTransformer embeddings**: Uses `text2vec-large-chinese` to convert text into embeddings.
- **ResNet-based binary classifier**: Built on top of the `ResNet18` architecture to classify each word as either fashion-related or not.
- **Stopword and single-character removal**: Enhances classification accuracy by removing irrelevant words.
- **Token-level classification**: Operates at the word level rather than classifying entire sentences or posts.


## Dataset Preparation

The dataset contains two categories:
- **Fashion-related samples (positive)**: Extracted from labeled social media posts.[topics_filtered.csv](https://github.com/diandianyilin/fashion/blob/main/topics_filtered.csv)
  - remove single Chinese characters and single English letters
  - remove certian noninformative fashion words: e.g., '穿搭', 'OOTD', 'ootd', 'Ootd', '日常', '每日', '安利', '种草', '喜欢', '真的'
- **Non-fashion-related samples (negative)**: Extracted from general Chinese Wikipedia text dumps.[non_fashion_texts](https://github.com/diandianyilin/fashion/tree/main/non_fashion_texts)

### Imbalance Handling
- The initial dataset was imbalanced:
  - **Fashion-related samples**: 43,127
  - **Non-fashion-related samples**: 73,084
- To address this imbalance, the non-fashion-related samples were **downsampled** to match the number of fashion-related samples, resulting in **balanced datasets**:
  - **Downsampled Non-fashion-related samples**: 43,127

## Model Training

### Step 1: Data Preparation
1. **Read positive and negative samples** from their respective files.
2. **Combine the datasets** into a single DataFrame.
3. **Downsample the non-fashion-related samples** to balance the dataset.

### Step 2: Word Embedding Generation
1. Use the pre-trained **`text2vec-large-chinese`** model to generate **1024-dimensional embeddings** for each word in the dataset.
2. Convert the word embeddings and labels into **PyTorch tensors**.

### Step 3: Train-Test Split
1. The dataset is split into **80% training** and **20% validation** sets.
2. Data is loaded into **PyTorch DataLoaders** for efficient batch processing.

### Step 4: Model Definition
1. **ResNet18-based binary classifier**: A ResNet architecture is adapted for binary classification by modifying the fully connected layers to predict one of two classes (fashion-related or not).
2. The model is trained using the **Adam optimizer** and **cross-entropy loss**.

### Step 5: Training and Validation
1. The model is trained for 5 epochs, with validation after each epoch.
2. Performance is measured using **accuracy**, **precision**, **recall**, and **F1 score**.

### Training Results:
- **Training and Validation Results**:

| **Epoch** | **Train Loss** | **Val Loss** | **Accuracy** | **Precision** | **Recall** | **F1 Score** |
|:---------:|:--------------:|:------------:|:------------:|:-------------:|:----------:|:------------:|
| 1         | 0.0910         | 0.0593       | 0.9760       | 0.9084        | 0.9309     | 0.9195       |
| 2         | 0.0553         | 0.0553       | 0.9770       | 0.9614        | 0.8789     | 0.9183       |
| 3         | 0.0417         | 0.0489       | 0.9801       | 0.9152        | 0.9530     | 0.9337       |
| 4         | 0.0325         | 0.0467       | 0.9827       | 0.9369        | 0.9462     | 0.9415       |
| 5         | 0.0262         | 0.0464       | 0.9827       | 0.9568        | 0.9244     | 0.9403       |
| **Final** |                |              | 0.9827       | 0.9568        | 0.9244     | 0.9403       |


The training and validation results for each epoch are presented, with performance metrics such as precision, recall, and F1 score showing consistent improvements across the epochs.


## Model Inference: Classifying Fashion-related Text

### Step 1: Preprocessing
1. **Tokenize** the `post_text` content into individual words using **Jieba**.
2. Remove **stopwords** from the tokens using a custom stopwords list [stopwords_cn.txt](https://github.com/diandianyilin/fashion/blob/main/stopwords_cn.txt).
3. Remove any **single-character tokens**.

### Step 2: Word Embedding and Classification
1. Pass each word through the **SentenceTransformer** model to generate embeddings.
2. Classify each word using the **ResNet-based binary classifier** (`tfashion`).
3. Retain words that are classified as fashion-related.

### Example Output:

| **Example** | **Original post_text** | **Filtered Keywords** |
|:-----------:|:-----------------------|:----------------------|
| 12997       | 尊嘟很爱redexclamationmark她们说这是富贵小姐姐穿搭尝试一个新look温柔气质大姐姐富家千金穿搭秋冬温柔慵懒风毛衣慵懒风穿搭高级感穿搭 | ['富贵', '小姐姐', '尝试', '温柔', '气质', '姐姐', '富家', '千金', '秋冬', '慵懒', '毛衣', '风穿', '高级', '感穿'] |
| 11585       | 好爱这种温柔白月光的感觉一定要试试仙气的裙子新中式穿搭民国风温柔连衣裙国风针织新中式套装 | ['温柔', '白月光', '感觉', '试试', '仙气', '裙子', '中式', '民国', '连衣裙', '国风', '针织', '套装'] |
| 11226       | 我先成为我自己微胖女孩微胖穿搭 | ['微胖', '女孩'] |
| 13552       | redapple型跟着模特穿keycapkeycap复古百褶裙太好穿身高cm体重斤斤小腿围cm大腿cm腰围cm肚围cmredapple型身材我太爱这件短裙了前几年都不敢尝试百褶裙没想到今年穿了感觉还不错哈哈哈哈哈应该是材质的问题厚的材质质感好苹果型身材苹果型小个子穿搭短裙穿搭短裙格子裙百褶裙百褶裙这么搭百褶裙穿搭格子百褶裙复古百褶裙复古格子半裙秋季穿搭秋季新款跟着模特学穿搭美拉德穿搭是什么苹果型身材穿搭小个子苹果型身材苹果型身材穿搭指南苹果型身材显瘦穿搭苹果型身材微胖穿搭微苹果型身材针织上衣舒服针织衫这么搭百搭针织上衣早秋必备针织衫 | ['redapple', '跟着', '模特', '复古', '百褶裙', '太好', '身高', '体重', '斤斤', '小腿', '大腿', '腰围', '肚围', '身材', '我太爱', '这件', '短裙', '几年', '尝试', '没想到', '感觉', '不错', '哈哈哈', '材质', '质感', '苹果', '小个子', '格子裙', '格子', '半裙', '秋季', '新款', '学穿', '拉德', '指南', '显瘦', '微胖', '搭微', '针织', '上衣', '舒服', '针织衫', '搭百搭', '早秋', '必备'] |
| 100         | 这件毛衣搭红围巾真的氛围感绝了真的太好看啦质感超棒软软糯糯的外面再搭个大衣妥妥韩剧女主疯狂爱上大学生穿搭大衣穿搭毛衣日常穿搭气质穿搭秋冬穿搭小个子穿搭秋冬毛衣 | ['这件', '毛衣', '搭红', '围巾', '真的', '氛围', '感绝', '好看', '质感', '超棒', '软软', '外面', '搭个', '大衣', '韩剧', '女主', '疯狂', '爱上', '大学生', '日常', '气质', '秋冬', '小个子'] |
| 9914        | 万圣节穿这样还了得穿了店里的新品拍一下照万圣节每日穿搭哥特 | ['万圣节', '店里', '新品', '每日', '哥特'] |
| 15089       | 这种身材巨巨巨好穿doubleexclamationmark微胖女生大胆穿冬天真的很好穿啊胯宽腿粗梨形身材微胖女孩穿搭微胖穿搭日常穿搭梨形身材穿搭梨形微胖梨形身材大粗腿梨形穿搭梨形胯宽腿粗穿搭微胖秋冬冬季穿搭微胖女生冬季穿搭 | ['身材', '巨巨', '巨好', '微胖', '女生', '大胆', '冬天', '真的', '梨形', '女孩', '日常', '秋冬', '冬季'] |
| 2309        | 基础Tee的一衣多穿法则夏天少不了的基础T恤怎么穿才能让他更有花样性所以我选择了三条不同类型的裤子进行搭配不同裤型的搭配也能让基础tee发挥它的可玩性今天穿什么香ootd每日穿搭男生穿搭开春穿搭基础短袖osmosismocuishleESOTERICInexistence存世GaforReal | ['基础', 'Tee', '一衣', '法则', '夏天', '少不了', 'T恤', '花样', '选择', '类型', '裤子', '搭配', '裤型', 'tee', '发挥', '可玩性', 'ootd', '每日', '男生', '开春', '短袖', 'GaforReal'] |
| 4101        | 只美拉德包包stuffedflatbread𖧧复古棕色百搭mate大容量棕色系mediumdarkskintone滴包包撞色巧克力包包chocolatebar羊羔毛包包ewe牛仔刺绣拼接棕色包包sewingneedle哭喊中心复古格纹帆布包burrito波士顿包型复古腋下包meatonbone包包偏爱小众包小众包包大学生上课包包腋下包帆布包美拉德棕色包包复古包包秋冬百搭包包通勤包包包包分享宝宝辅食包包不重样大容量包包 | ['只美', '拉德', '包包', '复古', '棕色', '百搭', 'mate', '大容量', '撞色', '巧克力', 'chocolatebar', '羊羔', '牛仔', '刺绣', '拼接', 'sewingneedle', '中心', '格纹', '帆布包', '包型', '腋下', 'meatonbone', '偏爱', '小众', '包小众', '大学生', '上课', '秋冬', '通勤', '分享', '宝宝', '辅食', '重样'] |
| 4394        | 攒了一个夏天的粉色growingheart我是一个爱穿粉色系的中年妇女ootd每日穿搭日常穿搭每日穿搭粉色系粉色少女心 | ['夏天', '粉色', 'growingheart', '中年妇女', 'ootd', '每日', '日常', '少女'] |


For more examples, see [tfashion5.ipynb](https://github.com/diandianyilin/fashion/blob/October/tfashion5.ipynb)  
