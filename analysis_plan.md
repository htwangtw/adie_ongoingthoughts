# Analysis Plan 

---

## Behavioural Data Analysis 

### Aim: To understand patterns of ongoing thought in the ASD patients and controls during n-back task, before and after intervention.

### The data will come from thought probes during n-back task.

1. Locate raw data 

   - One row per question 

2. Gather all such data, adding a column for whether they were a) control/ASD ; b) with/without ECG c) participant number d) RCT - interoceptive or exteroceptive task 

3. Transpose data so that one row = one thought probe (Will have multiiple rows per participant) 

4. Run PCA 

   - Run one PCA on all data

   - Supplementary: Run seperate PCAs for each group & sub group, and see how the extracted componants correlate with the original main factors. 

5. Present the data from this PCA in the form of wordclouds and heatmaps 

6. Linear mixed Model 

   - How do the factor loadings differ as a function of group (asc vs controls), trial (0-back 1-back) and timepoint (baseline vs post training)?
- Fixed effects: Trial type (0-back/1-back), Group (Control or ASD), timepoint (baseline or posttraining)
   - Use pca_res.csv, from pca.py script 

---

## Neuroimaging Data Analysis 

### Raw data location



### Preprocessing 

- Organise this data into BIDS format if not already done.
- Need to account for lack of T1s

----

### Interoception task 

- Participants completed heartbeat discrimintation task.   Audible tones were presented in or out of sync with their heart beat. They had to judge whether this series of tones were synchronous or asynchronous with their heart. 

#### Analysis 

- Descriptives: Number of correct/incorrect responses 

- Regressors at 1st level: 1) Synchronous trials, correct response 2) Asynchronous trials, correct response, 3) Synchronous trials, incorrect response 4) Asynchronous trials, incorrect response
- Contrasts at 1st level: 1) Synchronous correct > Synchronous incorrect; 2) Synchronous correct > Asynchronus correct
- Regressors at higher level: 1) Control? 2) ASC? 3) Baseline? 3) Post training?
- Contrasts at higher level: 1) Control > ASC 2) Baseline > Post Training (only for ASC)

#### Hypotheses (from protocol): 

H1: In control participants (non-ASC) compared to ASC at baseline, enhanced BOLD in bilateral insula, lateral somatomotor & adjacent parietal cortices, anterior cingulate cortex and  supplementary motor cortex. 

- Control > ASC 

H2: Compared to baseline, ASC subjects after introception training will show greater inslula BOLD activity. 

- ASC + follow up > ASC + baseline 

----

### Mind wandering task 

- Participants had to follow white circle and press button when it turned red (Ottaviani, 2013). 
- Thought probes: Focus; Distracted External; Distracted Internal; Distracted Body; Anxious Ruminating

#### Hypothesis (from protocal)

H1: Higher level of rumination in ASC vs Controls 

H2: Lower levels of rumination in ASC post training compared to baseline 

H3: Higher DMN activity related to higher mind wandering  (- not sophisticated enough)

#### Method

- PCA on all mindwandering data 
- Calculate factor scores on a per probe basis 

- 1st level regressors: scores on each thought factor 
- 1st level contrasts: contrasting one thoughht factor against another 

