"""HTML-Quiz-Template (feste Hülle) und Injektion des Fragen-Arrays.

Das Layout ist eine feste Hülle; das Sprachmodell liefert nur das
``questions``-Array, das inline eingespritzt wird – damit die fertige Datei per
``file://`` ohne lokalen Server und ohne CORS-Probleme öffnet.
"""
import json
from typing import List


QUIZ_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__QUIZ_TITLE__</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .status-bar {
            position: sticky;
            top: 0;
            background: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 100;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .status-info {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .mistakes { color: #dc3545; }
        .progress-container {
            width: 100%;
            background-color: #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            height: 12px;
        }
        .progress-bar {
            height: 100%;
            background-color: #28a745;
            width: 0%;
            transition: width 0.4s ease;
        }
        .quiz-container {
            max-width: 800px;
            margin: 30px auto;
            padding: 0 20px;
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        .quiz-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        h1 { text-align: center; color: #2c3e50; margin-top: 40px; }
        .question-title {
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .question-text {
            font-size: 1.2rem;
            color: #2c3e50;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .options { display: flex; flex-direction: column; gap: 10px; }
        button {
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.2s;
            text-align: left;
        }
        button:hover:not([disabled]) {
            background-color: #f0f8ff;
            border-color: #3498db;
        }
        button:disabled { cursor: not-allowed; opacity: 0.7; }
        button.correct {
            background-color: #d4edda !important;
            border-color: #28a745 !important;
            color: #155724;
        }
        button.wrong {
            background-color: #f8d7da !important;
            border-color: #dc3545 !important;
            color: #721c24;
            text-decoration: line-through;
        }
        .feedback {
            margin-top: 15px;
            padding: 15px;
            border-radius: 8px;
            display: none;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .feedback.correct-feedback {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .feedback.wrong-feedback {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .final-result {
            display: none;
            text-align: center;
            background: #e8f4fd;
            border: 2px solid #3498db;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 40px;
        }
    </style>
</head>
<body>

<div class="status-bar">
    <div class="status-info">
        <span>Fortschritt: <span id="progress-text">0%</span></span>
        <span class="mistakes">Fehler: <span id="mistake-counter">0</span></span>
    </div>
    <div class="progress-container">
        <div class="progress-bar" id="progress-bar"></div>
    </div>
</div>

<h1>__QUIZ_TITLE__</h1>

<div class="quiz-container" id="quiz-container"></div>

<div class="quiz-container">
    <div class="final-result" id="final-result">
        <h2>Quiz abgeschlossen!</h2>
        <p>Du hast alle Fragen beantwortet. Insgesamt hast du <strong id="final-mistakes">0</strong> Fehler gemacht.</p>
        <button onclick="location.reload()" style="background: #3498db; color: white; border: none; text-align: center; margin-top: 15px; padding: 12px 24px; font-size: 1.1rem; border-radius: 8px; cursor: pointer;">Quiz neustarten</button>
    </div>
</div>

<script>
    const questions = /*__QUESTIONS__*/[];

    let correctCount = 0;
    let mistakeCount = 0;

    function initQuiz() {
        const container = document.getElementById('quiz-container');
        questions.forEach((q, qIndex) => {
            const card = document.createElement('div');
            card.className = 'quiz-card';
            card.id = `question-card-${qIndex}`;
            const title = document.createElement('div');
            title.className = 'question-title';
            title.textContent = `Frage ${qIndex + 1} von ${questions.length}`;
            const text = document.createElement('div');
            text.className = 'question-text';
            text.textContent = q.text;
            const optionsContainer = document.createElement('div');
            optionsContainer.className = 'options';
            q.options.forEach((opt, optIndex) => {
                const btn = document.createElement('button');
                btn.textContent = opt;
                btn.onclick = () => handleAnswer(qIndex, optIndex, btn);
                optionsContainer.appendChild(btn);
            });
            const feedback = document.createElement('div');
            feedback.className = 'feedback';
            feedback.id = `feedback-${qIndex}`;
            card.appendChild(title);
            card.appendChild(text);
            card.appendChild(optionsContainer);
            card.appendChild(feedback);
            container.appendChild(card);
        });
    }

    function handleAnswer(qIndex, optIndex, btnElement) {
        const q = questions[qIndex];
        const card = document.getElementById(`question-card-${qIndex}`);
        const feedback = document.getElementById(`feedback-${qIndex}`);
        if (card.classList.contains('completed')) return;
        if (optIndex === q.correct) {
            btnElement.classList.add('correct');
            card.classList.add('completed');
            const allBtns = card.querySelectorAll('button');
            allBtns.forEach(b => b.disabled = true);
            feedback.className = 'feedback correct-feedback';
            feedback.innerHTML = `<strong>Richtig!</strong> ${q.explanation}`;
            feedback.style.display = 'block';
            correctCount++;
            updateProgress();
        } else {
            btnElement.classList.add('wrong');
            btnElement.disabled = true;
            mistakeCount++;
            document.getElementById('mistake-counter').textContent = mistakeCount;
            feedback.className = 'feedback wrong-feedback';
            feedback.innerHTML = `<strong>Leider falsch.</strong> Versuche es noch einmal!`;
            feedback.style.display = 'block';
        }
    }

    function updateProgress() {
        const percent = Math.round((correctCount / questions.length) * 100);
        document.getElementById('progress-bar').style.width = percent + '%';
        document.getElementById('progress-text').textContent = percent + '%';
        if (correctCount === questions.length) {
            document.getElementById('final-mistakes').textContent = mistakeCount;
            document.getElementById('final-result').style.display = 'block';
        }
    }

    initQuiz();
</script>

</body>
</html>
"""


def build_quiz_html(questions: List[dict], title: str) -> str:
    """Injiziert das Fragen-Array (als JSON, das gültiges JS ist) und den Titel."""
    q_json = json.dumps(questions, ensure_ascii=False, indent=8)
    out = QUIZ_TEMPLATE.replace("__QUIZ_TITLE__", title or "Wissens-Check")
    out = out.replace("/*__QUESTIONS__*/[]", q_json)
    return out
