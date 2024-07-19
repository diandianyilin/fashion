
# 多模态识别

# 1. 实验方案：

## 1.1 数据结构

1. 输入input：
    1. 图片和文本。
        - 图片：尽可能只截取衣服。
        - 文本：仅仅为辅助作用。
        - (不考虑音频。视频数据也当作图片数据处理)
    2. 其他信息：
        - 加入​​numerical information: post #like/#collect/#comment; poster 粉丝数/关注数/获赞总量/笔记数量/。sentiment analysis on comments
            - 本次实验使用的变量有3个：post_comments,post_like,post_collect
        - 输入的时间窗口定为2个月（1月1号-2月30号，1月2号到3月1号，1月3号到3月2号）

    - 训练用数据结构
        - 回归数据集：[`after2monthdata_20%.csv`](https://github.com/dengxw66/Multimodal_MKT/model/after2monthdata_20%.csv)，其中的["proportion"]为标签。是一个具体比例数值。
        - 分类数据集：[`after2monthdata_20%_with_trend.csv`](https://github.com/dengxw66/Multimodal_MKT/model/after2monthdata_20%_with_trend.csv)，其中的["trend"]为标签。是根据proportion占比值的不同数值分布3等分类，从高到底为1，0，-1，代表热度高，热度一般，完全没有热度。

2. 输出output：
    1. 预测具体数值比例。
        - 考虑到精度，不仅仅做了拟合，也做了分类任务。
    2. 预测时间窗口最后一天在两个月后的占比。（注意是那一整个月的占比）
    3. Label的计算只考虑图片类别，不考虑文本类别。

## 1.2 模型结构

<p align="center">
    <img src="pipleline2.png" width="600"/>
    <br>
    <strong>模型结构，添加numerical variables分支</strong>
</p>

过程：
1. 一次输入60天/2个月的数据，每一天的数据都是一批post（含有成对的image和text，以及numerical variables）
2. 每天的多模态数据都通过transformer的多个encoder模块，并做cross-attention多模态特征融合，然后将融合的特征与numerical variables的feature对齐拼接。
mlp就是将numerical_feature_dim的3也映射为1024大小，方便对齐image和text
3. 然后60天的数据送入一个时序长度为60的LSTM模型做时序融合，输出这60天的最后一天特征。(前59天的时序关系就融合到最后一天里面)
4. 最后使用mlp对最后一天的特征做预测或分类

关键问题：
- numerical variables为什么使用mlp？
    - 因为numerical variables变量很少，不用使用encoder提取特征了。所以使用常见的mlp做特征格式对齐即可。
- numerical variables为什么在cross-attention后，lstm前融合？
    - 因为cross-attention是图片和文本特征融合，这其中不涉及numerical variables。所以numerical variables是在多模态融合完成后，再一起送入时序融合步骤。
- numerical variable的拼接细节：
     - 文本嵌入向量（text_embeddings）：尺寸：(batch_size, sequence_length, text_embedding_dim)。在代码中，text_embedding_dim 为 1024
    - 视觉嵌入向量（vision_embeddings）：尺寸：(batch_size, sequence_length, vision_embedding_dim)。在代码中，vision_embedding_dim 为 1024
    - 数值嵌入向量（numerical_embeddings）：尺寸：(batch_size, sequence_length, numerical_feature_dim)。在代码中，numerical_feature_dim 为 3
    - mlp就是将numerical_feature_dim的3也映射为1024大小，方便对齐image和text。这样的好处是多模态和numerical特征权重均衡，充分表达了数量特征。


# 2. 实验步骤：

## 2.1 复现步骤


1. 数据处理逻辑，一共两步：
- 首先逐步运行：[`data.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/data.ipynb)。包含了视频切割，图片聚类，文本清洗等步骤。
- 然后逐步运行：[`label.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/label.ipynb)。负责制作分类数据集[`after2monthdata_20%.csv`](https://github.com/dengxw66/Multimodal_MKT/model/after2monthdata_20%.csv)和回归数据集[`after2monthdata_20%.csv`](https://github.com/dengxw66/Multimodal_MKT/model/after2monthdata_20%.csv)。


2. 训练代码,逐次运行文件即可。
    -  做分类任务：
        - 文件[`train_classification.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_classification.ipynb),使用image，text做label的热度3分类1/0/-1
        - 文件[`train_classification_num.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_classification_num.ipynb),使用image，text和numerical_variable做label的热度3分类1/0/-1
    - 做拟合任务：
        - 文件[`train_regression.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_regression.ipynb),使用image，text做label的占比具体值的预测回归。
        - 文件[`train_regression_num.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_regression.ipynb),使用image，text和numerical_variable做label的占比具体值的预测回归。

## 2.2 实验结果

1. 使用总数据的0.2%实验：
    - 做分类任务：
        - 见文件：[`train_classification.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_classification.ipynb), 测试集Loss: 0.000458289182157993
        - 见文件：[`train_classification_num.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_classification_num.ipynb), 测试集Loss: 0.00033924097693827093
    - 做拟合任务：
        - 见文件：[`train_regression.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_regression.ipynb),测试集精度达到100%
        - 见文件：[`train_regression_num.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/train_regression_num.ipynb)，测试集精度达到100%
2. 更大数据规模(总数据的1%)实验：见文件：[`tran_test.ipynb`](https://github.com/dengxw66/Multimodal_MKT/model/tran_test.ipynb)，测试集精度达到94%

- 结论：在小规模数据集上初步成功。可以尝试更大规模数据集了。



# 3. 后续改进/下周计划

1）使用分割segment衣服的图片，而不是全人体。

2）上述所有方案落实后，开始尝试更大规模数据集训练测试。























