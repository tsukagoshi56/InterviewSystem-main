def hello(people):
    a = ("hello, {}".format(people))
    return {
        "text": a,
        "key1": "dadada"
    }


x = [hello(p) for p in ["John", "Lennon", "Tokio", "Yamaguchi"]]

print(x)
