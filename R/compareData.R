require("dplyr")
require("scales")
require("ggplot2")
require("foreach")
args <- commandArgs(TRUE)
filename1 <- args[1]
filename2 <- args[2]
#dfA <- read.csv("../Data/RandomWalkSimulation.csv")
#dfB <- read.csv("../Data/BFSSimulation.csv")
dfA <- read.csv(filename1)
dfB <- read.csv(filename2)
colnames(dfA) <- c("vertices","edges","algorithm","path_length","included_failure","space","time")
colnames(dfB) <- c("vertices","edges","algorithm","path_length","included_failure","space","time")
df <- rbind(dfA,dfB)
df <- tbl_df(df)
df <- arrange(df,included_failure,vertices)
df <- df[2:nrow(df),]
failureDf <- filter(df, included_failure == "True")

#selects the two algorithms being compared
algdf <- arrange(df,algorithm)
algA <- algdf[1,3]
algB <- algdf[nrow(algdf),3]
#png(paste(df$vertices, " Vertex Comparison of Path Length.png"))
graph <- ggplot(df, aes(x=edges,y=path_length)) + geom_line(data=subset(df, algorithm == "bfs"), color="grey")  + geom_line(data=subset(df, algorithm == "randomwalk"), color="grey") + geom_jitter(size = .2, aes(color=algorithm)) + geom_smooth(data=subset(df, algorithm == "randomwalk"),se=TRUE,color="green") + geom_smooth(data=subset(df, algorithm == "bfs"),se=TRUE, color="red")
graph <- graph + ggtitle(paste(df$vertices, " Vertex Comparison of Path Length"))+ xlab("Number of Edges") + ylab("Path Length")
graph <- graph + scale_colour_hue(l=10) + geom_vline(data=failureDf,color="red",size=.2,aes(xintercept=edges))
graph
#dev.off()

#png(paste(df$vertices, " Vertex Comparison of Space Per Host.png"))
graph <- ggplot(df, aes(x=edges,y=space)) + geom_jitter(size = .2, aes(color=algorithm))
graph <- graph + geom_smooth(data=subset(df, algorithm == "randomwalk"),se=TRUE,color="green") + geom_smooth(data=subset(df, algorithm == "bfs"),se=TRUE, color="red")
graph <- graph + ggtitle(paste(df$vertices, " Vertex Comparison of Space Per Host"))+ xlab("Number of Edges") + ylab("Space per host in bytes")
graph <- graph + scale_colour_hue(l=10) + geom_vline(data=failureDf,color="red",size=.2,aes(xintercept=edges))
graph
#dev.off()

#png(paste(df$vertices, " Vertex Comparison of Running Time.png"))
graph <- ggplot(df, aes(x=edges,y=time)) + geom_jitter(size = .2, aes(color=algorithm))
graph <- graph + geom_smooth(data=subset(df, algorithm == "randomwalk"),se=TRUE,color="green") + geom_smooth(data=subset(df, algorithm == "bfs"),se=TRUE, color="red")
graph <- graph + ggtitle(paste(df$vertices, " Vertex Comparison of Running Time in Seconds"))+ xlab("Number of Edges") + ylab("Running Time (Seconds/Query)")
graph <- graph + scale_colour_hue(l=10) + geom_vline(data=failureDf,color="red",size=.2,aes(xintercept=edges))
graph
#dev.off()

