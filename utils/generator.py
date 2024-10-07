from utils.api_utils import generate_response
import jsonlines
from collections import defaultdict 
import os

class Generator:
    def __init__(self, promptor, model_name='gpt-4-turbo-2024-04-09',
        question_file='data/generated_questions_medium_difficult.jsonl', 
        n_each_time=10):
        self.promptor = promptor
        # Currently points to gpt-4-turbo-2024-04-09.
        self.model_name = model_name
        self.domains = promptor.domain_list
        if promptor.lang == 'en':
            self.domains = promptor.domain_list
            self.question_file = question_file
        else:
            # don't overlap with previous debate questions
            if not question_file.endswith(f'_{promptor.lang}.jsonl'):
                self.question_file = question_file.replace('.jsonl', f'_{promptor.lang}.jsonl')
                
        # how many questions do we ask LLM to generate in the prompt, set to 10
        self.n_each_time = n_each_time
        self.questions = []

    def get_prompt(self, domain: str, num: int):
        return self.promptor.get_qgen_prompt(domain, num)

    def parse_questions(self, qs):
        #qs: a string with 1. to 10.
        print('qs:', qs)
        questions_parsed = []
        for i in range(1, self.n_each_time+1):
            if i == self.n_each_time: #last one
                q = qs.split(f"({i}).")[1].strip()
            else:
                q = qs.split(f"({i}).")[1].split(f"({i+1}).")[0].strip()
            questions_parsed.append(q)
        return questions_parsed

    def generate_questions(self, num_each_domain_to_generate = 30, domains = None):
        if domains is not None:
            self.domains = domains
        # num each domain: should be a multiple of n_each_time
        questions = {}
        for domain in self.domains:
            questions[domain] = []
            prompt = self.get_prompt(domain, self.n_each_time)
            sample_n = num_each_domain_to_generate//self.n_each_time
            message = [{"role": "system", "content": prompt}]
            all_responses = generate_response(self.model_name, message, temperature = 0.7, 
                                              max_tokens = 3000, n = int(sample_n), 
                                              model_name = self.model_name)
            if sample_n != 1:
                for r in all_responses:
                    questions[domain] += self.parse_questions(r)
            else:
                questions[domain] += self.parse_questions(all_responses)
        # save to jsonl file
        with jsonlines.open(self.question_file, 'w') as writer:
            i = 1
            for domain, qs in questions.items():
                for q in qs:
                    writer.write({'domain': domain, 'id': i, 'question': q})
                    i += 1
        self.questions = questions
        return questions
    
    def load_questions(self, num_each_domain_to_load = False):
        loaded_domain_num = defaultdict(lambda: 0)
        questions = []
        with jsonlines.open(self.question_file) as reader:
            for obj in reader:
                # if num_each_domain_to_load is False, load all questions
                if num_each_domain_to_load == False:
                    questions.append(obj)
                # if num_each_domain_to_load is a number, load that many questions per domain
                elif loaded_domain_num[obj['domain']] < num_each_domain_to_load:
                    questions.append(obj)
                    loaded_domain_num[obj['domain']] += 1
        self.questions = questions
        return questions
    
    def get_question(self, question_id:int):
        if self.questions == []:
            self.load_questions()
        return [q for q in self.questions if q['id'] == question_id][0]
    

def load_question_from_generator(promptor, question_save_file, num_each_domain_to_load):
    gen = Generator(promptor, question_file=question_save_file)

    # generate if no questions
    if not os.path.exists(gen.question_file):
        gen.generate_questions(num_each_domain_to_generate=30)

    # load questions
    questions = gen.load_questions(num_each_domain_to_load = num_each_domain_to_load)
    print(f"Loaded {len(questions)} questions from {gen.question_file}")

    return questions

