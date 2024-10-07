from utils.generator import load_question_from_generator
from utils.LD_pair import make_pair_debate_many_questions, peer_evaluate_many_debates, get_committee
import argparse
from utils.prompts import Prompter
from utils.score_utils import compute_mle_elo, calculate_win_rate
from utils.api_utils import model2family

if __name__ == "__main__":
    # read arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--model_a", type=str, default='Qwen/Qwen1.5-72B-Chat', help="first contestant")
    parser.add_argument("--model_b", type=str, default='claude-3-haiku-20240307', help="second contestant")
    parser.add_argument("--num_each_domain_to_load", type=int, default=5, help="number of questions to debate for each domain")
    parser.add_argument("--judge_debate_rounds", type=int, default=1, help="How many rounds of debates to run")
    parser.add_argument("--question_save_file", type=str, default='data/generated_questions_difficult.jsonl', help="where to save generated questions")
    parser.add_argument("--debate_history_file", type=str, default='unspecified')
    parser.add_argument("--judge_save_file", type=str, default='unspecified')
    parser.add_argument("--shuffle_ab", type=bool, default=True, help="whether to shuffle the order of model_a and model_b")
    parser.add_argument("--evaluate_first_turn", action="store_true", help="whether to evaluate the first turn of the debate")
    parser.add_argument("--language", type=str, default='en', help="language used for evaluation")

    args = parser.parse_args()

    # this needs to be specified to decide committees
    all_models = ['gpt-4-turbo-2024-04-09', 'Qwen/Qwen1.5-72B-Chat', 'claude-3-haiku-20240307',
                  'zero-one-ai/Yi-34B-Chat', 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'gpt-35-turbo-0125',
                  'meta-llama/Llama-2-70b-chat-hf']

    # committee
    args.committee = get_committee(all_models, args.model_a, args.model_b)

    if args.all_judge_file == 'unspecified':
        args.all_judge_file = f'data/all_results/all_judge_results_{args.language}.jsonl'
    if args.all_debate_file == 'unspecified':
        args.all_debate_file = f'data/all_results/all_debate_history_{args.language}.jsonl'
    
    print('Arguments: ', args)
    
    print('************* STAGE 1: Question Generation *************')
    promptor = Prompter(args.language)
    
    # load questions
    questions = load_question_from_generator(promptor, args.question_save_file, args.num_each_domain_to_load)
    
    print('***************** STAGE 2: Peer Battles ****************')
    debates = make_pair_debate_many_questions(promptor, args.model_a, args.model_b, questions,
                                              args.debate_history_file, args.all_debate_file,
                                              shuffle_ab = args.shuffle_ab)

    print('****************** STAGE 3: Peer Review ****************')
    evals, _ = peer_evaluate_many_debates(promptor, debates, args.committee, args.judge_debate_rounds,
                                           args.judge_save_file, args.all_judge_file, print_scores = True,
                                           evaluate_first_turn = args.evaluate_first_turn)
    
    print('Win rates: ')
    print(calculate_win_rate(evals, args.judge_debate_rounds)['overall_win_rate'])
                