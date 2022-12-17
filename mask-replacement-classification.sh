while getopts i:v:t:r: flag
do
    case "${flag}" in
        i) train=${OPTARG};;
        v) val=${OPTARG};;
        t) test=${OPTARG};;
        r) checkpoint=${OPTARG};;
    esac
done
python3 bert-mlm-replacement.py summarization ${train} ${val} ${test}
bash classification.sh -i "train_anonymized_spacy_ner-mask.csv" -t "test_anonymized_spacy_ner-mask.csv"