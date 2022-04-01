#Naive Bayes algorithm from scratch

class Naive_Bayes:
    def __init__(self,n_pos,n_neg):
        self.n_pos=n_pos
        self.n_neg=n_neg
        self.total_pos_word_occurrence=0
        self.total_neg_word_occurrence=0
        self.unique_words=0
        self.vocabulary={}
        
    def vocab_builder(self,text,sentiment):
        for word in text.split(" "):
            if word not in self.vocabulary.keys():
                self.vocabulary[word]=[0,0]
                if sentiment==0:
                    self.vocabulary[word][0]=1
                else:
                    self.vocabulary[word][1]=1
            else:
                self.vocabulary[word][sentiment]+=1
                
    def laplacian_smoothing(self):
        unique_words=set()
        for word in self.vocabulary.keys():
            #calculating the total no. of positive and negative occurences of words
            self.total_pos_word_occurrence+=self.vocabulary[word][1]
            self.total_neg_word_occurrence+=self.vocabulary[word][0]
            #calculating the total no. of unique words in the dictionary
            unique_words.add(word)
        self.unique_words=len(unique_words)
        for word in self.vocabulary.keys():
            self.vocabulary[word][0]=(self.vocabulary[word][0]+1)/(self.total_neg_word_occurrence+self.unique_words)
            self.vocabulary[word][1]=(self.vocabulary[word][1]+1)/(self.total_pos_word_occurrence+self.unique_words)
    
    
    def log_likelihood(self):
        for word in self.vocabulary.keys():
            self.vocabulary[word].append(np.log(self.vocabulary[word][1]/self.vocabulary[word][0]))
        
    def train(self,train_data,y_label):
        for tweet,label in zip(train_data['text'],y_label):
            self.vocab_builder(tweet,label)
        self.laplacian_smoothing()
        self.log_likelihood()
        '''for key in list(self.vocabulary.keys())[:20]:
            print(self.vocabulary[key])'''
            
    def predict(self,x_val,y_val):
        #print(x_val.shape,y_val.shape)
        correct_pred=0
        total_pred=x_val.shape[0]
        for i in range(x_val.shape[0]):
            document=x_val.iloc[i,:]['text']
            lst_of_words=document.split(" ")
            #new_word=False
            pred=0
            document_prob=0
            for word in lst_of_words:
                if word in self.vocabulary.keys():
                    document_prob+=self.vocabulary[word][2]
            if document_prob>=0:
                pred=1
            if pred==y_val[i]:
                correct_pred+=1
        acc=correct_pred/total_pred
        print("Accuracy:{:.3f}".format(acc))
        
    def test(self,document):
        pred=0
        document_prob=0
        lst_of_words=document.split(" ")
        for word in lst_of_words:
            if word in self.vocabulary.keys():
                document_prob+=self.vocabulary[word][2]
        if document_prob>=0:
            pred=1
        return pred
            

n_positive=y_train[y_train==1].sum()
n_negative=y_train.shape[0]-n_positive

NB=Naive_Bayes(n_positive,n_negative)
NB.train(x_train,y_train)