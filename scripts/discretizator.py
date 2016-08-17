import pandas as pd

data = pd.read_csv("archivo.csv")

for i in range(8):
	data.ix[:,i] = pd.qcut(data.ix[:,i], 5, labels=["Muy Bajo","Bajo","Medio","Alto","Medio Alto"])

data.to_csv("dicretiza3.csv")