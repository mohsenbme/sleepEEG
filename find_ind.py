def find_ind(x, a):
    # finds position of a in list x
#     ind=[]
#     for i in range(0,len(x)):
#         if round(x[i])==a:
#             ind.append(i)
#     return ind[0]
    return np.argmin(abs(x-a))
