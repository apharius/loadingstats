threads <- read.csv('loadingstats.csv',header=TRUE,sep=";")

attach(threads)

png("tradar_per_timme.png",width=1920,height=1080)
barplot(table(CreationHour),main=sprintf("Skapade trådar per timme på dygnet (diagram skapat %s)",Sys.time()),col="#fd2860",ylim=c(0,40))
dev.off()

png("tradar_per_datum.png",width=1920,height=1080)
barplot(table(CreationDate),main=sprintf("Skapade trådar per datum (diagram skapat %s)",Sys.time()),col="#fd2860",ylim=c(0,35))
dev.off()

png("tradar_per_anvandare.png",width=1920,height=1080)
barplot(sort(table(Creator),decreasing=TRUE)[1:15],main=sprintf("Skapade trådar per användare (topp 15) (diagram skapat %s)",Sys.time()),col="#fd2860",ylim=c(0,60))
dev.off()
