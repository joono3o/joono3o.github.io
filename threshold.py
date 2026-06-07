import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

rookie = pd.read_csv('/mnt/user-data/outputs/mlb_rookie_hitting_stats.csv')
soph = pd.read_csv('/mnt/user-data/outputs/mlb_sophomore_hitting_stats.csv')

merged = rookie.merge(
    soph[['Player_ID','Sophomore_Year','G','AB','R','H','2B','3B','HR','RBI',
          'SB','CS','BB','SO','HBP','AVG','OBP','SLG','OPS']],
    on='Player_ID', suffixes=('_r','_s')
)
merged = merged[(merged['AB_s'] > 0) & (merged['OPS_s'] > 0)].copy()


X = merged[['OPS_r']].values
y = merged['OPS_s'].values

model = LinearRegression()
model.fit(X, y)

slope     = model.coef_[0]
intercept = model.intercept_
r2        = r2_score(y, model.predict(X))
rmse      = np.sqrt(mean_squared_error(y, model.predict(X)))

print(f"Linear regression: Soph_OPS = {slope:.4f} × Rookie_OPS + {intercept:.4f}")
print(f"R²   = {r2:.4f}")
print(f"RMSE = {rmse:.4f}")


merged['predicted_soph_OPS'] = model.predict(X)
merged['residual'] = merged['OPS_s'] - merged['predicted_soph_OPS']

print(f"\nResidual stats:")
print(merged['residual'].describe())


res_mean = merged['residual'].mean()
res_std  = merged['residual'].std()
threshold_1sd = res_mean - 1.0 * res_std
threshold_15sd = res_mean - 1.5 * res_std

print(f"\nResidual mean : {res_mean:.4f}")
print(f"Residual std  : {res_std:.4f}")
print(f"Threshold (−1σ) : {threshold_1sd:.4f}")
print(f"Threshold (−1.5σ): {threshold_15sd:.4f}")


merged['jinxed'] = (merged['residual'] < threshold_1sd).astype(int)
n_jinxed = merged['jinxed'].sum()
print(f"\nPlayers labelled jinxed (−1σ): {n_jinxed} / {len(merged)} = {n_jinxed/len(merged)*100:.1f}%")


print(f"\nA player is jinxed if their sophomore OPS is >{abs(threshold_1sd):.3f} below what was predicted")
print(f"(given their rookie OPS)")


jinxed_df = merged[merged['jinxed']==1].sort_values('residual')[
    ['Player_Name','Rookie_Year','OPS_r','OPS_s','predicted_soph_OPS','residual']
].head(15)
print("\nTop 15 most jinxed:")
print(jinxed_df.to_string(index=False))


best_df = merged.sort_values('residual', ascending=False)[
    ['Player_Name','Rookie_Year','OPS_r','OPS_s','predicted_soph_OPS','residual']
].head(10)
print("\nTop 10 most improved (beat prediction):")
print(best_df.to_string(index=False))
