from helper import execute, terminate_signal,console
terminate_signal() 
console.status("[orange1]Loading program. Please wait...", spinner="dots")
      
import pandas as pd       
    
import sys

#import re
#tokenizer = lambda text: re.findall(r'\b\w\w+\b', text)

#########################################################

'''
def obj_eval(obj):
    #This is simply for looking at the properties of an object
    #It's not a functioning part of the project
    
       
       
    print(f"Evaluating object {obj}...")
    #for name, member in inspect.getmembers(obj, predicate=callable):
    #     if inspect.ismethod(member) or inspect.isfunction(member):
    #        print(name)

    sig = inspect.signature(obj)
    for i in sig.parameters.values():
        print({i})

    sys.exit(0)
        
        
          
    

'''

def text_prep(text):
    #This prepares the raw data for processing
    import random

    documents = [(list(text.words(fileid)), category)
        for category in text.categories()
        for fileid in text.fileids(category)]
    random.shuffle(documents)

    reviews = [" ".join(words) for words, _ in documents]
    sentiments = [sentiment for _, sentiment in documents]

    return reviews, sentiments
 
    





class NLPmodel():
    def __init__(self, text, vec_type, model_type, **params):
        self.reviews, self.sentiment = text
        self.model_type = model_type
        self.vec_type = vec_type
        self.params = params
    
    
    def frameset(self):
        #This was originally for framing the data 
        
            df = pd.DataFrame({
                    'review': self.reviews,
                    'sentiment': self.sentiment})

            return df 
        
        


    def data_display(self, label, y_test, y_pred, accuracy):

        from sklearn.metrics import classification_report as summary_rep

        print(f"\nResults for {label}\n")
        print(summary_rep(y_test, y_pred), f"\n\nAccurary Score: {accuracy}%") 
        

    def modelsetup(self):
        from sklearn.model_selection import train_test_split
        
        # Pull out only the test split params
        split_params = {
            key: self.params.pop(key) 
            for key in ["test_size", "random_state"] 
            if key in self.params
        }
        df = self.frameset()
                    
        x_train, x_test, y_train, y_test = train_test_split(
            df['review'], df['sentiment'], **split_params
        ) 

        return x_train, x_test, y_train, y_test, df
        
        

    def classifier_setup(self):
        from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB

        #This is a dictionary to map out the different vectorizers. It is more
        #efficient then creating multiple vectorizer objects. The key is the vector type
        #passed from the object constructor parameter.
        vectorizer_map = {"cv": (CountVectorizer, "CountVectorizer"),
                                "tfidf":(TfidfVectorizer, "TF-IDF Vectorizer"),}
            
        if self.vec_type not in vectorizer_map:
                    raise ValueError(f"Error: Unknown vector type: {self.vec_type}")

        #This same goes for the diffent models used in the lectures

        from sklearn.svm import LinearSVC
        model_map = {"svm":(LinearSVC(class_weight='balanced'), " with SVC classifier"),
                        "nb":(MultinomialNB(), " with Naive Bayes classifier")}

        if self.model_type not in model_map:
                    raise ValueError(f"Error: Unknown model type: {self.model_type}")
            
        #This uses the passed in object values to reference the dictionary   
        VectorizerClass, vec_label = vectorizer_map[self.vec_type]
        model, model_label = model_map[self.model_type]
        

        return VectorizerClass, vec_label, model, model_label
        
        
        


    def model_fit(self, VectorizerClass, model, x_train, x_test, y_train):
        

        #This function takes the passed in values, builds a vectorizer
        #and then fits the appropriate values into the passed in model
        
        vectorizer = VectorizerClass(**self.params)
        x_train_vec = vectorizer.fit_transform(x_train)
        x_test_vec = vectorizer.transform(x_test)
            
        model.fit(x_train_vec, y_train)

        y_predict = model.predict(x_test_vec)

        return y_predict

        
         

    
    
    def classifier(self):
                
        from sklearn.metrics import accuracy_score as ac_score

        x_train, x_test, y_train, y_test, df = self.modelsetup()            #This obtains the split training and testing values to set up the model               
        
        VectorizerClass, vec_label, model, model_label = self.classifier_setup() #This calls the function that contains a defining dictionary of keys and paramters                                                                                                                          
        
        y_predict = self.model_fit(VectorizerClass, model, x_train, x_test, y_train)#This calls the model_fit() function that takes the model and training/test values
        accuracy = ac_score(y_test, y_predict)                                      # and fits them to the appropriate model, returning a prediction value  
        accuracy = accuracy * 100
        self.data_display(vec_label+model_label, y_test, y_predict, accuracy)


        


def main():

    
    with console.status("[bold cyan]Downloading NLTK dataset...", spinner="dots"):
        from nltk import download
        download('movie_reviews', quiet=True)
        download('stopwords', quiet=True)
        #stopword_set = set(stopwords.words('english'))  
    with console.status("[bold cyan]Downloading NTLK corpus...", spinner="dots"):
        from nltk.corpus import movie_reviews
        if not movie_reviews:
            print("Error: No dataset found. Terminating program")
            sys.exit(0)

    with console.status("[bold cyan]Reading, tokenizing, and preparing 2,000 movie reviews...", spinner="dots"):
        arranged_text = text_prep(movie_reviews)
    
    #Here we have the different parameters for the vectorizers
    vectorizer_configs = {
                                "cv": {
                                    "stop_words": "english",
                                    "lowercase": True,
                                    "token_pattern": r"\b\w+\b",
                                    "test_size": 0.2,
                                    "random_state": 42
                                },
                                "tfidf": {
                                    "stop_words": "english",
                                    "lowercase": True,
                                    "max_features": 5000,
                                    "token_pattern": r"\b\w+\b",
                                    "test_size": 0.2,
                                    "random_state": 42,
                                    "max_df": 0.75, #changed from 0.7
                                    "min_df": 5,
                                    "ngram_range": (1, 2), #added for fine tuning
                                    "sublinear_tf": True #added for fine tunine
                                }
                            }
    
    #model types
    models = ["nb", "svm"]
    for model_type in models:
        for vec_type, params in vectorizer_configs.items():
            console.print(f"\n[green]Running {vec_type.upper()} + {model_type.upper()}...[/green]")
            model = NLPmodel(arranged_text, vec_type, model_type, **params)
            model.classifier()


    


if __name__ == "__main__":
    execute(main)
        



