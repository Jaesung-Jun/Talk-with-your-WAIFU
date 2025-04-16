from mlask import MLAsk

def get_emotion_analyzer():
    emotion_analyzer = MLAsk()
    return emotion_analyzer

def emotion_detection(emotion_analyzer, msg):
    
    emo = emotion_analyzer.analyze(msg)

    if emo['emotion'] != None:
        return list(emo['emotion'])
    else:
        return ['default']