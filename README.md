# image_retrival　
本文整体上利用flask＋mysql搭建的，算法上主要是利用AlexNet网络提取图片的两个哈希码，长度分别为4096和48，短码用于检索回相似图像集，长码用于对相似结果集中图像进行排序，从而得到最终的搜索结果。
参考论文：
《Deep Learning of Binary Hash Codes for Fast Image Retrieval》