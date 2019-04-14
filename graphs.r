threads <- read.csv('threads.csv',header=TRUE,sep=";",quote="")
redaktionen <- c('Isabell Rydén','Aleksandar Buntic','Alexander Rehnman','Amanda Steén','Eric Lindholm','Jimmy Seppälä','Kiki','Albin Mobäck','Anders Eklöf','Niklas Karlsson','Oskar Skog','Petter Arbman','Simon Liljedahl','Tomas Engström','Jerry Olsson')

attach(threads)

png("tradar_per_timme.png",width=1920,height=1080)
barplot(table(CreationHour),main=sprintf("Skapade trådar per timme på dygnet (diagram skapat %s)",Sys.time()),col="#fd2860")
dev.off()

png("tradar_per_datum.png",width=1920,height=1080)
barplot(table(CreationDate),main=sprintf("Skapade trådar per datum (diagram skapat %s)",Sys.time()),col="#fd2860")
dev.off()

png("tradar_per_anvandare.png",width=1920,height=1080)
barplot(sort(table(Creator),decreasing=TRUE)[1:15],main=sprintf("Skapade trådar per användare (topp 15) (diagram skapat %s)",Sys.time()),col="#fd2860")
dev.off()

detach(threads)


replies <- threads[,c(1,6)]
attach(replies)
replies <- replies[order(-NumberOfReplies),]
topfifteen <- replies[2:16,]
topfifteen <- droplevels(topfifteen)
detach(replies)

attach(topfifteen)

png("topp_15_tradar_utan_bsl.png",width=1920,height=1080)
par(mar=c(25.1,4.1,4.1,2.1),las=2)
barplot(NumberOfReplies,names.arg=Title,main=sprintf("Topp 15 trådar efter inlägg (förutom Bullshit Lounge) (diagram skapat %s)",Sys.time()),col="#fd2860")
dev.off()

detach(topfifteen)

posts <- read.csv('posts.csv',header=TRUE,sep=";")

attach(posts)

posts_hour_title <- sprintf("Inlägg per timme på dygnet (diagram skapat %s)",Sys.time())

png("inlagg_per_timme.png",width=1920,height=1080)
barplot(table(PostHour),main=posts_hour_title,col="#fd2860")
dev.off()

posts_date_title <- sprintf("Inlägg per datum (diagram skapat %s)",Sys.time())
png("inlagg_per_datum.png",width=1920,height=1080)
barplot(table(PostDate),main=posts_date_title,col="#fd2860")
dev.off()

post_users_title <- sprintf("Topp 15 användare efter inlägg (diagram skapat %s)",Sys.time())
png("inlagg_per_anvandare.png",width=1920,height=1080)
barplot(sort(table(Poster),decreasing=TRUE)[1:15],main=post_users_title,col="#fd2860")
dev.off()

editor_posts <- posts[posts$Poster %in% redaktionen,]

for(editor in redaktionen){
	specific_editor <- editor_posts[editor_posts$Poster == editor,]
	datetable <- table(specific_editor$PostDate)
	png(sprintf("redaktionen/%s.png",editor),width=1920,height=1080)
	barplot(datetable,main=sprintf("Aktivitetsdiagram för %s",editor),col="#fd2860")
	dev.off()
	
}
