import sys
import numpy as np
import sklearn.base as skl_base

class HeroIdOneHotEncoder(skl_base.BaseEstimator, skl_base.TransformerMixin):
    def __init__(self, max_hero_id, team_r_start_end_col, team_d_start_end_col):
        self._max_hero_id = max_hero_id

        self._team_r_start_col = team_r_start_end_col[0]
        self._team_r_end_col = team_r_start_end_col[1]
        
        self._team_d_start_col = team_d_start_end_col[0]
        self._team_d_end_col = team_d_start_end_col[1]
                       
        return

    
    def fit(self, X, y = None):
        return self

    
    def transform(self, X, y = None):
        team_r = np.zeros((X.shape[0], self._max_hero_id), dtype=int)
        team_d = np.zeros((X.shape[0], self._max_hero_id), dtype=int)
        
        for row_idx in range(X.shape[0]):
            for col_idx in range(self._team_r_start_col, self._team_r_end_col + 1):
                team_r[row_idx, X[row_idx][col_idx] - 1] = 1
            
            for col_idx in range(self._team_d_start_col, self._team_d_end_col + 1):
                team_d[row_idx, X[row_idx][col_idx] - 1] = 1
    
        result = np.concatenate((team_r, team_d), axis=1)

        return result