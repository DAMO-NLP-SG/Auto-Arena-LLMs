from utils.generator import load_question_from_generator
from LD_utils.LD_pair import make_pair_debate_many_questions, peer_evaluate_many_debates
import argparse
from utils.prompts import Prompter

if __name__ == "__main__":
    # read arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--model_a", type=str, default='Qwen/Qwen1.5-72B-Chat', help="first contestant")
    parser.add_argument("--model_b", type=str, default='claude-3-haiku-20240307', help="second contestant")
    parser.add_argument("--num_each_domain_to_load", type=int, default=5, help="number of questions to debate for each domain")
    parser.add_argument("--judge_debate_rounds", type=int, default=1, help="How many rounds of debates to run")
    parser.add_argument("--question_save_file", type=str, default='data/generated_questions_difficult.jsonl', help="where to save generated questions")
    parser.add_argument("--debate_history_file", type=str, required=True, help="where to save debates")
    parser.add_argument("--judge_save_file", type=str, required=True, help="where to save judge results")
    parser.add_argument("--shuffle_ab", type=bool, default=True, help="whether to shuffle the order of model_a and model_b")
    parser.add_argument("--evaluate_first_turn", action="store_true", help="whether to evaluate the first turn of the debate")

    args = parser.parse_args()
    
    promptor = Prompter(args.language)

    all_models = ['gpt-4-turbo-2024-04-09', 'Qwen/Qwen1.5-72B-Chat', 'claude-3-haiku-20240307',
                  'zero-one-ai/Yi-34B-Chat', 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'gpt-35-turbo-0125',
                  'meta-llama/Llama-2-70b-chat-hf']

    # committee
    args.committee = [m for m in all_models if m not in [args.model_a, args.model_b]]
    print('Arguments: ', args)


    print('************* STAGE 1: Question Generation *************')
    questions = load_question_from_generator(promptor, args.question_save_file, args.num_each_domain_to_load)

    print('***************** STAGE 2: Peer Battles ****************')
    debates = make_pair_debate_many_questions(promptor, args.model_a, args.model_b, questions,
                                              args.debate_history_file,
                                              shuffle_ab = args.shuffle_ab)

    print('****************** STAGE 3: Peer Review ****************')
    evals, _ = peer_evaluate_many_debates(promptor, debates, args.committee, args.judge_debate_rounds,
                                           args.judge_save_file, print_scores = True,
                                           evaluate_first_turn = args.evaluate_first_turn)
    
