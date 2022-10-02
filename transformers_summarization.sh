while getopts i:v:t:r: flag
do
    case "${flag}" in
        i) train=${OPTARG};;
        v) val=${OPTARG};;
        t) test=${OPTARG};;
        r) checkpoint=${OPTARG};;
    esac
done
if [ ! -z "$var" ]
then
  python3 transformers/examples/pytorch/summarization/run_summarization.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_eval \
    --do_predict \
    --train_file ${train} \
    --validation_file ${val} \
    --test_file ${test} \
    --source_prefix "summarize: " \
    --output_dir "./summarization_$(date +"%T")" \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --text_column source \
    --summary_column target \
    --save_steps 25000 \
    --resume_from_checkpoint "${checkpoint}"
else
  python3 transformers/examples/pytorch/summarization/run_summarization.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_eval \
    --do_predict \
    --train_file ${train} \
    --validation_file ${val} \
    --test_file ${test} \
    --source_prefix "summarize: " \
    --output_dir "./summarization_$(date +"%T")" \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --text_column source \
    --summary_column target \
    --save_steps 25000
fi