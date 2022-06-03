<h1 align="center" style="color:dodgerblue; font-weight:700"> Sentiment Analysis on Twitter Tweets</h1>
<hr/>
<br/>
<p>Sentiment Analysis is conducted on various datasets after exploratory data analysis and data preprocessing, separately using variety of Machine Learning techniques</p>
    <h3 style=\"font-weight:600;\">15 implemented ML Algorithms : </h3>
    <ol>
    <li>Logistic Regression</li>
    <ul>
    <li>Newton CG</li>
    <li>SAG</li>
    <li>SAGA</li>
    <li>LBFGS</li>
    </ul>
    <li>Decision Tree Classifier</li>
    <li>Support Vector Machines</li>
    <ul>
    <li>Linear</li>
    <li>Poly</li>
    <li>RBF</li>
    <li>Sigmoid</li>
    </ul>
    <li>Majority Voting Ensemble</li>
    <li>Extreme Laerning Machines</li>
    <ul>
    <li>Tanh</li>
    <li>SinSQ</li>
    <li>Tribas</li>
    <li>Hardlim</li>
    </ul>
    <li>Artificial Neural Networks (Multi - Layer Perceptron) Gradient Descent</li>
    </ol>
    <hr/>
   <br/>
<br/>
<h2 align="center" style="color:red">Part 1 : Data Preprocessing</h2>
<ol>
<li style="margin-left:100px;">Exploratory Data Analysis</li>
<li style="margin-left:100px;">Data Preprocessing</li>
<li style="margin-left:100px;">Cleaning</li>
<li style="margin-left:100px;">Lemmatization</li>
</ol>
<h4 style="font-weight:700">>>> Run Text_Preprocessing_MP_Hybrid.py if you want to Preprocess some datasets</h4>
<hr/>
<br/>
<br/>
<h3 align="center" style="color: green; font-weight: 650;">Flow of Control</h3>
<ol>
<li style="margin-left:100px;">Sentence Segmentation</li>
<li style="margin-left:100px;">Word Tokenization</li>
<li style="margin-left:100px;">Same consecutive chars changed to max 2 times</li>
<li style="margin-left:100px;">Spelling Corrections</li>
<li style="margin-left:100px;">Removal of #Hashtags, @Mentions, http//:URLs, etc (Noise 1)</li>
<li style="margin-left:100px;">Removal of Special Unicode Characters (Noise 2)</li>
<li style="margin-left:100px;">Chat Abbreviations conversions (Noise 3)</li>
<li style="margin-left:100px;">Removal of Punctuations except `'` (Noise 4)</li>
<li style="margin-left:100px;">Stop Words Removal (Noise 5)</li>
<li style="margin-left:100px;">Parts of Speech Tagging</li>
<li style="margin-left:100px;">Stemming & Lemmatization</li>
<li style="margin-left:100px;">WhiteSpace Removals</li>
<li style="margin-left:100px;">Chunking</li>
</ol>
<hr/>
<br/>
<br/>
<h1 align="center" style="color:red">Part 2 : Machine Learning Models Training</h1>
<hr/>
<h2>Datasets</h2>
<li>
    <h3><a style="font-weight:700;" href="https://data.world/crowdflower/sentiment-analysis-in-text">Dataset 1</a></h4>
    <h4>Value Counts</h4>
    <ul>
    <li>-1 : 15236</li>
    <li>0  : 9465</li>
    <li>1  : 15299</li>
    </ul>
</li>
<li>
    <h3><a style="font-weight:700;" href="https://www.kaggle.com/datasets/shashank1558/preprocessed-twitter-tweets">Dataset 2</a></h4>
    <h4>Value Counts</h4>
    <ul>
    <li>-1 : 1117</li>
    <li> 0 : 1570</li>
    <li> 1 : 1186</li>
    </ul>
</li>
<li>
    <h3><a style="font-weight:700;" href="https://www.kaggle.com/datasets/imrandude/twitter-sentiment-analysis">Dataset 3</a></h4>
    <h4>Value Counts</h4>
    <ul>
    <li>0 : 29720</li>
    <li>1 : 2242</li>
    </ul>
</li>
<li>
    <h3><a style="font-weight:700;" href="https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset">Dataset 4</a></h4>
    <h4>Value Counts</h4>
    <ul>
    <li>-1 : 35510</li>
    <li> 0 : 55213</li>
    <li> 1 : 72250</li>
    </ul>
</li>
