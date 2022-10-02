First, launch `bash install.sh`.  
To launch the script for text summarization, use next command:   
```bash transformers_summarization.sh -i path_to_train -v path_to_val -t path_to_test```  

For translation, script requires tsv format.  Use following line:   
```bash transformers_translation.sh -i path_to_train -t path_to_test```


If you want to resume from checkpoint, add `-r path_to_checkpoint_dir` to any of two commands above.
