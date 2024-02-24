'''
REGRESSION

Notes
- For hematuria severity measurement calibration

Documentation
- 

'''

import time
import numpy as np

from sklearn.metrics import mean_squared_error
import numpy as np

# Assuming y_true and y_pred are your true and predicted values respectively
y_true = np.array([0.3, 0.8, 4.0, 9.0, 15.0])
y_pred = np.array([2.5, 0.0, 2, 8])

# Calculate mean squared error
mse = mean_squared_error(y_true, y_pred)

# Calculate RMSE
rmse = np.sqrt(mse)

print("Root Mean Squared Error (RMSE):", rmse)



# if __name__ == '__main__':
#     yee()