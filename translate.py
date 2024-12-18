from flask import Flask, request, jsonify, abort
from openai import OpenAI

# 设置 OpenAI API 密钥
client = OpenAI(
    # OpenAI 官方的 key 测试的时候用超量了，买了个 第三方服务的 key
    api_key='sk-6J5mkJOO0t5S7PrmBfBe6e97B1774eC2B735C2AeAbAe9f6d',
    base_url="https://dzqc.link/v1"
)

# 初始化 Flask 应用
app = Flask(__name__)

# 预定义有效的 input_type 选项
valid_input_types = ["university", "major", "description", "city", "rank", "admission_requirements",
                     "scholarship", "work", "course_content", "alumni", "policies"]

# 根据输入文本类型创建提示模板
def create_prompt(input_text: str, input_type: str, output_lang: str) -> str:
    # 创建用于翻译的 Prompt，保留专有名词，翻译成指定语言，默认中文
    prompts = {
        "university": f"请将以下大学名称翻译成'{output_lang}': '{input_text}'",
        "major": f"请将以下专业名称翻译成'{output_lang}': '{input_text}'",
        "description": f"请将以下专业描述翻译成简洁准确带有一定解释的'{output_lang}': '{input_text}'",
        "city": f"请将以下大学所在的城市翻译成'{output_lang}': '{input_text}'",
        "rank": f"请将以下大学排名翻译成'{output_lang}'并进行扩充，"
                f"包括排名、学生评论和教师简介，以帮助学生进行择校: '{input_text}'",
        "admission_requirements": f"请将以下大学相关的入学要求翻译成'{output_lang}'并进行扩充，"
                                  f"包括申请指南、GPA 要求、标准化考试成绩"
                                  f"（例如 SAT、TOEFL、IELTS）和先决条件: '{input_text}'",
        "scholarship": f"请将以下大学相关的奖学金信息翻译成'{output_lang}'并进行扩充，"
                       f"包括申请资格标准: '{input_text}'",
        "work": f"请将以下大学-专业相关的未来职业发展翻译成'{output_lang}'并进行扩充，"
                f"包括不同的方向和就业情况: '{input_text}'",
        "course_content": f"请将以下大学-专业相关的课程描述翻译成'{output_lang}'并进行扩充，"
                          f"包括各个课程内容、学习成果和特定课程的先决条件: '{input_text}'",
        "alumni": f"请将以下大学相关的校友信息翻译成'{output_lang}'并进行扩充，"
                    f"包括杰出校友简介及其职业成就: '{input_text}'",
        "policies": f"请将以下大学相关的政策信息翻译成'{output_lang}'并进行扩充，"
                    f"包括针对外国学生的学术政策、评分制度和重要的大学规定: '{input_text}'",
    }
    return prompts.get(input_type, f"请翻译以下文本: '{input_text}'")

# 调用 OpenAI API 进行翻译
def translate_with_gpt(prompt: str) -> str:
    try:
        # 使用新的 ChatCompletion API
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # 或者其他支持的模型
        messages=[
            {"role": "system", "content": "你是一个拥有深厚留学背景，了解牛剑及世界前100大学的学业规划及申请、"
                                          "个人职业发展咨询、国内外落户服务的技术翻译助手，旨在成为每个家庭教育国际化的播种者。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        abort(500, description=f"翻译失败: {str(e)}")


# 调用 GPT 自动生成 prompt
def generate_prompt_with_gpt(input_text: str, input_type: str, output_lang: str) -> str:
    try:
        # 使用 GPT 来生成合适的翻译 prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个拥有深厚留学背景，了解牛剑及世界前100大学的学业规划及申请、"
                                          "个人职业发展咨询、国内外落户服务的技术翻译助手，旨在成为每个家庭教育国际化的播种者。"},
                {"role": "user", "content": f"生成一个合适的翻译提示，用于将 '{input_text}' 翻译成'{output_lang}'并进行扩充，要求含义尽量贴近 '{input_type}' 的意思。"}
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        abort(500, description=f"无法生成 prompt: {str(e)}")

# 翻译 API 路由
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()

    # 输入数据验证
    if 'input_text' not in data or 'input_type' not in data:
        return jsonify({"error": "缺少必需参数 input_text 或 input_type"}), 400

    input_text = data['input_text']
    input_type = data['input_type']
    output_lang = data['output_lang'] if data['output_lang'] != "" else "Chinese"

    # 验证 input_text 是否为空
    if not input_text.strip():
        return jsonify({"error": "input_text 不能为空"}), 400

    # 验证 input_type 是否有效
    if input_type in valid_input_types:
        # 创建 Prompt
        prompt = create_prompt(input_text, input_type, output_lang)
    else:
        # 如果 input_type 无效，调用 GPT 自动生成 Prompt
        prompt = generate_prompt_with_gpt(input_text, input_type, output_lang)

    if not prompt:
        return jsonify({"error": f"无法为 input_type '{input_type}' 创建 Prompt"}), 400

    # 调用 GPT 进行翻译
    translation = translate_with_gpt(prompt)
    print(prompt)

    # 如果是 curl 调接口，需要转一下编码格式，否则中文会显示不出来
    return jsonify({
    "input_text": input_text,
    "input_type": input_type,
    "output_lang": output_lang,
    "translation": translation
}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# HTTP 错误处理器
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": str(error)}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
