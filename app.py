from pathlib import Path
import json, os, math
from flask import Flask, render_template, request
from matching import calculate_score, explain_recommendation, analyze_gaps
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 65536
BASE = Path(__file__).parent

def load_careers():
    return json.loads((BASE / 'careers.json').read_text(encoding='utf-8'))

@app.get('/')
def home():
    return render_template('index.html', careers=load_careers())

@app.get('/assessment')
def assessment():
    careers=load_careers()
    return render_template('assessment.html', careers=careers, skills=sorted({s for c in careers for s in c['skills']}))

@app.post('/recommend')
def recommend():
    careers=load_careers()
    skills=sorted({s for c in careers for s in c['skills']})
    try:
        student={k:request.form.get(k,'').strip()[:120] for k in ['name','degree','branch','interests']}
        if not all(student.values()) or student['interests'] not in {c['interest'] for c in careers}: raise ValueError()
        student['hours']=int(request.form.get('hours','8'))
        if not 1 <= student['hours'] <= 80: raise ValueError()
        for skill in skills:
            student[skill]=int(request.form.get(skill,'1'))
            if not 1 <= student[skill] <= 5: raise ValueError()
    except (ValueError,TypeError):
        return render_template('error.html'),400
    results=[]
    for c in careers:
        gaps=sorted(analyze_gaps(student,c),key=lambda g:g['gap'],reverse=True)
        results.append(dict(name=c['name'],description=c['description'],score=calculate_score(student,c),reasons=explain_recommendation(student,c),gaps=gaps,weeks=max(1,math.ceil(sum(g['gap'] for g in gaps)*6/student['hours']))))
    results.sort(key=lambda c:c['score'],reverse=True)
    return render_template('result.html',student=student,recommendations=results)

@app.get('/health')
def health(): return {'status':'ok'}

if __name__ == '__main__':
    from waitress import serve
    serve(app,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))
