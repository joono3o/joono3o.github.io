# AI+X 딥러닝 기말 프로젝트
배경준 2026026026 elsovlse@hanyang.ac.kr

이환 2026077947 lhweane@hanyang.ac.kr

이승현 2026030200 lshlsh8503@gmail.com

# Motivation
소포모어 징크스 현상을 데이터 기반으로 검증하고, 딥러닝 알고리즘을 통해 개인의 이전 성과가 이후 성과에 미치는 영향을 분석하여 성과 하락을 예측할 수 있는 모델을 구축하고자 이 프로젝트를 진행한다.

# Datasets
루키와 소포모어 시즌의 타석 수가 너무 적지 않은 1950년~2011년 데뷔 선수 200명을 데이터로 삼았다.

소포모어 스텟 (1): [mlb_sophomore_hitting_stats.csv](https://github.com/user-attachments/files/28455758/mlb_sophomore_hitting_stats.csv)

루키 스텟 (1): [mlb_rookie_hitting_stats.csv](https://github.com/user-attachments/files/28455760/mlb_rookie_hitting_stats.csv)

소포모어 스텟 (2):

루키 스텟 (2): 

# Methodology
1. 소포모어 징크스를 겪은 선수의 기준을 정하기 위해 선형회귀를 활용한다.
2. 로지스틱 회귀를 활용하여 징크스를 겪은 선수들과 그렇지 않은 선수들을 나눈 요인을 찾아본다.

# Evaluation & Analysis
Methodology의 1단계를 실행한 결과는 다음과 같다. (threshold.py 참고)

<img width="596" height="403" alt="jinx threshold" src="https://github.com/user-attachments/assets/1f3cf198-d723-4e48-bcff-a0ddff3ef1e8" />
<img width="612" height="561" alt="jinxed players" src="https://github.com/user-attachments/assets/0956306c-ace5-414b-8828-0a9df111765f" />

모든 선수들의 OPS를 선형회귀로 분석하여 징크스의 기준을 잡았다. 징크스의 기준은 루키 시즌에 비해 OPS가 0.112보다 크게 감소한 것으로 정했다. 데이터의 양이 적은 관계로
징크스를 겪은 선수는 총 23명 뿐, 전체 선수들 중 12%이다. 2단계에서 오버피팅을 피해야 함을 주의해야한다.


Methodology의 2단계를 실행한 결과는 다음과 같다.

```{python}
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
```

<img width="927" height="317" alt="화면 캡처 2026-06-08 013230" src="https://github.com/user-attachments/assets/71a2f972-3ca8-4d51-8395-679de62c1183" />
<img width="926" height="237" alt="화면 캡처 2026-06-08 013253" src="https://github.com/user-attachments/assets/c01a6f33-a140-4da6-959a-89064f3714fe" />
<img width="967" height="727" alt="화면 캡처 2026-06-08 013325" src="https://github.com/user-attachments/assets/0ed03e9b-06dd-44cd-8c1a-5d8007e3bdd9" />

첫번째 표는 징크스를 겪은 선수들과 그렇지 않은 선수들을 가르는 데에 영향을 미친 요인을 분석한 표이다. BB Rate(볼넷, 사구로 인한 출루)와 ISO(장타율)가 높은 타자들이 징크스를 피할 확률이 높은 것을 알 수 있다. 반면, SO Rate(삼진)가 높거나 루키 시즌의 일부만 보낸(Partial season) 선수들의 징크스 확률이 더 높게 나왔다.

두번째 표는 모델이 징크스를 예측한 결과를 보여주는 표이다. 표에서 보이듯이 위양성이 54개로 정확히 예측한 15개를 크게 웃도는 수치다. 마지막 그래프에서 알 수 있듯이 정확도는 0.678 정도로 무작위로 예측하는 경우일 때(대략 0.5 정확도)보다는 좋은 성능을 보여주지만, 그리 높은 정확도는 아니다. 전체 데이터량이 192명의 선수에 불과해서 이러한 결과가 나온 것으로 보인다.

# Conclusion


