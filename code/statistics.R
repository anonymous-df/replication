data <- read.csv("diff_models_token.csv", header=TRUE)
summary(data)
library(ggplot2)
ggplot(data,aes(token)) + geom_density()

data$token

library(ggvenn)
x <- list(
  "n-gram" = data$id[data$ngram==1], 
  "LSTM" = data$id[data$lstm==1], 
  "DockerFill" = data$id[data$dockerfill==1]
)

ggvenn(
  x, 
  fill_color = c("#0073C2FF",  "#CD534CFF", "#CD534CFF"),
  stroke_size = 0.5, set_name_size = 5,show_percentage = TRUE
)


library('epitools')
library(effsize)
data <- read.csv("diff_models_line.csv", header=TRUE)
summary(data)
matrix<-c(data$ngram[data$metric=='Acc-1'],data$dockerfill[data$metric=='Acc-1'])
mcnemar.test(data$ngram[data$metric=='Acc-1'],data$dockerfill[data$metric=='Acc-1'])
mcnemar.test(data$ngram[data$metric=='Acc-5'],data$dockerfill[data$metric=='Acc-5'])
wilcox.test(data$ngram[data$metric=='MRR'],data$dockerfill[data$metric=='MRR'])
boxplot(data$ngram[data$metric=='MRR'],data$dockerfill[data$metric=='MRR'])
summary(data$ngram[data$metric=='MRR'])
summary(data$dockerfill[data$metric=='MRR'])


mcnemar.test(data$ngram[data$metric=='EM'],data$dockerfill[data$metric=='EM'])
wilcox.test(data$ngram[data$metric=='ED'],data$dockerfill[data$metric=='ED'])
wilcox.test(data$ngram[data$metric=='BLEU'],data$dockerfill[data$metric=='BLEU'])
wilcox.test(data$ngram[data$metric=='ROUGE'],data$dockerfill[data$metric=='ROUGE'])
wilcox.test(data$ngram[data$metric=='METEOR'],data$dockerfill[data$metric=='METEOR'])

oddsratio(data$ngram[data$metric=='EM'],data$dockerfill[data$metric=='EM'],correction = F)
cliff.delta(data$dockerfill[data$metric=='ED'],data$ngram[data$metric=='ED'])
cliff.delta(data$ngram[data$metric=='BLEU'],data$dockerfill[data$metric=='BLEU'])
cliff.delta(data$ngram[data$metric=='ROUGE'],data$dockerfill[data$metric=='ROUGE'])
cliff.delta(data$ngram[data$metric=='METEOR'],data$dockerfill[data$metric=='METEOR'])


mcnemar.test(data$lstm[data$metric=='Acc-1'],data$dockerfill[data$metric=='Acc-1'])
mcnemar.test(data$lstm[data$metric=='Acc-5'],data$dockerfill[data$metric=='Acc-5'])
wilcox.test(data$lstm[data$metric=='MRR'],data$dockerfill[data$metric=='MRR'])


oddsratio(data$ngram[data$metric=='Acc-1'],data$dockerfill[data$metric=='Acc-1'],correction = F)
oddsratio(data$ngram[data$metric=='Acc-5'],data$dockerfill[data$metric=='Acc-5'],correction = F)
cliff.delta(data$ngram[data$metric=='MRR'],data$dockerfill[data$metric=='MRR'])

summary(data)

oddsratio(data$dockerfill[data$metric=='Acc-1'],data$lstm[data$metric=='Acc-1'],correction = F)
oddsratio(data$lstm[data$metric=='Acc-5'],data$dockerfill[data$metric=='Acc-5'],correction = F)
cliff.delta(data$lstm[data$metric=='MRR'],data$dockerfill[data$metric=='MRR'])

#####
data <- read.csv("stats_token_types.csv", header=TRUE)
mcnemar.test(subset(data, metric=='Acc-1' & type == 'Identifier')$lstm,subset(data, metric=='Acc-1' & type == 'Identifier')$dockerfill)
oddsratio(subset(data, metric=='Acc-1' & type == 'Identifier')$lstm,subset(data, metric=='Acc-1' & type == 'Identifier')$dockerfill,correction = F)

mcnemar.test(subset(data, metric=='Acc-5' & type == 'Identifier')$lstm,subset(data, metric=='Acc-5' & type == 'Identifier')$dockerfill)
oddsratio(subset(data, metric=='Acc-5' & type == 'Identifier')$lstm,subset(data, metric=='Acc-5' & type == 'Identifier')$dockerfill,correction = F)

wilcox.test(subset(data, metric=='MRR' & type == 'Identifier')$lstm,subset(data, metric=='MRR' & type == 'Identifier')$dockerfill)
cliff.delta(subset(data, metric=='MRR' & type == 'Identifier')$lstm,subset(data, metric=='MRR' & type == 'Identifier')$dockerfill)


mcnemar.test(subset(data, metric=='Acc-1' & type == 'String')$ngram,subset(data, metric=='Acc-1' & type == 'String')$dockerfill)
oddsratio(subset(data, metric=='Acc-1' & type == 'String')$ngram,subset(data, metric=='Acc-1' & type == 'String')$dockerfill,correction = F)

mcnemar.test(subset(data, metric=='Acc-5' & type == 'String')$ngram,subset(data, metric=='Acc-5' & type == 'String')$dockerfill)
oddsratio(subset(data, metric=='Acc-5' & type == 'String')$ngram,subset(data, metric=='Acc-5' & type == 'String')$dockerfill,correction = F)

wilcox.test(subset(data, metric=='MRR' & type == 'String')$ngram,subset(data, metric=='MRR' & type == 'String')$dockerfill)
cliff.delta(subset(data, metric=='MRR' & type == 'String')$ngram,subset(data, metric=='MRR' & type == 'String')$dockerfill)


mcnemar.test(subset(data, metric=='Acc-1' & type == 'Symbol')$ngram,subset(data, metric=='Acc-1' & type == 'Symbol')$dockerfill)
oddsratio(subset(data, metric=='Acc-1' & type == 'Symbol')$ngram,subset(data, metric=='Acc-1' & type == 'Symbol')$dockerfill,correction = F)

mcnemar.test(subset(data, metric=='Acc-5' & type == 'Symbol')$ngram,subset(data, metric=='Acc-5' & type == 'Symbol')$dockerfill)
oddsratio(subset(data, metric=='Acc-5' & type == 'Symbol')$ngram,subset(data, metric=='Acc-5' & type == 'Symbol')$dockerfill,correction = F)

wilcox.test(subset(data, metric=='MRR' & type == 'Symbol')$ngram,subset(data, metric=='MRR' & type == 'Symbol')$dockerfill)
cliff.delta(subset(data, metric=='MRR' & type == 'Symbol')$ngram,subset(data, metric=='MRR' & type == 'Symbol')$dockerfill)

####
p.adjust(p, method = 'holm', n = length(p))

#
  data <- as.matrix(data.frame(Similarity = c(1.36, 1.65, 2.88),         
                               Naturalness = c(1.86, 2.01, 3.01),
                               Informativeness = c(2.20, 2.33, 3.23)
  )) 

rownames(data) <- c("n-gram", "DockerFill")

# ·Ö×éÖù×´Í¼
t<-barplot(data,                                        
          col = c("#e0beb3", "#fbf0c6",  "#c2dcf3"),
          border = "black", # Öù×Ó±ß¿òÎªºÚÉ«
          # names.arg = c('control1', 'case1', 'control2', 'case2', 'case3'),  # Öù×ÓÃû³Æ
          #xlab = 'class',  # XÖá±êÌâ
          ylab = 'Score',  # YÖá±êÌâ
          ylim = c(0, 4),
          beside = TRUE,
           )
 
 text(t, data+0.18, labels=c(1.36, 1.65, 2.88, 1.86, 2.01, 3.01, 2.20, 2.33, 3.23))
 # Í¼Àı
 legend("top",                                    
        legend = c("n-gram", "LSTM", "DockerFill"),
        fill = c("#e0beb3", "#fbf0c6",  "#c2dcf3"),
        ncol = 3)

library(exact2x2)
library(effsize)
library(xtable)


library(psych)
M<-read.csv('human_scores.csv',header=TRUE,sep=",")
cohen.kappa(x=cbind(M$lstm.s1,M$lstm.s2))  #0.82
cohen.kappa(x=cbind(M$lstm.n1,M$lstm.n2))  #0.75
cohen.kappa(x=cbind(M$lstm.i1,M$lstm.i2))  #0.71


cohen.kappa(x=cbind(M$ngram.s1,M$ngram.s2)) #0.65
cohen.kappa(x=cbind(M$ngram.n1,M$ngram.n2)) #0.52
cohen.kappa(x=cbind(M$ngram.i1,M$ngram.i2)) #0.64

cohen.kappa(x=cbind(M$dockerfill.s1,M$dockerfill.s2)) #0.92
cohen.kappa(x=cbind(M$dockerfill.n1,M$dockerfill.n2)) #0.88
cohen.kappa(x=cbind(M$dockerfill.i1,M$dockerfill.i2)) #0.74

d<-c(0.82,0.75,0.71,0.65,0.52,0.64,0.92,0.88,0.74)
mean(d)

