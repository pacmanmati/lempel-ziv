for f in ls data/original_files/text_files/*
do
    echo "file: $f"
    python batch.py $f
done    
