# FairView: scholarship shortlisting prototype

README prose word count: about 1,060 (including the table) (code and commands not counted).

FairView is a small intelligent interactive system for my Intelligent Interactive Systems project. A person role-plays a scholarship applicant. A scoring model gives a decision, shown with or without reasons, and an audit view compares fairness ratings with outcomes by income band. All data is synthetic.

## Project status

- Works (implemented): profile sliders and three personas, the scoring model, the shortlist / borderline / not-shortlisted rule, Condition A (decision only) and Condition B (decision, factors, what-if), rating, comment and flag (held in the page for the session, with a CSV download; nothing is sent anywhere).
- Simulated: the audit view. It scores 500 synthetic applicants with the same model. Its fairness ratings are placeholders loaded by a button, not participant data. The borderline "a person will decide" hand-over is a message only: there is no real reviewer or review queue.
- Planned, not built: a small pilot with a diverse sample, optional language-model rewording of the explanation checked against written criteria, and retraining without the income band.

## Technology stack

- index.html: one file of HTML and JavaScript. It holds the interface and the model's weights. No server, no installation.
- train_model.py: Python with NumPy and scikit-learn. It trains a logistic regression on 300 synthetic past decisions and writes model.json. An income effect is seeded into those decisions on purpose, so the audit has something to find.
- No language model runs inside the prototype and no API key is needed.
- Undecided: whether to add a language-model rewording step.

## Running or inspecting the work

- Open index.html in any browser. Use the persona buttons, move the sliders, switch between Condition A and B, then rate and flag.
- Press "Load placeholder ratings" to see the audit table filled.
- To retrain: pip install numpy scikit-learn, then python train_model.py. Paste the new model.json values into index.html if you change them.

```
pip install numpy scikit-learn
python train_model.py
```

## Development record

- Stage 1, first version: a Streamlit app (fairview.py) with sliders, A/B toggle and a ratings file. I dropped it before use because it needed installation and was more than the project needed. It is not part of the submission.
- Stage 2, scope cut: I designed adaptive explanation depth, a confirmation dialog and a third condition showing every weight, then removed them. The brief rewards clear reasoning over feature count, so I kept three ideas: explain, admit doubt, check.
- Stage 3, borderline band: I added the 40-60% referral to a person, because an inference is a bet and a confident guess on a close case is the worse error.
- Stage 4, audit view: I added outcomes by income band and a flip test, because ratings measure perception and cannot show that a system is fair.
- Stage 5, checks: before relying on the prototype I tested three things. The decision label follows the rule. Every what-if really reaches 60%. No what-if advises changing income. All passed for the three personas, and a browser test confirmed that rating, flag and the audit table work and that the console shows no errors.
- Stage 6, my own test run: I opened index.html and ran all three personas. Likelihoods matched the model (Sam 23%, Priya 49%, Alex 25%). Priya at income band 5 reached 96%, and Sam at band 5 moved from not shortlisted to borderline. Priya's grades bar stayed slightly larger than her income bar, so the report says income is one of the largest factors, not the largest. High grades shortlisted Alex despite low income. The placeholder audit table showed the expected means (A 5.6 / 2.4, B 5.7 / 3.3).
- Change after testing: the report and storyboards talk about "Condition B", but when I first opened the prototype I could not tell which control switched it. A comparison of two conditions only works if the person can see which one they are in, so I renamed the toggle label from "Demo control:" to "Condition (A or B):" and re-ran the browser test, which still passed. The commit history shows this change.

## AI assistance

- Tool: Claude (Anthropic).
- What was mine: the project idea and research gap (from my Assignment 1), choosing scholarship shortlisting, keeping the system simple, the three-idea scope (explain, admit doubt, check), the idea of comparing outcomes by group, and every decision on what to keep or cut. I directed each revision and I am responsible for the claims in the report. AI was only an aid: the design is mine, and AI helped build and illustrate it.
- What Claude did: generated the system diagram and storyboard images, helped build the scoring model and wrote the code for the prototype to my design, and drafted the report text and this README for me to edit.
- Original, reused and assisted work:

| Part | Original (mine) | Reused | AI-assisted (Claude) |
|---|---|---|---|
| Idea, gap, scope | Gap from my Assignment 1; scholarship setting; three-idea scope | Findings of Wang et al., Alves et al., Starke et al. | None |
| Scoring model | What it must do, what stays out, the group-comparison idea | scikit-learn, NumPy | Wrote the training script and model to my design |
| Prototype (index.html) | Screens, conditions, personas, what-if limits, what to cut | None | Wrote the code to my design |
| Diagram and storyboards | What they show and the simpler layout | Matplotlib | Generated the images |

- How I guided the model and prototype (Claude built to these instructions):
  - I said the project must not be an elaborate software project, only a way to show an intelligent system, so Claude dropped the first Streamlit version for one HTML file.
  - I said I needed a prototype to demonstrate, and asked how algorithmic fairness could be demonstrated at all. That led to comparing ratings with measured outcomes.
  - I suggested grouping the data by a demographic and comparing groups. This became the audit view, with income band as the group and a bias seeded on purpose so there is something to find.
  - Claude's first hand-weighted rule was replaced with a trained logistic regression, because a fixed rule is not really intelligent.
  - I asked for the whole design to stay simple but smart, which fixed the limit of three ideas and the plain, one-flow diagram.
- How I used and checked it: I tested all three personas myself in the browser, corrected the claim that income is the biggest factor to "one of the largest" after seeing Priya's grades bar, and relabelled the condition toggle after I could not find Condition B. Checks run: the three behaviour checks above; the storyboard numbers against the prototype's output; the lecture claims against the slides; the Assignment 1 findings against my review. Claude ran several of these, so I will repeat the key ones myself before submitting.

## Additional files

- figures/: the system diagram, three storyboards and a prototype screenshot, as used in the report.
- No ZIP is needed.
