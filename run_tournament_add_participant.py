import math
from typing import Dict, List, Tuple
import argparse

from tqdm import tqdm

from utils.generator import load_question_from_generator
from utils.LD_pair import make_pair_debate_many_questions, peer_evaluate_many_debates 
from utils.score_utils import compute_mle_elo, preety_print_model_ratings, calculate_win_rate
import pandas as pd
from collections import defaultdict
import os
from utils.common_utils import read_jsonl

def read_tournament(tournament_dir, judge_debate_rounds, new_participant):
    # find all judge files
    all_rounds = [r for r in os.listdir(tournament_dir) if os.path.isdir(f'{tournament_dir}/{r}')]
    # organize by number
    all_rounds = sorted(all_rounds, key=lambda x: int(x.split('_')[0].replace('round', '')))
    # filter the ones before the new participant
    rounds = []
    for r in all_rounds:
        if new_participant.replace('/', '_') in r:
            print('Stopping at round: ', r)
            break
        else:
            rounds.append(r)
    judge_files = []
    for r in rounds:
        if os.path.isdir(f'{tournament_dir}/{r}'):
            judge_files += [f'{tournament_dir}/{r}/{f}' for f in os.listdir(f'{tournament_dir}/{r}') if f.endswith('_judge_results.jsonl')]
    # initialize
    judge_results = []
    previous_matchups = defaultdict(set)
    participants = []

    for j in judge_files:
        results = list(read_jsonl(j))
        judge_results.extend(results)
        # record previous matchups
        models = results[0]['gamekey'][1:3]
        previous_matchups[models[0]].add(models[1])
        previous_matchups[models[1]].add(models[0])
        participants.extend(models)
    print(f'loaded {len(judge_results)} judge results')
    judge_results = [j for j in judge_results if j['judge_debate_rounds'] == judge_debate_rounds]
    print(f'filtered to {len(judge_results)} judge results')
    # get unique participants
    participants = list(set(participants))
    return judge_results, previous_matchups, participants

def pair_players(
    names: List[str], previous_matchups: Dict[str, set]
) -> List[Tuple[str, str]]:
    
    def can_be_paired(player1, player2):
        return player2 not in previous_matchups.get(player1, set())

    def find_pairings():
        # repeat until all players are paired
        if not unpaired_names:
            return []

        # first player
        player = unpaired_names.pop(0)

        # for the rest (opponents)
        for opponent in unpaired_names:

            # if have not played before
            if can_be_paired(player, opponent):

                # add to matchup pairings
                unpaired_names.remove(opponent)
                previous_matchups[player].add(opponent)
                previous_matchups[opponent].add(player)
                return [(player, opponent)] + find_pairings()

        # Assign a bye if no opponent is found
        print(f"Bye for {player}")
        # None is to indicate that this player has no opponents
        # Every opponent has been played before
        return [(player, None)] + find_pairings()

    # initialize unpaired to all players
    unpaired_names = names[:]

    return find_pairings()

if __name__ == "__main__":
    # read arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--num_each_domain_to_load", type=int, default=5, help="number of questions to debate for each domain")
    parser.add_argument("--judge_debate_rounds", type=int, default=1, help="How many rounds of debates to run")
    parser.add_argument("--question_save_file", type=str, default='data/generated_questions_difficult.jsonl', help="where to save generated questions")
    parser.add_argument("--tournament_dir", type=str, required=True, help="where to save the tournament files")
    parser.add_argument("--shuffle_ab", type=bool, default=True, help="whether to shuffle the order of model_a and model_b")
    parser.add_argument("--add_participant", type = str, help="which new participant to add to the tournament")
    parser.add_argument("--language", type=str, default='en', help="language used for evaluation")
    
    args = parser.parse_args()
    if args.language == 'zh' and 'zh' not in args.tournament_dir:
        raise Exception("Mismatch between language and tournament directory. Please use a directory with 'zh' in the name.")
    if args.language not in ['en', 'zh']:
        raise Exception("Invalid language. Choose either 'en' or 'zh'.")
    
    # args.all_judge_file = 'data/all_results/all_judge_results_LD.jsonl'
    # args.all_debate_file = 'data/all_results/all_debate_history_LD.jsonl'

    # read previous tournament history
    judge_results, previous_matchups, previous_participants = read_tournament(args.tournament_dir, args.judge_debate_rounds, args.add_participant)

    # update all player names
    player_names = previous_participants + [args.add_participant]

    # initialize rating as mmlu scores
    mmlu_ratings = pd.read_csv('data/MMLU.csv')
    mmlu_ratings = mmlu_ratings[mmlu_ratings['Model'].isin(player_names)]
    missing_players = [p for p in player_names if p not in mmlu_ratings['Model'].tolist()]
    if len(missing_players) > 0:
        print(f"Missing MMLU ratings for the following players: {missing_players}")
        raise Exception(f'Provide initial MMLU scores of {missing_players} in data/MMLU.csv!')

    ############################################################
    ##################### INITIALIZATION #######################
    ############################################################

    # determine number of pairings to run
    num_pairings = math.ceil(math.log2(len(player_names)))
    print("Number of pairings to add new participant:", num_pairings)

    # read in previous scores, initialize new participant with 1000
    scores, _ = compute_mle_elo(judge_results, args.judge_debate_rounds)
    INIT_RATING=1000
    scores[args.add_participant] = INIT_RATING

    ############################################################
    ################### 1. LOAD QUESTIONS ######################
    ############################################################

    # load questions
    questions = load_question_from_generator(args.question_save_file, args.num_each_domain_to_load, language = args.language)

    # determine where to save this round's results
    existing_rounds = [f for f in os.listdir(args.tournament_dir) if os.path.isdir(f"{args.tournament_dir}/{f}")]
    matched_folder = [f for f in existing_rounds if args.add_participant.replace('/', '_') in f]
    if len(matched_folder) > 0:
        round_dir = f"{args.tournament_dir}/{matched_folder[0]}"
    else:
        # create a folder
        round_dir = f"{args.tournament_dir}/round{len(existing_rounds)+1}_add_{args.add_participant.replace('/', '_')}"
        os.makedirs(round_dir, exist_ok=True)

    # initialize elo history
    elo_history = {}
    for model in player_names:
        elo_history[model] = [scores[model]]

    # check for previous debate files
    previous_debates = [f for f in os.listdir(round_dir) if f.endswith('_debate_history.jsonl')]
    # for each round
    for pairing_num in tqdm(range(num_pairings)):
        # determine which model to play against
        # if previously determined
        if len([d for d in previous_debates if d.startswith(f'{pairing_num}_')]) > 0:
            add_write = args.add_participant.replace('/', '_')
            debate_file = [d for d in previous_debates if f'{pairing_num}_{add_write}_' in d][0]
            closest_model = debate_file.replace(f'{pairing_num}_{add_write}_', '').replace('_debate_history.jsonl', '').replace('_', '/')
            print('closest model: ', closest_model)
        # first pairing, pair the one with most similar MMLU to args.add_participant
        elif pairing_num == 0:
            mmlu_dict = dict(zip(mmlu_ratings['Model'], mmlu_ratings['MMLU']))
            participant_mmlu = mmlu_dict[args.add_participant]
            if participant_mmlu != -1:
                mmlu_dict.pop(args.add_participant)
                closest_model = min(mmlu_dict, key=lambda x:abs(mmlu_dict[x]-participant_mmlu))
            else:
                print('No MMLU provided, pairing with the middle model.')
                scores_no_participant = {k: v for k, v in scores.items() if k != args.add_participant}
                # pair the median model in the scores
                closest_model = sorted(scores_no_participant, key=lambda x: -scores_no_participant[x])[len(scores_no_participant)//2]
            print(f"Pairing {args.add_participant} with {closest_model} based on MMLU")
        # pair the one with most similar ELO
        else:
            other_scores = {k: v for k, v in scores.items() if k != args.add_participant and k not in previous_matchups[args.add_participant]}
            closest_model = min(other_scores, key=lambda x:abs(other_scores[x]-scores[args.add_participant]))
            print(f"Pairing {args.add_participant} with {closest_model} based on ELO")

        model_a = args.add_participant
        model_b = closest_model
        previous_matchups[model_a].add(model_b)
        previous_matchups[model_b].add(model_a)

        print('----------------- Match:', model_a, model_b, '-----------------')
        print('initial scores:', scores)
        # committee in descending order of scores
        committee = sorted(scores, key=scores.get, reverse=True)
        committee = [c for c in committee if c != model_a and c != model_b][:5]
        print('Committee:', committee)

        save_model_a_name = model_a.replace('/', '_')
        save_model_b_name = model_b.replace('/', '_')

        debate_history_file = f"{round_dir}/{pairing_num}_{save_model_a_name}_{save_model_b_name}_debate_history.jsonl"
        judge_save_file = f"{round_dir}/{pairing_num}_{save_model_a_name}_{save_model_b_name}_judge_results.jsonl"

        print('---- Peer Battles ----')
        debates = make_pair_debate_many_questions(model_a, model_b, questions,
                                                    debate_history_file,
                                                    shuffle_ab = args.shuffle_ab,
                                                    language = args.language)

        print('---- Peer Reviews ----')
        evals, elo_scores = peer_evaluate_many_debates(debates, committee, args.judge_debate_rounds,
                                                        judge_save_file,
                                                        initial_score=scores, print_scores = True,
                                                        evaluate_first_turn = False,
                                                        language = args.language)
        print('Win rates: ')
        print(calculate_win_rate(evals, args.judge_debate_rounds)['overall_win_rate'])
        judge_results.extend(evals)
        (mle_elo, _) = compute_mle_elo(judge_results, args.judge_debate_rounds)
        # update scores
        for model in player_names:
            if model in mle_elo:
                scores[model] = mle_elo[model]

        print('final scores:', scores)
        for model in player_names:
            elo_history[model].append(scores[model])

        elo_history_df = pd.DataFrame.from_dict(elo_history)
        elo_history_df.to_csv(f"{round_dir}/elo_history.csv")
        print(f"Round Scores sorted: {sorted(player_names, key=lambda p: -scores[p])}")
    
    # Sort players by their final scores for the final ranking
    final_ranking = sorted(player_names, key=lambda p: -scores[p])
    print("Final Ranking:", final_ranking)
    print('Final MLE ELO scores:')
    print(preety_print_model_ratings(compute_mle_elo(judge_results, args.judge_debate_rounds)[1]))