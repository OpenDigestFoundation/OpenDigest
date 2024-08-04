import util
import random
from pathlib import Path

def get_summary_from_abstract(abstract):

    prompt = f'''
    用中文简短的摘要他解决的问题，解决方法，实验结果：
    **输出格式**:
    解决的问题:
    解决方法:
    实验结果:
    {abstract}
    '''
    response = util.call_kimi_completions(prompt)
    return response


def output_review_from_file(pdf_path, style = "short"):
    # "Development/input/1706.03762v7.pdf"
    file_object = util.client_kimi.files.create(file=Path(pdf_path), purpose="file-extract")
    file_content = util.client_kimi.files.content(file_id=file_object.id).text
    
    history = [
        {"role": "system", 
        "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {
            "role": "system",
            "content": file_content,
        }
    ]
    def chat(query, history):
        history.append({
            "role": "user", 
            "content": query
        })
        completion = util.client_kimi.chat.completions.create(
            model="moonshot-v1-32k",
            messages=history,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        history.append({
            "role": "assistant",
            "content": result
        })
        return result
    
    summary = chat('''
    回答四个问题来总结这篇学术论文为四句话：

    如果这篇文章时提出了新方法，那就用如下的四个问题：
    这篇文章在解决什么问题？
    这篇文章提出了什么方法？
    这个方法跟已有工作比有什么进步？
    这篇文章对这个领域有什么潜在的未来影响？

    输出格式为文章段落
    ''', history)

    if style == "short": return summary
    
    related_work = chat('''
    这篇文章内提到的重点相关工作有哪些？
    输出格式：
    （人名，年份）工作名称： 工作内容简介
    ''', history)

    approach = chat('''
    这篇文章的核心方法是什么？ 请结合文章内的算法和公式进行解释
    ''', history)

    experiment = chat('''
    这篇文章的实验数据对比说明了什么结果？请列出具体数字和分析
    ''', history)

    impact = chat('''
    这篇文章对于这个领域可能的影响有哪些
    ''', history)

    return "**summary**: " + summary + "\n" + \
           "**related work**: " + related_work + "\n" + \
           "**approach**: " + approach + "\n" + \
           "**experiment**: " + experiment + "\n" + \
           "**impact**: " + impact
           
