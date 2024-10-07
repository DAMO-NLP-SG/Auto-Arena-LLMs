import jsonlines
import os
import tiktoken
import os

model2family = {
    'gpt-35-turbo-0125': 'gpt',
    'gpt-4-turbo-2024-04-09': 'gpt',
    'gpt-4o-2024-05-13': 'gpt',
    'gpt-4-0125-preview': 'gpt',
    'gpt-4-0613': 'gpt',
    'gpt-4o-mini': 'gpt',
    #########################################################
    'claude-3-haiku-20240307': 'claude',
    'claude-3-opus-20240229': 'claude',
    'claude-3-sonnet-20240229': 'claude',
    'claude-3-5-sonnet-20240620': 'claude',
    'claude-2.1': 'claude',
    'claude-2.0': 'claude',
    'claude-instant-1.2': 'claude',
    #########################################################
    'models/gemini-pro': 'gemini',
    'models/gemini-1.5-pro-latest': 'gemini',
    "gemini-1.5-pro": 'gemini',
    'gemini-1.5-flash-exp-0827': 'gemini',
    #########################################################
    "google/gemma-2-27b-it": 'gemma',
    #########################################################
    'meta-llama/Llama-3-70b-chat-hf': 'llama',
    'meta-llama/Llama-2-70b-chat-hf': 'llama',
    'meta-llama/Llama-2-13b-chat-hf': 'llama',
    'meta-llama/Llama-2-7b-chat-hf': 'llama',
    'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo': 'llama',
    #########################################################
    'zero-one-ai/Yi-34B-Chat': 'yi',
    #########################################################
    'lmsys/vicuna-13b-v1.5': 'vicuna',
    'lmsys/vicuna-7b-v1.5': 'vicuna',
    #########################################################
    'mistralai/Mistral-7B-Instruct-v0.1': 'mistral',
    'mistralai/Mistral-7B-Instruct-v0.2': 'mistral',
    'mistralai/Mixtral-8x7B-Instruct-v0.1': 'mistral',
    'mistral-large-2402': 'mistral',
    #########################################################
    'Qwen/Qwen2-72B-Instruct': 'qwen',
    'Qwen/Qwen1.5-72B-Chat': 'qwen',
    'Qwen/Qwen1.5-14B-Chat': 'qwen',
    'Qwen/Qwen1.5-7B-Chat': 'qwen',
    'qwen-max-0428': 'qwen',
    #########################################################
    'deepseek-ai/deepseek-llm-67b-chat': 'deepseek',
    'deepseek-chat': 'deepseek',
    #########################################################
    'openchat/openchat-3.5-1210': 'openchat',
    #########################################################
    'glm-4': 'glm',
    #########################################################
    'wenxin-4': 'wenxin',
    #########################################################
    'minimax-abab6.5-chat': 'minimax',
    #########################################################
    'SenseChat-5': 'SenseChat',
    #########################################################
    'Baichuan2-Turbo-192k': 'Baichuan',
    #########################################################
    'reka-flash-20240226': 'reka',
    'reka-core-20240501': 'reka',
    #########################################################
    'command-r-plus': 'cohere',
}

def read_jsonl(file_path):
    with jsonlines.open(file_path) as reader:
        return [obj for obj in reader]

def read_jsonl_if_exists(fname):
    if os.path.exists(fname):
        return read_jsonl(fname)
    else:
        return []

def match_game_key(qid, model_a, model_b, games, 
                   match_turn = None, order_matters = False,
                   judges = None):

    # get game keys
    game_keys = [g['gamekey'] for g in games]

    # initialize
    matched = False
    matched_key = None
    matched_game = []

    if [qid, model_a, model_b] in game_keys: 
        matched_key = [qid, model_a, model_b]
        matched_game += [g for g in games if g['gamekey'] == matched_key]
        matched = True
    
    if not order_matters and [qid, model_b, model_a] in game_keys: 
        matched_key = [qid, model_b, model_a]
        matched_game += [g for g in games if g['gamekey'] == matched_key]
        matched = True
        
    if matched:
        # match multi-turn
        if match_turn is not None:
            matched_game = [g for g in matched_game if g['num_rounds'] == match_turn]

        # if it's a judge round
        if len(matched_game) > 0 and 'judge_debate_rounds' in matched_game[0]:
            # check if judges include models from the same families
            reevaluate = False
            for j in matched_game[0]['judges']:
                if model2family[j] == model2family[model_a] or model2family[j] == model2family[model_b]:
                    reevaluate = True
            if reevaluate:
                # return partial game
                # in this case, we have less than 5 judges
                matched_game_judges = [g for g in matched_game if set(g['judges']) == set(judges)] 
                # we have this game with different judges
                if len(matched_game_judges) == 0 and len(matched_game) >= 1:
                    print('Found matched games not with the same judges')
                    overlapping_judges = set(matched_game[0]['judges']) & set(judges)
                    print(f'{len(overlapping_judges)} overlapping judges: {overlapping_judges}')
                    # only keep the overlapping judges
                    partial_game = {'gamekey': matched_game[0]['gamekey'],
                                    'judges': list(overlapping_judges),
                                    'num_rounds': match_turn,
                                    'judge_debate_rounds': matched_game[0]['judge_debate_rounds'],
                                    'ref_answer': matched_game[0]['ref_answer'],
                                    'debate_history': matched_game[0]['debate_history']}
                    for j in overlapping_judges:
                        partial_game[j] = {}
                        partial_game[j]['judgement'] = [matched_game[0][j]['judgement'][0]]
                        partial_game[j]['winner'] = [matched_game[0][j]['winner'][0]]
                    matched_game = [partial_game]

                # has the same judges
                elif len(matched_game_judges) == 1:
                    matched_game = [matched_game_judges[0]]


        # if matched more than 1 games, this only happens when we matched a game with different rounds
        if len(matched_game) > 1:
            # if this is a judgement, return the one with highest judge debate rounds
            if 'judge_debate_rounds' in matched_game[0]:
                # game with max judge_debate_rounds: evaluation round
                matched_game = max(matched_game, key=lambda x: x['judge_debate_rounds'])
            # if this is a game, return the one with highest debate rounds
            else:
                matched_game = max(matched_game, key=lambda x: x['num_rounds'])
        
        # if matched only one game, return
        elif len(matched_game) == 1:
            matched_game = matched_game[0]
            
        # if matched 0 games, return None
        else:
            matched = False
            matched_key = None
            matched_game = None
            
    return matched, matched_key, matched_game

encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(string):
    return len(encoding.encode(string))

def init_all_results(tournament_dir, all_debate_file, all_judge_file):

    print(f'initializing all_debate_file and all_judge_file')
    rounds = [r for r in os.listdir(tournament_dir) if 'round' in r]

    debate_files = []
    judge_files = []
    for r in rounds:
        debate_files += [f'{tournament_dir}/{r}/{f}' for f in os.listdir(f'{tournament_dir}/{r}') if f.endswith('_debate_history.jsonl')]
        judge_files += [f'{tournament_dir}/{r}/{f}' for f in os.listdir(f'{tournament_dir}/{r}') if f.endswith('_judge_results.jsonl')]

    debates = []
    for j in debate_files:
        debates.extend(list(read_jsonl(j)))
    judge_results = []
    for j in judge_files:
        judge_results.extend(list(read_jsonl(j)))

    # if files don't exist, save to file
    if not os.path.exists(all_debate_file) and not os.path.exists(all_judge_file):
        # save to file
        with jsonlines.open(all_debate_file, mode='w') as writer:
            writer.write_all(debates)
        with jsonlines.open(all_judge_file, mode='w') as writer:
            writer.write_all(judge_results)
        print(f'initialized {len(debates)} previous debates')
        print(f'initialized {len(judge_results)} judge results')
    # else, save the results that are not in the file
    else:
        all_debates = read_jsonl(all_debate_file)
        all_judge_results = read_jsonl(all_judge_file)
        d_i = 0
        j_i = 0
        for d in debates:
            if d not in all_debates:
                all_debates.append(d)
                d_i += 1
        for j in judge_results:
            if j not in all_judge_results:
                all_judge_results.append(j)
                j_i += 1
        print(f'added {d_i} debates')
        print(f'added {j_i} judge results')
        # save to file
        with jsonlines.open(all_debate_file, mode='w') as writer:
            writer.write_all(all_debates)
        with jsonlines.open(all_judge_file, mode='w') as writer:
            writer.write_all(all_judge_results)