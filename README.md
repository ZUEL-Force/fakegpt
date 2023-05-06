# fake_gpt3

这是一个尝试利用openai_api做点什么的小项目，仅用于学习和测试。

### web端gpt聊天

这个是尝试复刻一个openai官网式的聊天，主要是练手。

### 移动端gpt聊天

其实就是把web端打包成了安卓apk，和web端差不多。

### qq机器人

利用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp.git)控制qq，gpt生成回复。当然你还可以把ai作图和语音回复等也缝合进去。

### b站直播

gpt与弹幕互动，利用[语音合成](https://github.com/CjangCjengh/MoeGoe)把gpt的回复播出来。这里使用了[bilibili-api](https://github.com/Nemo2011/bilibili-api)，代码修改自[AI-Vtuber-chatglm](https://github.com/AliceNavigator/AI-Vtuber-chatglm)。


### 特别感谢：

在我们的项目中参考、修改或直接使用了以下项目的代码或api，在此提出感谢。如有侵权，请给我们提issue，我们会立刻处理。


[go-cqhttp](https://github.com/Mrs4s/go-cqhttp.git) go-cqhttp 兼容 OneBot-v11 绝大多数内容，并在其基础上做了一些扩展，详情请看 go-cqhttp 的文档。

[MoeGoe](https://github.com/CjangCjengh/MoeGoe) 语音合成模型的训练和推理都是使用的这位大佬的代码。

[bilibili-api](https://github.com/Nemo2011/bilibili-api) 这是一个用 Python 写的调用 Bilibili 各种 API 的库， 范围涵盖视频、音频、直播、动态、专栏、用户、番剧等。注意：使用此模块时请仅用于学习和测试，违规此模块许可证及此条注意事项而产生的后果自负。

[AI-Vtuber-chatglm](https://github.com/AliceNavigator/AI-Vtuber-chatglm) 本地部署chatglm生成并以语音回复你的bilibili直播弹幕。


这是我们第一次发布开源项目，说实话有很多没弄明白的地方。比如我们在项目中使用了其他作者的开源代码，但不知道我们怎样做才能符合他们的许可证规定。如果有哪些地方做的不对，还请各位大佬批评指正，我们一定会立刻修改。

## [MIT LICENSE](./LICENSE)
