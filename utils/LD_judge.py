from utils.api_utils import generate_response
import re
import jsonlines
import os

ref_answer_file = 'data/all_results/ref_answers.jsonl'

if not os.path.exists(ref_answer_file):
    ref_answers = {}
else:
    # else read
    with jsonlines.open(ref_answer_file) as reader:
        ref_answers = [obj for obj in reader][0]

TIE_DELTA = 0.1

# Extract scores from judgments
two_score_pattern = re.compile("\[\[(\d+\.?\d*),\s?(\d+\.?\d*)\]\]")
two_score_pattern_backup = re.compile("\[(\d+\.?\d*),\s?(\d+\.?\d*)\]")
one_score_pattern = re.compile("\[\[(\d+\.?\d*)\]\]")
one_score_pattern_backup = re.compile("\[(\d+\.?\d*)\]")

# Categories that need reference answers
NEED_REF_CATS = ["math", "reasoning", "coding"]

class Judge:

    def __init__(self, promptor, model_name):

        self.model_name = model_name
        self.chat_history = [{"role": "system", "content": promptor.judge_instruction}]
        self.promptor = promptor
    
    def reformat_history(self, debate, ref_answer, evaluate_turn='LD'):

        q = debate['question']['question']
        chat_history = self.promptor.init_user_input + ' ' + q + '\n'

        if debate['question']['domain'] in self.promptor.cats_in_language(NEED_REF_CATS):
            chat_history += self.promptor.judge_use_ref_answer_instruction + f'\n{ref_answer}\n'

        if evaluate_turn == 'LD':
            for i in range(len(debate['rounds'])):

                round = debate['rounds'][i]
                chat_history += self.promptor.round_instruction.replace('//NUM//', str(i+1))

                for (role, response) in round:
                    content = response['original']
                    chat_history += self.promptor.assistant.replace('//ROLE//', role.upper()) + f':\n{content}\n'
        else:
            # the debate only has one round? what happened?
            if len(debate['rounds']) == 1:
                chat_history += f'\n\n{self.promptor.round_instruction.replace("//NUM//", "1")}\n'
                a_response = debate['rounds'][0][0][1]['original']
                chat_history += f'{self.promptor.assistant.replace("//ROLE//", "A")}:\n{a_response}\n'

                b_response = debate['rounds'][0][1][1]['original']
                chat_history += f'{self.promptor.assistant.replace("//ROLE//", "B")}:\n{b_response}\n'
            else:
                # if the debate has more than one round, but we only want to evaluate 1 round (without peer battle)
                chat_history += f'\n\n{self.promptor.round_instruction.replace("//NUM//", "1")}\n'
                # first round first response
                a_response = debate['rounds'][0][0][1]['original']
                chat_history += f'{self.promptor.assistant.replace("//ROLE//", "A")}:\n{a_response}\n'
                # second round first response
                b_response = debate['rounds'][1][0][1]['original']
                chat_history += f'{self.promptor.assistant.replace("//ROLE//", "B")}:\n{b_response}\n'

        return chat_history
    
    def receive_previous_response(self, eval_history):
        # initial debate history and response
        debate_history = eval_history['debate_history']
        self.chat_history.append({'role': 'user', 'content': debate_history})
        evals = eval_history[self.model_name]['judgement']
        self.chat_history.append({'role': 'assistant', 'content': evals[0]})

        # if there has been debates
        if len(evals) > 1:
            for i in range(1, len(eval)):
                self.receive_committee_response(eval_history, i)
                self.chat_history.append({'role': 'assistant', 'content': evals[i]})
    
    def get_evaluation(self, chat_history, ref_answer, evaluate_turn = 'LD'):

        # In the debate rounds, there is no chat history passed
        if chat_history != None:
            chat_history = self.reformat_history(chat_history, ref_answer, evaluate_turn)

            chat_history += '\n' + self.promptor.judge_instruction
            self.chat_history.append({'role': 'user', 'content': chat_history})
            debate_history = chat_history
        else:
            debate_history = None
        winner = "error"

        max_tokens = int(self.promptor.judge_word_limit * self.promptor.word2token)
        try:
            print(self.chat_history)
            judgement = generate_response(self, self.chat_history, n = 1, max_tokens = max_tokens)
            print('Judgement:', judgement)
        except Exception as e:
            if hasattr(e, 'param') and e.param in ['max_tokens', 'security']:
                judgement = '$ERROR$'
            else:
                raise e
            
        if chat_history is not None:
            judgement = judgement.replace(chat_history, '')

        if "[[A]]" in judgement:
            winner = "A"
        elif "[[B]]" in judgement:
            winner = "B"
        elif '[[Tie]]' in judgement or self.promptor.tie in judgement:
            winner = "tie"

        self.chat_history.append({'role': 'assistant', 'content': judgement})
        return winner, judgement, debate_history
    
    def receive_committee_response(self, judge_dict, debate_round):
        other_judges = [j for j in judge_dict['judges'] if j != self.model_name]
        committee_response = self.promptor.judge_debate_instruction
        i = 1
        for judge in other_judges:
            judgement = judge_dict[judge]["judgement"][debate_round-1]
            if judgement != '$ERROR$':
                # if we are doing 1st debate round, should see everyone else's round 0 response
                committee_response += f'\n\n{self.promptor.judge.replace("//NUM//", str(i))}:\n{judgement}'
                i += 1
        committee_response += '\n' + self.promptor.judge_debate_start
        self.chat_history.append({'role': 'user', 'content': committee_response})

def majority_vote(results):
    results = [r for r in results if r != 'error']
    sorted_count = sorted([(results.count(r), r) for r in set(results)], reverse=True)
    if len(sorted_count) == 1 or sorted_count[0][0] > sorted_count[1][0]:
        best_model = sorted_count[0][1]
    else:
        best_model = 'tie'
    return best_model

def generate_ref_answer(promptor, model_name, question):
    prompt = promptor.ref_answer_prompt + question
    input = [{'role': 'user', 'content': prompt}]
    ref_answer = generate_response(None, input, model_name = model_name).replace(prompt, '')
    return ref_answer

def peer_evaluate(promptor, committee, debate, 
                  judge_save_file = None,
                  judge_debate_rounds = 0,
                  evaluate_turn = 'LD',
                  previous_history = None):
    '''
    Input:
        committee: [str] list of model names in the committee
        debate: dict, the debate to evaluate
        judge_save_file: str, file to save current judge results
        judge_debate_rounds: int, the number of rounds to debate among judges, default is 0 (no debate, majority vote)
        previous_history: dict, the previous history of the debate, 
            this is only passed when the debate has been partially evaluated (not enough rounds)
    '''
    # if any is error, return error
    if previous_history is not None:
        judge_dict = previous_history
        judges = []
        judge_dict['judge_debate_rounds'] = judge_debate_rounds
        # initialize judges as objects with previous history
        for judge_name in committee:
            j = Judge(judge_name)
            j.receive_previous_response(previous_history)
            judges.append(j)

    else:
        winners = []
        judge_dict = {'gamekey': debate['gamekey'], 'judges': committee, 
                    'num_rounds': evaluate_turn, 'judge_debate_rounds': judge_debate_rounds,
                    'ref_answer': None}
        judges = []
        ############### STEP0: REFERENCE ANSWERS ################
        if debate['question']['domain'] in promptor.cats_in_language(NEED_REF_CATS):
            best_committee_member = committee[0]
            # if we have never generated ref answers in this language, initialize as empty
            if promptor.lang not in ref_answers.keys():
                ref_answers[promptor.lang] = {}
            if best_committee_member not in ref_answers[promptor.lang].keys():
                ref_answers[promptor.lang][best_committee_member] = {}
            # if we have a reference answer for this question
            if str(debate['gamekey'][0]) in ref_answers[promptor.lang][best_committee_member].keys():
                ref_answer = ref_answers[promptor.lang][best_committee_member][str(debate['gamekey'][0])]
            # else generate a new one
            else:
                print(f"Reference answer not found for {best_committee_member}")
                ref_answer = generate_ref_answer(promptor, best_committee_member, debate['question']['question'])
                ref_answers[promptor.lang][best_committee_member][debate['gamekey'][0]] = ref_answer
                # save
                with jsonlines.open(ref_answer_file, 'w') as writer:
                    writer.write(ref_answers)
        else:
            ref_answer = None
        judge_dict['ref_answer'] = ref_answer

        ############### STEP1: GENERATE JUDGEMENTS ################
        for judge_name in committee:
            judge = Judge(promptor, judge_name)
            winner, judgement, dh = judge.get_evaluation(debate, ref_answer, evaluate_turn = evaluate_turn)
            winners.append(winner)
            judge_dict[judge_name] = {"winner": [winner], "judgement": [judgement]}
            judges.append(judge)
            if 'debate_history' not in judge_dict.keys():
                judge_dict['debate_history'] = dh
                
        final_winner = majority_vote(winners)
        judge_dict['final_winner'] = [final_winner]

    ############### STEP2: DEBATE ################
    if judge_debate_rounds != 0:
        num_already_debated = len(judge_dict['final_winner'])-1
        # if we debated 1 round, we would have 2 winners
        # if we want to debate 3 rounds, it would be range(2,4), which is [2,3]
        for round_i in range(num_already_debated+1, judge_debate_rounds+1):
            winners = []
            for judge in judges:
                # first receive last round's committee response
                judge.receive_committee_response(judge_dict, round_i)
                winner, judgement, _ = judge.get_evaluation(None, None)
                judge_dict[judge.model_name]["judgement"].append(judgement)
                judge_dict[judge.model_name]["winner"].append(winner)
                if winner == 'error':
                    winners.append(judge_dict[judge.model_name]["winner"][-2])
                else:
                    winners.append(winner)
            final_winner = majority_vote(winners)
            judge_dict['final_winner'].append(final_winner)

    # if judge_save_file is not None and all_judge_file is not None:
    if judge_save_file is not None:
        
        # append to current history
        with jsonlines.open(judge_save_file, 'a') as writer:
            writer.write(judge_dict)
            
    return judge_dict