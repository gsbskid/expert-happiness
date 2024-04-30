# Steps to make New VectorStores

* Put all your PDFs in the `PDFs` folder
* run 
```
pip install -r requirements.txt
```
```
sudo apt-get update
sudo apt install poppler-utils tesseract-ocr libgl1-mesa-glx
```

* Now you can run the `extraction.ipynb` file 

## What does the extraction.ipynb file does

* It first gets the list of all `pdfs`
* Then it uses `unstructured` library to get text chunks 
* `Unstructured` Library at the backend first converts the pdfs to images 
* Then run `parition_image` on them 
* The `partition_image` uses $2$ models.

* * **Yolo** - to Identify image boxes
* * **Facebook/Detectron** - to identify the text sections

* * You can read more about the working here
* * [unstructred-image](https://unstructured-io.github.io/unstructured/core/partition.html#partition-image)
* * [unstructured-pdf](https://unstructured-io.github.io/unstructured/core/partition.html#partition-pdf)

* The parition function returns an iterable of the unstructred class 
* This class has `text` attribute which can be extracted using list comprehension
* Now we make $2$ version of the text 
* * **Unstructured_text** - text divided by chunks defined by the unstructured library 
* * **Normal_text** - text divided by chunks devided by the full text 

* The files then uses different evaluation techniques to determine which chunk is better 

* these evautlion mainly consistes of checking chunks on how much they are relevant, how much is their coverge, how less are they redundant

* After this it makes $2$ graphs showing the performance of each version on different tasks 

* After this, we create $2$ different vectorstores, which are saved for further usage 

# App.py

```
streamlit run app.py
```

* The Interface is similar, you have $2$ options to choose from for the vector-stores

* You can directly choose the vector store from the sidebar and ask your questions
