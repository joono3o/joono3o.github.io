import pandas as pd, numpy as np, json, warnings
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
warnings.filterwarnings('ignore')

rookie = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
soph   = pd.read_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats.csv')

merged = rookie.merge(
    soph[['Player_ID','Sophomore_Year','G','AB','R','H','2B','3B','HR','RBI',
          'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS']],
    on='Player_ID', suffixes=('_r','_s')
)
merged = merged[(merged['AB_s']>0)&(merged['OPS_s']>0)].copy()
print("Merged cols:", [c for c in merged.columns if 'SF' in c or 'HBP' in c])


lr = LinearRegression().fit(merged[['OPS_r']], merged['OPS_s'])
merged['predicted_soph_OPS'] = lr.predict(merged[['OPS_r']])
merged['residual'] = merged['OPS_s'] - merged['predicted_soph_OPS']
threshold = -merged['residual'].std()
merged['jinxed'] = (merged['residual'] < threshold).astype(int)


merged['HR_rate']  = merged['HR_r']  / merged['AB_r']
merged['BB_rate']  = merged['BB_r']  / merged['AB_r']
merged['SO_rate']  = merged['SO_r']  / merged['AB_r']
merged['ISO']      = merged['SLG_r'] - merged['AVG_r']
merged['partial']  = (merged['AB_r'] < 300).astype(int)
merged['BABIP']    = ((merged['H_r'] - merged['HR_r']) /
                      (merged['AB_r'] - merged['SO_r'] - merged['HR_r'] + 1)
                     ).clip(0,1)

features     = ['OPS_r','HR_rate','BB_rate','SO_rate','ISO','partial','BABIP','AVG_r']
feat_labels  = ['Rookie OPS','HR Rate','BB Rate','SO Rate','ISO (Power)',
                'Partial Season','BABIP','Batting Avg']

df = merged[features+['jinxed','Player_Name','Rookie_Year']].dropna().copy()
X  = df[features].values
y  = df['jinxed'].values
print(f"n={len(df)}, jinxed={y.sum()} ({y.mean()*100:.1f}%)")

scaler = StandardScaler()
X_sc   = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model.fit(X_sc, y)

cv      = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc  = cross_val_score(model, X_sc, y, cv=cv, scoring='roc_auc')
cv_f1   = cross_val_score(model, X_sc, y, cv=cv, scoring='f1')
cv_acc  = cross_val_score(model, X_sc, y, cv=cv, scoring='accuracy')

y_prob  = model.predict_proba(X_sc)[:,1]
y_pred  = model.predict(X_sc)
cm      = confusion_matrix(y, y_pred)
fpr,tpr,_ = roc_curve(y, y_prob)
auc     = roc_auc_score(y, y_prob)

coefs = sorted(zip(feat_labels, model.coef_[0]), key=lambda x: x[1])

df['jinx_prob']       = y_prob
df['predicted_jinxed']= y_pred

print(f"\nAUC={auc:.3f}, CV-AUC={cv_auc.mean():.3f}±{cv_auc.std():.3f}")
print(f"CV-F1={cv_f1.mean():.3f}, CV-Acc={cv_acc.mean():.3f}")
print("\nConfusion matrix:\n", cm)
print("\nCoefficients:")
for f,c in coefs:
    print(f"  {f:20s} coef={c:.4f}  OR={np.exp(c):.3f}")

out = {
    'n_players': int(len(df)), 'n_jinxed': int(y.sum()),
    'pct_jinxed': round(float(y.mean()*100),1),
    'threshold': round(float(threshold),4),
    'cv_auc': round(float(cv_auc.mean()),3), 'cv_auc_std': round(float(cv_auc.std()),3),
    'cv_f1': round(float(cv_f1.mean()),3),   'cv_acc': round(float(cv_acc.mean()),3),
    'auc': round(float(auc),3),
    'intercept': round(float(model.intercept_[0]),4),
    'confusion_matrix': cm.tolist(),
    'coefficients': [{'feature':f,'coef':round(float(c),4),'odds_ratio':round(float(np.exp(c)),4)} for f,c in coefs],
    'roc_fpr': [round(float(v),4) for v in fpr],
    'roc_tpr': [round(float(v),4) for v in tpr],
    'players': [
        {'name': row.Player_Name, 'year': int(row.Rookie_Year),
         'jinx_prob': round(float(row.jinx_prob),4),
         'actual': int(row.jinxed), 'predicted': int(row.predicted_jinxed),
         'ops_r': round(float(df.at[idx,'OPS_r']),3),
         'hr_rate': round(float(df.at[idx,'HR_rate']),4),
         'bb_rate': round(float(df.at[idx,'BB_rate']),4),
         'so_rate': round(float(df.at[idx,'SO_rate']),4),
         'partial': int(df.at[idx,'partial']),
         'babip': round(float(df.at[idx,'BABIP']),3),
         'iso': round(float(df.at[idx,'ISO']),3),
        }
        for idx, row in df.iterrows()
    ]
}
with open('/tmp/logit_results.json','w') as f:
    json.dump(out, f)
print("Saved. JSON size:", len(json.dumps(out)))
