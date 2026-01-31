def analyze_sentiment(text: str) -> str:
    """
    Very basic rule-based sentiment analysis for market news.
    """
    positive_words = ["growth", "approval", "success", "launch", "breakthrough", "strong", "positive", "increase", "gain", "profit"]
    negative_words = ["decline", "failure", "recall", "lawsuit", "negative", "loss", "decrease", "warning", "delay", "risk"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"
