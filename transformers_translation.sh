while getopts i:t:r:x: flag
do
    case "${flag}" in
        i) train=${OPTARG};;
        t) test=${OPTARG};;
        r) checkpoint=${OPTARG};;
        x) method=${OPTARG};;
    esac
done
if [ ! -z "$checkpoint" ]
then
  python3 transformers/examples/pytorch/translation/run_translation.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_predict \
    --source_lang en \
    --target_lang de \
    --train_file "${train}.json" \
    --test_file "${test}.json" \
    --output_dir "./translation_${method}_$(date +"%T")" \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --save_steps 25000 \
    --resume_from_checkpoint "${checkpoint}"
else
    python3 translation_csv_to_json.py ${train}
    python3 translation_csv_to_json.py ${test}
    python3 transformers/examples/pytorch/translation/run_translation.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_predict \
    --source_lang en \
    --target_lang de \
    --train_file "${train}.json" \
    --test_file "${test}.json" \
    --output_dir "./translation_${method}_$(date +"%T")" \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --save_steps 25000
fi