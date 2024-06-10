import jsonlines
import os
import tiktoken


def read_jsonl(file_path):
    with jsonlines.open(file_path) as reader:
        return [obj for obj in reader]

def read_jsonl_if_exists(fname):
    if os.path.exists(fname):
        return read_jsonl(fname)
    else:
        return []

def match_game_key(qid, model_a, model_b, games, 
                   match_turn = None, order_matters = True,
                   judges = None):

    # get game keys
    game_keys = [g['gamekey'] for g in games]

    # initialize
    matched = False
    matched_key = None
    matched_game = None

    if [qid, model_a, model_b] in game_keys: 
        matched_key = [qid, model_a, model_b]
        matched_game = [g for g in games if g['gamekey'] == matched_key]
        matched = True
    
    elif not order_matters and [qid, model_b, model_a] in game_keys: 
        matched_key = [qid, model_b, model_a]
        matched_game = [g for g in games if g['gamekey'] == matched_key]
        matched = True
        
    if matched:
        # match multi-turn
        if match_turn is not None:
            matched_game = [g for g in matched_game if g['num_rounds'] == match_turn]

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