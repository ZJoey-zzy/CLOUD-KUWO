import numpy as np
mtranse_l2r = np.array([0.4236, 0.9034, 0.5829])
gcn_l2r = np.array([0.3279, 0.8526, 0.4874])

mtranse_r2l = np.array([0.3958,0.847,0.548])
gcn_l2r = np.array([0.3415,0.8406,0.487])

print((mtranse_l2r+mtranse_r2l)/2)
print((gcn_l2r+gcn_l2r)/2)