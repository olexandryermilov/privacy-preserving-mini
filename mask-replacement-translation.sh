while getopts i:v:t:r: flag
do
    case "${flag}" in
        i) train=${OPTARG};;
        v) val=${OPTARG};;
        t) test=${OPTARG};;
        r) checkpoint=${OPTARG};;
    esac
done
python3 bert-mlm-replacement.py translation ${train} ${test}
python3 transformers/examples/pytorch/translation/run_translation.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_predict \
    --source_lang en \
    --target_lang de \
    --train_file "./train_anonymized_translation_spacy_ner-mask.json" \
    --test_file "./test_anonymized_translation_spacy_ner-mask.json" \
    --output_dir "./translation_$(date +"%T")" \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --text_column text \
    --summary_column summary \
    --save_steps 25000
fi