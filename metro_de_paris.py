import pandas

dir_dist = pandas.read_csv('dir_dist.csv', header=None)
real_dist = pandas.read_csv('real_dist.csv', header=None)

print(dir_dist)
print(real_dist)