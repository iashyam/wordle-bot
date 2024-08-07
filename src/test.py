xs = ['shyam', 'ram', 'mphit', 'dev']

def f(x):
    return True if len(x)==5 else False

filtered = list(filter(f, xs))
print(filtered)
