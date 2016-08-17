data <- read.csv("dicretiza3.csv")
d <- data[,c(4:17)] #quitar el codigo, ano y numero de linea
d2<- d[,c(1:7,10:14)]  #quitar el total de titulados y titulados/matriculados
rules_bajo <- apriori(d2,
                  parameter=list(support=0.01,
                                 confidence=0.5),
                 appearance=list(rhs=c("rdeser=Muy Bajo","rdeser=Bajo"),
                                 default="lhs"))
rules_alto <- apriori(d2,
                  parameter=list(support=0.01,
                                 confidence=0.5),
                 appearance=list(rhs=c("rdeser=Alto","rdeser=Medio Alto"),
                                 default="lhs"))


