from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
sentences = [
                "The plot was good, but the characters are uncompelling and the dialog is not great.", 
                "A really bad, horrible book.",       
                "At least it isn't a horrible book."
            ]
for sentence in sentences:
    print(sentence)
    snt = analyser.polarity_scores(sentence)
    # sentiment = vaderSentiment(sentence)
    print ("\n\t" + str(snt))