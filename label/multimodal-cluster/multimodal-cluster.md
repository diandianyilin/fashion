


# multimodal cluster


# 1. 处理步骤


1. 对于图片去掉其中black area 大于95%的bad case.
2. 对于文本，首先对于post的'post_content'和'post_tag'拼接在一起
    - 具体来说：进行使用[`jieba`]分词，使得句子变为一些key words。使用关键词提取技术[`RAKE`],得到这个句子中最重要的关键词。
3. 使用imagebind得到image和text的embedding向量，然后concatenate拼成一个向量。
    - 并行拼接：[text embedding, image embedding]
4. 进行cluster聚类。使用sihouette计算最佳聚类数目。可视化每个类型的结果，看看每个类中的效果是否make sense



# 2. 具体处理


## 2.1 image处理

首先segment衣服，并计算出每个衣服的占比全图的面积。根据面积的分布情况，和segment后的识别能力，得到threshold为5%。因此去掉其中black area占比超过95%的图片（即衣服占比太少＜5%的图片都去掉）。

对于剩下的图片进行人体segment

## 2.2 text处理


句子：'花卉连衣裙这样搭配真的好好看❤️ - 小红书,,05-17,,#白茶姐弟 #每日穿搭 #气质连衣裙 #连衣裙 #显瘦连衣裙'


0. 数据清洗：去掉语气词和无关词汇[`stopwords_cn.txt`]，去掉nan异常词汇，表情包转化[`emoji`]
    - 得到：'花卉连衣裙 搭配真的好好看(爱心)   白茶姐弟  每日穿搭  气质连衣裙  连衣裙  显瘦连衣裙 '
1. 首先使用[`jieba`]分词，使得句子变为一些key words。
    - 得到：'花卉 连衣裙   搭配 真的 好好看 ( 爱心 )  白茶 姐弟  每日 穿 搭  气质 连衣裙  连衣裙   显瘦 连衣裙'
2. 然后使用关键词提取技术[`RAKE`],得到这个句子中最重要的关键词。
    - 得到：'白茶 姐弟 每日 穿 搭 气质 连衣裙 连衣裙 显瘦 连衣裙'
3. 对这些关键词当作一个句子，直接进行embedding和cluster
    - 使用text2vec-large-chinese，进行embedding


上述细节见代码：[`data.ipynb`](https://github.com/dengxw66/Multimodal_MKT/blob/dxw_devlop/label/text-cluster/data.ipynb)



# 3. 聚类结果



## 3.1 sihouette轮廓法

- 可视化最佳聚类数目



## 3.2 可视化每个类型的结果

见：/data1/dxw_data/llm/Multimodal-MKT/label/multimodal-cluster/data_095.ipynb

## 2.3 可视化

- 下面的结果是使用silhouette得到的58类(暂拟定)，来做聚类得到的category


### 2.3.1 整体类别分布情况展示

<p align="center">
    <img src="image/proportion.png" width="800"/>
    <br>
    <strong>Fig.6, 每个月的所有category的proportion。没有出现明显过大或过低的异常分布情况。</strong>
</p>


<p align="center">
    <img src="image/time.png" width="800"/>
    <br>
    <strong>Fig.7, 全年各个风格持续时长。不同颜色的高度代表不同category。发现同一个风格最多持续出现3个月(有两处)</strong>
</p>



### 2.3.2 具体每个月的top5展示

- 每个图代表一个月，分布是5*10张图片组合。5行代表top5，即每行代表同一个风格。每行10张图，即每个风格采样10张图片。


<p align="center">
    <img src="image/top12/month_1_top5.png" width="800"/>
    <br>
    <strong>Fig.7, month_1_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_2_top5.png" width="800"/>
    <br>
    <strong>Fig.8, month_2_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_3_top5.png" width="800"/>
    <br>
    <strong>Fig.9, month_3_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_4_top5.png" width="800"/>
    <br>
    <strong>Fig.10, month_4_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_5_top5.png" width="800"/>
    <br>
    <strong>Fig.11, month_5_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_6_top5.png" width="800"/>
    <br>
    <strong>Fig.12, month_6_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_7_top5.png" width="800"/>
    <br>
    <strong>Fig.13, month_7_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_8_top5.png" width="800"/>
    <br>
    <strong>Fig.14, month_8_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_9_top5.png" width="800"/>
    <br>
    <strong>Fig.15, month_9_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_10_top5.png" width="800"/>
    <br>
    <strong>Fig.16, month_10_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_11_top5.png" width="800"/>
    <br>
    <strong>Fig.17, month_11_top5</strong>
</p>

<p align="center">
    <img src="image/top12/month_12_top5.png" width="800"/>
    <br>
    <strong>Fig.18, month_12_top5</strong>
</p>

- 结论：
    - 相比于之前的segment衣服结果，这次没有出现头和饰品占比过高的bad case情况(因为这次提前去掉了衣服小于6%的图)。
    - 每个类别可以看出明显规律，基本make sense。如果还需要进一步提高效果，可以考虑使用88等其他更大数目的silhouette极值点聚类。


















































