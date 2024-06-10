from utils.common_utils import read_jsonl_if_exists, match_game_key
from utils.LD_debate import make_pair_debate
from utils.LD_judge import peer_evaluate
from utils.score_utils import print_eval_results
import jsonlines
import random


# Make a pair of models debate many questions
def make_pair_debate_many_questions(promptor, model_a, model_b, questions,
                                    debate_history_file,
                                    shuffle_ab = True):
    '''
    Input:
        model_a, model_b: str, model names
        questions: [dict] list of questions items
        debate_history_file: str, file to save debate history
        shuffle_ab: bool, whether to shuffle the order of a and b at each question
    Output:
        debates: [dict] list of debates
    '''
    # read all debates
    all_debate_history = read_jsonl_if_exists(debate_history_file)
    current_debates = []

    
    for question in questions:

        if shuffle_ab:
            # shuffle the order of a and b
            model_l = [model_a, model_b]
            model_a = random.choice(model_l)
            model_b = model_l[1] if model_a == model_l[0] else model_l[0]

        # check if already debated
        matched, gamekey, game = match_game_key(question['id'], model_a, model_b, 
                                                all_debate_history, order_matters=False,
                                                match_turn='LD')

        if not matched:

            # make a new debate if not debated
            print(f"New debate for [{question['id']}, {model_a}, {model_b}]")
            peer_battle_history = make_pair_debate(promptor, model_a, model_b, question, 
                                                   debate_history_file)
            current_debates.append(peer_battle_history)
            print('Peer battle completed.')

        else:
            # print(f"Already debated at {gamekey}")
            current_debates.append(game)

            existing_debates = read_jsonl_if_exists(debate_history_file)
            if game not in existing_debates:
                # write to own history
                with jsonlines.open(debate_history_file, 'a') as writer:
                    writer.write(game)
        
    return current_debates

# make a committee of models evaluate many debates
def peer_evaluate_many_debates(promptor, debates, committee, judge_debate_rounds,
                               judge_save_file,
                               initial_score = None, print_scores = True,
                               evaluate_first_turn = False):
    '''
    Input:
        debates: [dict] list of debates
        committee: [str] list of model names
        judge_debate_rounds: how many rounds to debate among judges
        judge_save_file: str, file to save judge results
        evaluate_first_turn: whether to evaluate the first turn (a response, b response)
    '''
    # all_judge_results = read_jsonl_if_exists(all_judge_file)
    all_judge_results = read_jsonl_if_exists(judge_save_file)
    evals = []

    if evaluate_first_turn:
        turn = 1
    else:
        turn = 'LD'

    print(f"Evaluating Turn: {turn}-----------------------")
    for debate in debates:

        # check if already evaluated
        matched, gamekey, game = match_game_key(debate['gamekey'][0], debate['gamekey'][1], debate['gamekey'][2], 
                                                all_judge_results, match_turn=turn, judges=committee, order_matters = False)
        # already debated with enough rounds
        if matched and game['judge_debate_rounds'] >=  judge_debate_rounds:
            # print(f"Already evaluated at {gamekey}")
            evals.append(game)

            existing_evals = read_jsonl_if_exists(judge_save_file)
            if game not in existing_evals:
                # write to own history
                with jsonlines.open(judge_save_file, 'a') as writer:
                    writer.write(game)

        # not debated at all
        elif not matched:
            print(f"Evaluating Debate: {debate['gamekey']}")
            eval = peer_evaluate(promptor, committee, debate, 
                                judge_save_file,
                                judge_debate_rounds = judge_debate_rounds,
                                evaluate_turn = turn)
            
            evals.append(eval)

        # evaluated but not enough rounds
        else:
            print(f'Evaluated at {gamekey} but only {game["judge_debate_rounds"]} rounds')
            eval = peer_evaluate(promptor, committee, debate, 
                                judge_save_file,
                                judge_debate_rounds = judge_debate_rounds,
                                evaluate_turn = turn,
                                previous_history = game)
            evals.append(eval)
                
    elo_scores, win_rates = print_eval_results(evals, initial_score = initial_score,
                                    print_scores = print_scores,
                                    judge_debate_rounds = judge_debate_rounds)
    print('Win rates:', win_rates)

    return evals, elo_scores