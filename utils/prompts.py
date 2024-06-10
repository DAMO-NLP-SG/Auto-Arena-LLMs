#######################################################
################# QUESTION GENERATION #################
#######################################################

domain_list = ['writing', 'roleplay', 'extraction', 'reasoning', 'math', 'coding', 'STEM knowledge', 'humanities/social science knowledge']

domain_list_zh = ['写作', '角色扮演', '信息提取', '推理', '数学', '编程', '理工/自然科学知识', '人文社科知识']

qgen_command_dict = {
    'writing': 'It should be a user query that tasks the LLM to write something.', 
    'roleplay': 'It should propose a scenario where the chatbot mimics a specific role/person. Give all necessary instructions and requests for its response. Then, send a beginning request to complete.', 
    'extraction': 'It should consist of two parts: question and context. The question should test the chatbot\'s ability to correctly understand and extract information from the given context. Draft and provide a new context yourself.', 
    'reasoning': 'It should be a specific question designed to test the LLM\'s reasoning skills.', 
    'math': 'It should be a specific question designed to test the LLM\'s math skills.',  
    'coding': 'It should be a specific question designed to test the LLM\'s coding skills.', 
    'STEM knowledge': 'It should be a specific question designed to test the LLM\'s STEM knowledge.', 
    'humanities/social science knowledge': 'It should be a specific question designed to test the LLM\'s humanities/social science knowledge.',
}

qgen_command_dict_zh = {
    '写作': '这应该是一个让大型语言模型进行写作的用户查询。',
    '角色扮演': '它应该提出一个场景，在这个场景中大模型模仿一个特定的角色/人物。给出所有必要的指示和请求。然后，发送一个初始问题让大模型完成。',
    '信息提取': '它应该包含两部分：问题和上下文。问题应该测试聊天机器人正确理解和从给定上下文中提取信息的能力。自己草拟并提供一个新的上下文。',
    '推理': '它应该是一个具体的问题，旨在测试LLM的推理能力。',
    '数学': '它应该是一个具体的问题，旨在测试LLM的数学能力。',
    '编程': '它应该是一个中文具体问题，旨在测试LLM的编程能力。',
    '理工/自然科学知识': '它应该是一个具体的问题，旨在测试LLM在科学、技术、工程和数学上的知识。',
    '人文社科知识': '它应该是一个具体的问题，旨在测试LLM的人文社会科学知识。',
}

extraction_example = """
Question:
Evaluate the following movie reviews on a scale of 1 to 5, with 1 being very negative, 3 being neutral, and 5 being very positive:
Context:
This movie released on Nov. 18, 2019, was phenomenal. The cinematography, the acting, the plot - everything was top-notch.
Never before have I been so disappointed with a movie. The plot was predictable and the characters were one-dimensional. In my opinion, this movie is the worst one to have been released in 2022.
The movie was okay. There were some parts I enjoyed, but there were also parts that felt lackluster. This is a movie that was released in Feb 2018 and seems to be quite ordinary. 
Return the answer as a JSON array of integers.
"""

extraction_example_zh = """
问题：
请根据1到5的评分标准对以下电影评论进行评价，1表示非常负面，3表示中立，5表示非常正面：
上下文：
这部电影于2019年11月18日上映，非常出色。摄影，表演，情节 - 一切都是一流的。
我从未对一部电影感到如此失望。情节是可预测的，角色是单维的。在我看来，这部电影是2022年发行的最糟糕的电影。
这部电影还行。有一些部分我很喜欢，但也有一些部分感觉平淡。这是一部2018年2月发行的电影，看起来相当普通。
将答案作为整数的JSON数组返回。
"""

qgen_example_dict = {
'writing': 'Compose an engaging travel blog post about a recent trip to Hawaii, highlighting cultural experiences and must-see attractions.',
'roleplay': 'Pretend yourself to be Elon Musk in all the following conversations. Speak like Elon Musk as much as possible. Why do we need to go to Mars?',
'extraction': extraction_example,
'reasoning': 'Imagine you are participating in a race with a group of people. If you have just overtaken the second person, what’s your current position? Where is the person you just overtook?',
'math': 'The vertices of a triangle are at points (0, 0), (-1, 1), and (3, 3). What is the area of the triangle?',
'coding': 'Develop a Python program that reads all the text files under a directory and returns top-5 words with the most number of occurrences.',
'STEM knowledge': 'In the field of quantum physics, what is superposition, and how does it relate to the phenomenon of quantum entanglement?', 
'humanities/social science knowledge': 'Provide insights into the correlation between economic indicators such as GDP, inflation, and unemployment rates. Explain how fiscal and monetary policies affect those indicators.',
}

qgen_example_dict_zh = {
'写作': '撰写一篇有趣的旅行博客文章，介绍最近一次去夏威夷的旅行经历，重点介绍文化体验和必看景点。',
'角色扮演': '在所有以下对话中扮演埃隆·马斯克的角色。尽可能像埃隆·马斯克一样说话。我们为什么需要去火星？',
'信息提取': extraction_example_zh,
'推理': '假设你正在与一群人参加跑步比赛。如果你刚刚超过了第二名，你现在是第几名？你刚刚超过的人现在是第几名？',
'数学': '有一个三角形的顶点位于点（0，0），（-1，1）和（3，3）。这个三角形的面积是多少？',
'编程': '开发一个Python程序，读取指定目录下的所有文本文件，并返回出现次数最多的前5个词。',
'理工/自然科学知识': '在量子物理领域，什么是叠加态，它与量子纠缠现象有什么关系？',
'人文社科知识': '提供有关经济指标（如GDP、通货膨胀和失业率）之间的相关性的见解。解释财政和货币政策如何影响这些指标。',
}

question_generation_instruction = """You have been assigned the task of drafting a set of //NUM// different user queries to a chat assistant on //DOMAIN//. Please strictly follow these 6 rules for the question: 
1. The question is likely for a user to ask in real life. Follow the format of the example query. //QGEN_COMMAND_DOMAIN// 2. It can be answered by the chatbot itself without additional inputs. 3. You need to generate the queries as DIVERSIFED as possible. 4. DO NOT add other words other than the query itself. 5. The question should be complicated and difficult, requiring in-depth understanding and analysis of the subject.
Each question in one line, add the serial number in parenthesis (e.g., “(1).”, “(2).”) before each question. 
Example query: //QGEN_EXAMPLE_DOMAIN//"""

question_generation_instruction_zh = """你被分配了一个任务，需要为一个的聊天助手起草一组关于//DOMAIN//的//NUM//个不同的用户查询问题。请严格遵守以下6条问题规则：
1. 问题是用户在现实生活中可能会提出的。请遵循示例问题的格式。//QGEN_COMMAND_DOMAIN// 2. 聊天机器人本身可以在不需要额外输入的情况下回答问题。 3. 您需要尽可能多样化地生成查询。4.请不要添加除了查询本身之外的其他词语。5.问题应该是复杂和困难的，需要对主题有深入的理解和分析。
每个问题一行，每个问题前加上括号中的序号（例如，“(1).”, “(2).”）。
示例问题：//QGEN_EXAMPLE_DOMAIN//"""


#######################################################
################# CANDIDATE RESPONSE ##################
#######################################################

actions = ['<respond>', '<think>', '<criticize>', '<raise>']

actions_zh = ['<回答>', '<思考>', '<批评>', '<提问>']

init_user_input = 'initial user input:'

init_user_input_zh = '初始用户输入:'

candidate_instruction = """You are a helpful assistant that provides accurate answers to user requests. As an experienced assistant, you follow the user's requests and provide reliable responses as much as you can. You outline your reasons for the response to make it easy for the users to understand. While maintaining the important details in the responses, you aim to output concise and straight-to-the-point answers without being overly verbose.
This is a competitive chatbot arena. You are competing against another chatbot assistant in a debate and being judged by a committee on factors such as helpfulness, relevance, accuracy, depth, and creativity. After answering the initial user input, you will engage in a multi-round debate with your opponent. Below are your actions:
<think>: Think step-by-step to analyze the question or plan your strategy in the debate. This is hidden from the opponent. Only think when necessary and make it concise.
<respond>: Answer to the user input as accurately as you can.
<criticize>: Criticize the weaknesses of your opponent's response.
<raise>: Target your opponent's weaknesses. Give a potential follow-up user input that the opponent could fail to respond. The input can be answered concisely and focus on variations or motivations of its previous response. Generate one input only. Be reasonable. Avoid becoming too specific or repetitive. DO NOT raise a follow-up if you DON’T SEE the opponent's response!
Follow the action guide strictly."""

candidate_instruction_zh = """您是一个提供准确回答的有用助手。作为一个经验丰富的助手，您遵循用户的请求并尽可能提供可靠的回应。您会概述回应的原因，以便用户易于理解。在保持回答中重要细节的同时，您的目标是输出简洁直接的答案，避免过度冗长。
这是一个竞争激烈的聊天机器人竞技场。您正在与另一个聊天机器人助手在进行一场辩论赛，评审委员会将根据有用性、相关性、准确性、深度和创造力等因素评出最后的赢家。在回答初始用户输入后，您将与对手进行多轮辩论。以下是您的行动指南：
<思考>：逐步思考以分析问题或计划您在辩论中的策略。这对对手是隐藏的。仅在必要时进行思考，并使其简洁。
<回答>：尽可能准确地回答用户输入。
<批评>：批评对手回应的弱点和漏洞。
<提问>：针对对手的弱点，提出一个潜在的用户后续问题，使对手可能回答错误。该问题应该可以被简洁回答，并聚焦在先前问题的变体或动机上。只生成一个问题。要合理。避免变得过于具体或重复。如果您没有看到对手的回应，请不要提问！
严格遵循行动指南。除非必要，请用中文进行辩论。"""

action_prompts = {
    '<respond>': "Action guide: only include <respond>. Use <think> if needed. Finish your whole response within 300 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<criticize>_<raise>': "Action guide: include both <criticize> and <raise>. Use <think> if needed. Finish your whole response within 300 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<respond>_<criticize>_<raise>': "Action guide: include all of <respond>, <criticize>, and <raise>. Use <think> if needed. Finish your whole response within 600 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
}

action_prompts_zh = {
    '<respond>': "行动指南：只包括<回答>。如果需要，请使用<思考>。整个回答不超过300字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<criticize>_<raise>': "行动指南：包括<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过300字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<respond>_<criticize>_<raise>': "行动指南：包括<回答>、<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过600字，包括<思考>。将每个行动都用相应的标签括起来！",
}

action_prompts_writing = {
    '<respond>': "Action guide: only include <respond>. Use <think> if needed. Finish your whole response within 400 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<criticize>_<raise>': "Action guide: only include <criticize> and <raise>. Use <think> if needed. Do not use <respond>. Finish your whole response within 400 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
    '<respond>_<criticize>_<raise>': "Action guide: include all of <respond>, <criticize>, and <raise>. Use <think> if needed. Finish your whole response within 800 words, including <think>. ENCLOSE EACH ACTION IN ITS RESPECTIVE TAGS!",
}

action_prompts_writing_zh = {
    '<respond>': "行动指南：只包括<回答>。如果需要，请使用<思考>。整个回答不超过400字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<criticize>_<raise>': "行动指南：包括<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过400字，包括<思考>。将每个行动都用相应的标签括起来！",
    '<respond>_<criticize>_<raise>': "行动指南：包括<回答>、<批评>和<提问>。如果需要，请使用<思考>。整个回答不超过800字，包括<思考>。将每个行动都用相应的标签括起来！",
}

need_extra_space_cats = ['writing', 'roleplay', 'coding', 'humanities/social science knowledge']
need_extra_space_cats_zh = ['编程']

missing_actions_prompts = 'Only generate //ACTIONS_UNDONE//! ENCLOSE THEM IN TAGS!'

missing_actions_prompts_zh = '只生成//ACTIONS_UNDONE//! 用标签括起来!'

opponent_response = 'Opponent\'s Response:'

opponent_response_zh = '对手的回答:'

#######################################################
################### JUDGE PROMPTS #####################
#######################################################

round_instruction = '[[Round //NUM//]]'

round_instruction_zh = '[[第//NUM//轮]]'

assistant = 'Assistant //ROLE//'

assistant_zh = '//ROLE//助手'

judge = 'Judge //NUM//'

judge_zh = '评委//NUM//'

tie = '[[Tie]]'

tie_zh = '[[平局]]'

ref_answer_prompt = 'Please provide an accurate and concise response to the following question, do not add anything else.\n'

ref_answer_prompt_zh = '请对以下问题提供准确简洁的回答，不要添加其他内容。\n'

judge_instruction = "This is a chatbot arena. Two AI assistants had a multi-round debate on who is more helpful. Please act as an impartial judge and evaluate the capability of two AI assistants. You should choose the assistant that follows instructions and answers questions better. Your evaluation should consider factors such as helpfulness, relevance, and accuracy. Begin your evaluation by comparing the responses of the two assistants and provide a short explanation. Avoid any position biases and ensure that the order in which the responses were presented does not influence your decision. DO NOT allow the LENGTH of the responses to influence your evaluation, choose the one that is straight-to-the-point instead of unnecessarily verbose. When the two candidates perform equally well, choose the SHORTER answer. Do not favor certain names of the assistants. Be as objective as possible. After providing your explanation concisely within 200 words, output your final verdict by strictly following this format: \"[[A]]\" if assistant A is better, \"[[B]]\" if assistant B is better, and \"[[Tie]]\" for a tie. Finish your judgement within 300 words."

judge_instruction_zh = "这是一场聊天机器人辩论赛。请作为一个公正的裁判，评估两个AI助手的能力。您应该选择指令遵循能力更强、回答问题更好的助手。您的评估应该考虑有用性、相关性、简洁度、和准确性等因素。开始您的评估时，请比较两个助手的回应，并提供简短的解释。避免任何立场偏见，并确保回应呈现的顺序不影响您的决定。不要让回应的长度影响您的评估。选择直接简洁而非繁杂冗长的那个！当两个候选人表现同样出色时，选择更短的答案！不要偏爱助手的某些名字。尽可能客观。在200字内简洁地提供您的解释后，严格按照以下格式给出您的最终裁决：如果A助手更好，回答“[[A]]”；如果B助手更好，回答“[[B]]”；如果平局，回答“[[Tie]]”。在300字内完成您的判断。"

judge_debate_instruction = "Below are the responses from other judges in the committee. Please read them and decide whether you want to adjust your rating or maintain your original judgement. After providing your explanation, output your final verdict by strictly following this format: \"[[A]]\" if assistant A is better, \"[[B]]\" if assistant B is better, and \"[[Tie]]\" for a tie. Finish your judgement within 300 words."

judge_debate_instruction_zh = "以下是委员会中其他裁判的判断。请阅读并决定您是想要调整您的评级还是保持原来的判断。在提供解释之后，严格按照以下格式给出您的最终裁决：如果A助手更好，回答“[[A]]”；如果B助手更好，回答“[[B]]”；如果平局，回答“[[Tie]]”。在300字内完成您的判断。"

judge_debate_start = 'Above are the responses from other judges. Please make your judgment now:'

judge_debate_start_zh = '以上是其他评委的回答。请现在做出您的判断：'

judge_use_ref_answer_instruction = 'Focus more on the accuracy of the answers, here is a Reference Answer to use:'

judge_use_ref_answer_instruction_zh = '请更专注于答案的准确性，这里有一个参考答案供您使用：'

#######################################################
################### PROMPTER CLASS ####################
#######################################################

class Prompter:
    def __init__(self, lang='en'):
        self.lang = lang
        if self.lang == 'en':
            self.domain_list = domain_list
            self.qgen_command_dict = qgen_command_dict
            self.qgen_example_dict = qgen_example_dict
            self.question_generation_instruction = question_generation_instruction
            
            self.candidate_instruction = candidate_instruction
            self.init_user_input = init_user_input
            self.missing_actions_prompts = missing_actions_prompts
            
            self.actions = actions
            self.action_prompts = action_prompts
            self.action_prompts_writing = action_prompts_writing
            self.need_extra_space_cats = need_extra_space_cats
            self.opponent_response = opponent_response
            
            self.round_instruction = round_instruction
            self.assistant = assistant
            self.judge = judge
            self.tie = tie
            self.ref_answer_prompt = ref_answer_prompt
            self.judge_instruction = judge_instruction
            self.judge_debate_instruction = judge_debate_instruction
            self.judge_debate_start = judge_debate_start
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction
            
            self.word2token = 4/3
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        elif self.lang == 'zh':
            self.domain_list = domain_list_zh
            self.qgen_command_dict = qgen_command_dict_zh
            self.qgen_example_dict = qgen_example_dict_zh
            self.question_generation_instruction = question_generation_instruction_zh
            
            self.candidate_instruction = candidate_instruction_zh
            self.init_user_input = init_user_input_zh
            self.missing_actions_prompts = missing_actions_prompts_zh
            
            self.actions = actions_zh
            self.action_prompts = action_prompts_zh
            self.action_prompts_writing = action_prompts_writing_zh
            self.need_extra_space_cats = need_extra_space_cats_zh
            self.opponent_response = opponent_response_zh
            
            self.round_instruction = round_instruction_zh
            self.assistant = assistant_zh
            self.judge = judge_zh 
            self.tie = tie_zh
            self.ref_answer_prompt = ref_answer_prompt_zh
            self.judge_instruction = judge_instruction_zh
            self.judge_debate_start = judge_debate_start_zh
            self.judge_debate_instruction = judge_debate_instruction_zh
            self.judge_use_ref_answer_instruction = judge_use_ref_answer_instruction_zh
            
            self.word2token = 1.5
            self.word_limit_normal = 300
            self.word_limit_extra_space = 400 #for need_extra_space_cats
            self.judge_word_limit = 300 #for judge verdicts
        else:
            raise ValueError("Invalid language: " + lang)
        
        # no need to add to this part
        if self.lang != 'en':
            self.domain_en_to_lang = {en: other for en, other in zip(domain_list, self.domain_list)}
            self.action_en_to_lang = {en: other for en, other in zip(actions, self.actions)}
    
    def get_qgen_prompt(self, domain, num):
        prompt = self.question_generation_instruction.replace('//NUM//', str(num)).replace('//DOMAIN//', domain).replace('//QGEN_COMMAND_DOMAIN//', self.qgen_command_dict[domain]).replace('//QGEN_EXAMPLE_DOMAIN//', self.qgen_example_dict[domain])
        return prompt
    
    def cats_in_language(self, cats):
        if self.lang == 'en':
            return cats
        else:
            return [self.domain_en_to_lang[cat] for cat in cats]
        
    def acts_in_language(self, acts):
        if self.lang == 'en':
            return acts
        else:
            return [self.action_en_to_lang[act] for act in acts]