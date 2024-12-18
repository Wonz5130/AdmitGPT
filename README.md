## ApplyEduTranslateGPT

一个针对留学申请的翻译 GPT，可以灵活准确翻译留学相关问题，例如：大学名 or 专业名 or 专业描述等，并给出相应答案。

## 需求分析

### 翻译语言

默认翻译成中文，因为针对的是国内留学者，也支持翻译成其他语言，输入参数里可自定义

### 定义 prompt

主要针对翻译写合适的 prompt
- 简单的名词，比如大学名、专业、城市，可以直接就是翻译。
- 复杂的名词，比如专业描述、以及自己想到的入学要求、奖学金信息、未来职业发展、专业相关的课程、校友信息、政策信息等，需要 GPT 进行扩充。
- 还有没列举到的名词，这时候需要 GPT 自己生成合适的 prompt。

### 参数定义

- input_text：输入要翻译的文本
- input_type：输入文本的类型，提前定义了一些类型。如果在预定义类型里，运行我定义的 prompt，如果遇到没有定义的类型，运行 GPT 自己生成的 prompt
- output_lang：要翻译成的语言

### 请求接口

```zsh
curl -X POST http://127.0.0.1:5000/translate \
-H "Content-Type: application/json" \
-d '{"input_text": "peking university", "input_type": "university", "output_lang": "Chinese"}'
```

## 测试 case

### 已经定义的翻译名词

- university
  - ![university](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162233739.png)
- major
  - ![major](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162233215.png)
- description
  - ![description](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162234626.png)
- city
  - ![city](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162235198.png)
- rank
  - ![rank](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410170939651.png)
- admission_requirements
  - ![admission_requirements](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162235274.png)
- scholarship
  - ![scholarship](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410170937500.png)
- work
  - ![work](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162236575.png)
- course_content
  - ![course_content](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162236672.png)
- alumni
  - ![alumni](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162236808.png)
- policies
  - ![policies](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162237752.png)

### 没有定义过的翻译名词

例如：cost学费

![cost](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162238827.png)

### 400

- 缺少必需参数 input_text 或 input_type
  - ![input_lost](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162243950.png)
- input_text 为空
  - ![input_text_none](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162242964.png)

- 默认翻译成中文，因为针对的是国内留学者，也支持翻译成其他语言，输入参数里可自定义
  - ![default_chinese](https://raw.githubusercontent.com/Wonz5130/My-Private-ImgHost/master/img/202410162244316.png)

### case汇总

```json
{
    "input_text": "北京大学",
    "input_type": "university",
    "output_lang": "English"
}

{
    "input_text": "Computer Science",
    "input_type": "major",
    "output_lang": ""
}

{
    "input_text": "Computer Science",
    "input_type": "description",
    "output_lang": ""
}

{
    "input_text": "University College London",
    "input_type": "city",
    "output_lang": ""
}

{
    "input_text": "University College London",
    "input_type": "rank",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London",
    "input_type": "admission_requirements",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London",
    "input_type": "scholarship",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London-Computer Science",
    "input_type": "work",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London-Computer Science",
    "input_type": "course_content",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London",
    "input_type": "alumni",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London",
    "input_type": "policies",
    "output_lang": "Chinese"
}

{
    "input_text": "University College London",
    "input_type": "cost",
    "output_lang": "English"
}
```



## 遇到的问题

### OpenAI Python 库升级导致原来的 API 不能用

遇到报错：

```commandline
"error": "500 Internal Server Error: \u7ffb\u8bd1\u5931\u8d25: \n\nYou tried to access openai.Completion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.\n\nYou can run openai migrate to automatically upgrade your codebase to use the 1.0.0 interface. \n\nAlternatively, you can pin your installation to the old version, e.g. pip install openai==0.28\n\nA detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742\n
```

经过查资料发现是 OpenAI Python 库升级之后，API 全重写了。

解决

1. 升级 OpenAI 库版本

```zsh
pip install --upgrade openai
```

2. 检查版本号，确保>=1.0.0

```zsh
pip3 show openai 
```

目前版本是：

```commandline
Name: openai
Version: 1.51.2
Summary: The official Python library for the openai API
Home-page: https://github.com/openai/openai-python
Author: 
Author-email: OpenAI <support@openai.com>
License: 
Location: /opt/homebrew/lib/python3.11/site-packages
Requires: anyio, distro, httpx, jiter, pydantic, sniffio, tqdm, typing-extensions
Required-by: 
```

3. 运行 OpenAI 官方迁移工具

```zsh
openai migrate
```

执行完之后，会自动将用到的老版本的 API 调用替换为兼容 openai>=1.0.0 的新 API。

## 参考资料

- OpenAI 官方 API 文档：https://github.com/openai/openai-python/blob/main/api.md
- OpenAI 迁移指南：https://github.com/openai/openai-python/discussions/742