### 2.3.3 具体每个月的top5展示
[data_visual.ipynb](https://github.com/diandianyilin/fashion/blob/October/data_visual.ipynb)  


- 每个图代表一个月，分布是5*10张图片组合。5行代表top5，即每行代表同一个风格。每行10张图，即每个风格采样10张图片。


<p align="center">
    <img src="https://github.com/user-attachments/assets/20ee2ef0-89c5-4ef4-aff2-7e1fe109a5ed" width="800"/>
    <br>
    <strong>Fig.8.1, month_1_top5: 显瘦秋冬/可爱/秋冬韩系/女童/男生秋冬</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/fd3cd04b-cc74-4dab-a22f-326367e8c756" width="800"/>
    <br>
    <strong>Fig.8.2, month_2_top5: 秋冬韩系/可爱/男生秋冬/显瘦秋冬/裙子连衣裙</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/02f9f740-1c4c-4b4c-bfdd-440618f97d18" width="800"/>
    <br>
    <strong>Fig.8.3, month_3_top5: 日本/秋冬韩系/小个子显瘦/小个子显瘦女生/男生秋冬</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/9cec5917-3b66-47a4-bf60-cb241ef946fb" width="800"/>
    <br>
    <strong>Fig.8.4, month_4_top5: 秋冬韩系/男生秋冬/日本/香云纱汉服/甜妹裙子</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/44a0a7b0-1e2e-4806-a8c6-65be290c1270" width="800"/>
    <br>
    <strong>Fig.8.5, month_5_top5: 可爱/衬衫/男生秋冬/香云纱汉服/小个子显瘦女生</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/94890f18-3ff1-48d4-9828-d274f6884d39" width="800"/>
    <br>
    <strong>Fig.8.6, month_6_top5: 可爱/女生长裙/显瘦秋冬/裙子连衣裙/小个子显瘦女生</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/00d0835d-7a84-45df-8a4b-72b667ce66b9" width="800"/>
    <br>
    <strong>Fig.8.7, month_7_top5: 可爱/裙子温柔/裙子连衣裙/女生长裙/小个子显瘦</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/9bee925e-de72-449b-a923-40f6615a7ff3" width="800"/>
    <br>
    <strong>Fig.8.8, month_8_top5: 小个子希野逸儿/显瘦秋冬/裙子连衣裙/小个子显瘦/可爱</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/b247359f-31b9-4d7f-a96b-a12a64c8bfe5" width="800"/>
    <br>
    <strong>Fig.8.9, month_9_top5: 小个子显瘦/显瘦秋冬/小个子希野逸儿/可爱/秋冬韩系</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/dcbb6c22-39be-45c2-bb9c-3c94d0717e84" width="800"/>
    <br>
    <strong>Fig.8.10, month_10_top5: 显瘦秋冬/小个子显瘦/秋冬韩系/可爱/男生秋冬</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/7404514d-3b2d-4c8e-8483-8f592a0c0f8f" width="800"/>
    <br>
    <strong>Fig.8.11, month_11_top5: 显瘦秋冬/可爱/秋冬韩系/小个子显瘦/女生长裙</strong>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/7911f2ce-57e0-48dc-88a0-ae5304948917" width="800"/>
    <br>
    <strong>Fig.8.12, month_12_top5: 显瘦秋冬/可爱/女孩小个子微胖/小个子显瘦/秋冬韩系</strong>
</p>

- 结论：
    - 相比于之前的segment衣服结果，这次没有出现头和饰品占比过高的bad case情况(因为这次提前去掉了衣服小于5%的图)。
    - 每个类别可以看出明显规律，基本make sense。
