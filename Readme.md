First, launch `bash install.sh`.  
To launch the script for text summarization, use next command:   
```bash transformers_summarization.sh -i path_to_train -v path_to_val -t path_to_test```  

For translation, script requires tsv format.  Use following line:   
```bash transformers_translation.sh -i path_to_train -t path_to_test```

For classification, use next command:
```bash classification.sh -i path_to_train -t path_to_test```

For example, ```bash classification.sh -i path_to_train -t path_to_test```

For processing of data using <mask> replacement, use following command:
```bash mask_replacement.sh -i path_to_train -v path_to_val -t path_to_test```  
If your files are ```path/to/train.source``` and ```path/to/train.target```, path_to_train is ```path/to/train``` 


If you want to resume from checkpoint, add `-r path_to_checkpoint_dir` to any of two commands above.
