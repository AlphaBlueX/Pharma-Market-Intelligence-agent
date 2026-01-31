from typing import Dict, Any
from backend.processing.sentiment import analyze_sentiment

class AlertEngine:
    def process_news(self, news_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the severity of a news item and generates an alert if necessary.
        """
        text = news_item.get("text", "")
        sentiment = analyze_sentiment(text)
        
        # Simple heuristic for severity
        severity = "Low"
        if sentiment == "Negative":
            severity = "High" if any(kw in text.lower() for kw in ["recall", "lawsuit", "failure"]) else "Medium"
        elif sentiment == "Positive":
            severity = "Medium" if "approval" in text.lower() or "breakthrough" in text.lower() else "Low"
            
        return {
            "is_alert": severity in ["Medium", "High"],
            "severity": severity,
            "title": news_item.get("title", "Market Update"),
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "entities": news_item.get("entities", {})
        }

alert_engine = AlertEngine()
